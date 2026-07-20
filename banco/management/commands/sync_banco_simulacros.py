import random
import unicodedata

from django.core.management.base import BaseCommand
from django.db import transaction

DIAGNOSTICO_SLUG = 'diagnostico-inicial'
MUESTRA_POR_MODULO_DIAGNOSTICO = 3
AREAS_DISCIPLINARES = ['ingles', 'tecnologia', 'matematicas', 'ciencias_naturales', 'ciencias_sociales']
TIPOS_ITEM_GRADUADO = ['mas_adecuada', 'menos_adecuada']

# Modulos sin banco de preguntas propio (Documento Maestro Cap. 4, Modulos
# 10 y 11): se renderizan con analisis en vivo del historial del usuario
# (contenidos/views.py:TIPOS_CON_ANALISIS + seguimiento/analitica.py), no
# con un Simulacro de preguntas fijas. No se sincronizan aqui.
SLUGS_SIN_SIMULACRO_PROPIO = {'analisis-del-desempeno', 'plan-de-fortalecimiento'}

# slug legacy -> slug canonico vigente en dashboard/question_generator.py:MODULES.
# Quedaron huerfanos por sucesivas rondas de renombrado
# (renombrar_arquitectura_institucional) que solo tocaban el nombre visible
# del Simulacro, nunca el academics.Module al que apuntaba ni el slug del
# Module canonico creado por apply_market_ready_upgrade. Reapuntar en vez
# de crear una fila nueva preserva el id del Simulacro y su historial de
# Intento.
SLUGS_LEGACY_A_CANONICO = {
    'competencias-comportamentales-tjs': 'analisis-de-casos',
}


def _normalizar(texto):
    """Minuscula + sin tildes, para comparar 'competencia' sin que un acento
    inconsistente entre el catalogo (dashboard/question_generator.py) y el
    contenido cargado (importar_lote_oficial/ingest_smpi) deje un modulo
    entero sin preguntas asignadas."""
    texto = (texto or '').strip().lower()
    return ''.join(c for c in unicodedata.normalize('NFKD', texto) if not unicodedata.combining(c))


class Command(BaseCommand):
    help = (
        'Conecta el Banco de Items ya publicado (BancoPregunta activa=True, '
        'estado=publicado) con el Simulacro real de cada modulo del catalogo '
        '(dashboard.question_generator.MODULES). Repara el enlace Simulacro-'
        'Module cuando quedo apuntando a un slug legacy tras un renombrado, '
        'crea el Simulacro si un modulo nunca tuvo uno (ej. Inclusion '
        'Educativa, Gestion Escolar), actualiza Simulacro.preguntas (set — '
        'refleja exactamente el banco publicado actual, no acumula) y activa '
        'el Simulacro si termina con al menos --min-preguntas preguntas. '
        'El Diagnostico Inicial tiene banco propio (competencia="Diagnostico '
        'integral", temas: Analisis de errores, Comprension de consigna, '
        'Gestion del tiempo, Plan de estudio - Documento Maestro Cap. 4, '
        'Modulo 1, actualizado con el Banco Oficial de Preguntas) y ademas '
        'se completa con una muestra de items ya publicados de los demas '
        'modulos, para mantener variedad y cobertura general del examen.\n\n'
        'No borra preguntas del banco ni borra ningun Simulacro existente. '
        'Correr despues de activar_lote_oficial o de ingest_smpi; forma '
        'parte del pipeline automatico de build.sh para que un modulo '
        'publicado en el banco quede disponible a los estudiantes sin pasos '
        'manuales.'
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--min-preguntas', type=int, default=1,
            help='Minimo de preguntas activas para activar el Simulacro (default 1)'
        )

    def handle(self, *args, **options):
        from banco.models import BancoPregunta
        from simulacros.models import Simulacro
        from academics.models import Module
        from dashboard.question_generator import MODULES, AREA_MODULE_SLUG

        min_preguntas = options['min_preguntas']
        publicadas = list(BancoPregunta.objects.filter(activa=True, estado='publicado'))

        resumen = []
        muestras_para_diagnostico = []
        preguntas_propias_diagnostico = []

        with transaction.atomic():
            self._desactivar_modulos_legacy(Module, resumen)

            for entry in MODULES:
                slug = entry['slug']
                if slug == DIAGNOSTICO_SLUG:
                    # El Diagnostico Inicial ahora tiene banco propio
                    # (Banco Oficial de Preguntas, competencia="Diagnostico
                    # integral"). Se captura aqui pero su Simulacro se arma
                    # al final, combinado con la muestra de los demas modulos.
                    competencia_norm = _normalizar(entry['competencia'])
                    preguntas_propias_diagnostico = [
                        p for p in publicadas if _normalizar(p.competencia) == competencia_norm
                    ]
                    continue
                if slug in SLUGS_SIN_SIMULACRO_PROPIO:
                    continue  # Los dos de solo-analisis no llevan Simulacro.

                if slug == AREA_MODULE_SLUG:
                    for area in AREAS_DISCIPLINARES:
                        preguntas = [p for p in publicadas if p.area == area]
                        simulacro = self._resolver_simulacro(Simulacro, Module, entry, area=area)
                        if not simulacro:
                            resumen.append(f'  [omitido] Sin Module para "{slug}" / area={area}')
                            continue
                        self._aplicar(simulacro, preguntas, min_preguntas, resumen)
                        muestras_para_diagnostico += self._muestra(preguntas)
                    continue

                competencia_norm = _normalizar(entry['competencia'])
                if entry['tipo'] == 'competencias_tjs':
                    # Unico modulo con calificacion por idoneidad graduada
                    # (Documento Maestro Cap. 1.4.4 / 8.5) - cualquier item
                    # graduado pertenece aqui aunque su 'competencia' libre
                    # no coincida textualmente con la del catalogo.
                    preguntas = [
                        p for p in publicadas
                        if _normalizar(p.competencia) == competencia_norm or p.tipo_item in TIPOS_ITEM_GRADUADO
                    ]
                else:
                    preguntas = [p for p in publicadas if _normalizar(p.competencia) == competencia_norm]

                simulacro = self._resolver_simulacro(Simulacro, Module, entry)
                if not simulacro:
                    resumen.append(f'  [omitido] Sin Module para "{slug}"')
                    continue
                self._aplicar(simulacro, preguntas, min_preguntas, resumen)
                muestras_para_diagnostico += self._muestra(preguntas)

            diagnostico_entry = next((e for e in MODULES if e['slug'] == DIAGNOSTICO_SLUG), None)
            diagnostico = self._resolver_simulacro(Simulacro, Module, diagnostico_entry) if diagnostico_entry else None
            if diagnostico:
                vistos = set()
                muestra_final = []
                for p in preguntas_propias_diagnostico + muestras_para_diagnostico:
                    if p.id not in vistos:
                        vistos.add(p.id)
                        muestra_final.append(p)
                self._aplicar(diagnostico, muestra_final, min_preguntas, resumen)
            else:
                resumen.append('  [omitido] Sin Module para "diagnostico-inicial"')

        for linea in resumen:
            self.stdout.write(linea)
        self.stdout.write(self.style.SUCCESS(f'Sincronizacion completa: {len(resumen)} linea(s) procesadas.'))

    def _desactivar_modulos_legacy(self, Module, resumen):
        for slug_legacy in SLUGS_LEGACY_A_CANONICO:
            actualizados = Module.objects.filter(slug=slug_legacy, is_active=True).update(is_active=False)
            if actualizados:
                resumen.append(f'  Module legacy desactivado: "{slug_legacy}"')

    def _resolver_simulacro(self, Simulacro, Module, entry, area=None):
        """Devuelve el Simulacro vigente para este modulo del catalogo,
        reapuntando uno legacy si existe (preserva id/historial de Intento)
        o creando uno nuevo si el modulo nunca tuvo Simulacro propio."""
        canon_module = Module.objects.filter(slug=entry['slug']).first()
        if not canon_module:
            return None

        tipo_sim = entry['tipo_sim']
        area_valor = area if area is not None else entry.get('area', 'general')

        existente = Simulacro.objects.filter(module=canon_module, tipo=tipo_sim, area=area_valor).order_by('-id').first()
        if existente:
            return existente

        # Un Simulacro legacy puede seguir apuntando a un Module con un slug
        # anterior del mismo modulo (ver SLUGS_LEGACY_A_CANONICO / historial
        # de renombrado). Se identifica por tipo+area+nombre visible y se
        # reapunta al Module canonico en vez de crear una fila nueva.
        huerfano = (
            Simulacro.objects.filter(nombre=entry['title'], tipo=tipo_sim, area=area_valor)
            .exclude(module=canon_module)
            .order_by('-id').first()
        )
        if huerfano:
            huerfano.module = canon_module
            huerfano.save(update_fields=['module'])
            return huerfano

        nombre = entry['title']
        if area is not None:
            from banco.models import BancoPregunta
            nombre = f"Simulacro por área - {dict(BancoPregunta.AREA_CHOICES)[area]}"

        return Simulacro.objects.create(
            nombre=nombre,
            descripcion=entry['description'],
            tipo=tipo_sim,
            module=canon_module,
            area=area_valor,
            activo=False,
        )

    def _muestra(self, preguntas):
        if len(preguntas) <= MUESTRA_POR_MODULO_DIAGNOSTICO:
            return list(preguntas)
        return random.Random(42).sample(preguntas, MUESTRA_POR_MODULO_DIAGNOSTICO)

    def _aplicar(self, simulacro, preguntas, min_preguntas, resumen):
        simulacro.preguntas.set(preguntas)
        deberia_activarse = len(preguntas) >= min_preguntas
        if simulacro.activo != deberia_activarse:
            simulacro.activo = deberia_activarse
            simulacro.save(update_fields=['activo'])
        resumen.append(f'  {simulacro.nombre} (id={simulacro.id}): {len(preguntas)} pregunta(s) -> activo={simulacro.activo}')
