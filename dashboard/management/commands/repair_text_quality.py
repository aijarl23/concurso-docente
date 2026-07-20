from django.core.management.base import BaseCommand
from django.db.models import Count

from academics.models import Category, Module, NormativeResource
from banco.models import BancoPregunta, Categoria, Subcategoria
from commerce.models import Product
from contenidos.models import Modulo, Tema
from simulacros.models import Simulacro
from usuarios.models import Usuario


TEXT_MODELS = [
    Category,
    Module,
    NormativeResource,
    Categoria,
    Subcategoria,
    BancoPregunta,
    Product,
    Modulo,
    Tema,
    Simulacro,
    Usuario,
]


REPLACEMENTS = {
    '?rea': 'área',
    '?reas': 'áreas',
    '?nico': 'único',
    '?nicos': 'únicos',
    'm?dulo': 'módulo',
    'm?dulos': 'módulos',
    'diagn?stico': 'diagnóstico',
    'Diagn?stico': 'Diagnóstico',
    'cr?tica': 'crítica',
    'Cr?tica': 'Crítica',
    'pedag?gica': 'pedagógica',
    'pedag?gicas': 'pedagógicas',
    'decisi?n': 'decisión',
    'informaci?n': 'información',
    'retroalimentaci?n': 'retroalimentación',
    'Matematicas': 'Matemáticas',
    'Tecnologia e Informatica': 'Tecnología e Informática',
    'Lectura Critica': 'Lectura Crítica',
    'Lectura critica': 'Lectura crítica',
    'Diagnostico inicial': 'Diagnóstico inicial',
    'Competencias pedagogicas': 'Competencias pedagógicas',
    'Pedagogia y didactica': 'Pedagogía y didáctica',
    'Simulacro por area': 'Simulacro por área',
    'Simulacros por area': 'Simulacros por área',
    'Ingles': 'Inglés',
    'Pago unico': 'Pago único',
    'pago unico': 'pago único',
    'Acceso unico': 'Acceso único',
    'acceso unico': 'acceso único',
    'retroalimentacion': 'retroalimentación',
    'Revision tecnica': 'Revisión técnica',
    'revision tecnica': 'revisión técnica',
    'Continuar practica': 'Continuar práctica',
    'Evaluacion': 'Evaluación',
    'evaluacion': 'evaluación',
    'Pedagogia': 'Pedagogía',
    'pedagogia': 'pedagogía',
    'didactica': 'didáctica',
    'Didactica': 'Didáctica',
    'comunicacion': 'comunicación',
    'Comunicacion': 'Comunicación',
    'orientacion': 'orientación',
    'Orientacion': 'Orientación',
    'gestion': 'gestión',
    'Gestion': 'Gestión',
    'Analisis': 'Análisis',
    'analisis': 'análisis',
    'Comprension': 'Comprensión',
    'comprension': 'comprensión',
    'Informacion': 'Información',
    'informacion': 'información',
    'Metacognicion': 'Metacognición',
    'Integracion': 'Integración',
    'integracion': 'integración',
    'Educacion': 'Educación',
    'educacion': 'educación',
}


def repair_encoding(value):
    if not any(marker in value for marker in ("Ã", "Â")):
        return value
    try:
        decoded = value.encode("latin1").decode("utf-8")
    except UnicodeError:
        return value
    return decoded if decoded.count("�") <= value.count("�") else value


class Command(BaseCommand):
    help = 'Corrige textos visibles, codificación y acentos en datos activos sin tocar lógica funcional.'

    def add_arguments(self, parser):
        parser.add_argument('--check-only', action='store_true', help='Solo reporta problemas sin modificar datos.')

    def _reparar_tipo_modulo(self, tipo_corrupto, tipo_canonico):
        corrupta = Modulo.objects.filter(tipo=tipo_corrupto).first()
        if not corrupta:
            return 0

        canonica = Modulo.objects.filter(tipo=tipo_canonico).first()
        if not canonica:
            corrupta.tipo = tipo_canonico
            corrupta.save(update_fields=['tipo'])
            return 1

        # Ya existen las dos filas (canonica creada por seed_modulos /
        # apply_market_ready_upgrade en un deploy anterior a este fix): se
        # conserva la canonica y se reasigna cualquier historial real que
        # dependa de la duplicada antes de borrarla.
        from contenidos.models import Tema
        from seguimiento.models import ProgresoModulo

        # OJO: Tema.orden es la clave logica real que usa
        # seed_modulos.update_or_create(modulo=modulo, orden=topic_order, ...).
        # La canonica ya tiene sus propios Tema (orden 1..N) sembrados en un
        # deploy anterior por seed_modulos, independientes de los de la
        # corrupta. Un `update()` masivo de modulo=corrupta -> modulo=canonica
        # sin revisar 'orden' deja dos filas con el mismo (modulo, orden) en
        # la canonica - eso es exactamente lo que rompe seed_modulos en el
        # SIGUIENTE deploy con MultipleObjectsReturned (causa raiz real del
        # incidente de produccion de julio 2026). Por eso aqui se mueve tema
        # por tema: si la canonica ya tiene ese 'orden', el de la corrupta es
        # un duplicado logico (no historial nuevo) y se descarta; si no, se
        # reasigna de verdad.
        ordenes_en_canonica = set(Tema.objects.filter(modulo=canonica).values_list('orden', flat=True))
        temas_movidos = 0
        temas_descartados = 0
        for tema in Tema.objects.filter(modulo=corrupta).order_by('orden', 'id'):
            if tema.orden in ordenes_en_canonica:
                tema.delete()
                temas_descartados += 1
            else:
                tema.modulo = canonica
                tema.save(update_fields=['modulo'])
                ordenes_en_canonica.add(tema.orden)
                temas_movidos += 1

        progreso_movido = ProgresoModulo.objects.filter(modulo=corrupta).update(modulo=canonica)
        if temas_movidos or temas_descartados or progreso_movido:
            self.stdout.write(
                f'  Fusionando Modulo tipo="{tipo_corrupto}" (id={corrupta.id}) -> '
                f'"{tipo_canonico}" (id={canonica.id}): {temas_movidos} tema(s) reasignados, '
                f'{temas_descartados} tema(s) duplicados descartados, '
                f'{progreso_movido} progreso(s) reasignados.'
            )
        corrupta.delete()
        return 1

    def handle(self, *args, **options):
        check_only = options['check_only']
        scanned = 0
        changed = 0
        suspicious = []

        # Corrige corrupcion ya aplicada por versiones anteriores de este mismo
        # comando: el reemplazo generico de abajo alguna vez toco Modulo.tipo
        # (una clave de codigo con choices fijos, no texto de usuario) y le puso
        # tildes por error (ej. 'analisis_desempeno' -> 'análisis_desempeno'),
        # rompiendo silenciosamente cualquier comparacion `tipo == 'analisis_desempeno'`
        # en el codigo (vistas, TIPOS_CON_ANALISIS, etc.). Fix explicito y de una
        # sola vez para autocurar produccion en el proximo deploy.
        #
        # 'tipo' tiene unique=True: si el deploy anterior ya alcanzo a crear la
        # fila canonica (seed_modulos/apply_market_ready_upgrade) mientras la
        # fila con tilde seguia viva, un UPDATE directo choca contra el UNIQUE.
        # En ese caso se fusiona - se reasigna el historial real (Tema,
        # ProgresoModulo) de la fila con tilde hacia la canonica y se borra la
        # duplicada - en vez de solo renombrar.
        if not check_only:
            corregidas = self._reparar_tipo_modulo('análisis_desempeno', 'analisis_desempeno')
            corregidas += self._reparar_tipo_modulo('gestión_escolar', 'gestion_escolar')
            if corregidas:
                self.stdout.write(self.style.WARNING(f'Corregidas {corregidas} claves Modulo.tipo con tildes indebidas.'))

        for model in TEXT_MODELS:
            fields = [
                field.name
                for field in model._meta.fields
                # Los campos con choices son claves de codigo (tipo, area,
                # estado, respuesta_correcta, etc.), nunca texto libre para
                # el usuario - jamas deben pasar por el reemplazo de acentos.
                # SlugField tampoco: un slug es un identificador tecnico
                # (referenciado por FK y por strings hardcodeados en el
                # codigo - MODULES, MODULE_SLUG_TO_CONTENT_TYPE, etc.), no
                # texto para mostrar. Acentuarlo in-place rompe cualquier
                # comparacion por slug y, peor, choca con el UNIQUE del
                # campo y con la fila canonica que apply_market_ready_upgrade
                # recrea en cada deploy (root cause del bug real: academics.Module
                # duplicado con y sin tildes en el slug tras varios deploys).
                if field.get_internal_type() in {'CharField', 'TextField', 'EmailField'}
                and not field.choices
            ]
            for obj in model.objects.all():
                scanned += 1
                updates = {}
                for field in fields:
                    value = getattr(obj, field, None)
                    if not isinstance(value, str) or not value:
                        continue
                    fixed = repair_encoding(value)
                    for source, target in REPLACEMENTS.items():
                        fixed = fixed.replace(source, target)
                    if fixed != value:
                        updates[field] = fixed
                    if any(marker in fixed for marker in ['�', 'Ã', 'Â']) or any(fragment in fixed for fragment in ['?rea', '?nico', '?tica', '?dulo']):
                        suspicious.append((model.__name__, obj.pk, field, fixed[:120]))
                if updates and not check_only:
                    for field, value in updates.items():
                        setattr(obj, field, value)
                    obj.save(update_fields=list(updates.keys()))
                    changed += 1

        active_questions = BancoPregunta.objects.filter(activa=True)
        duplicate_groups = list(
            active_questions.exclude(hash_contenido='')
            .values('hash_contenido')
            .annotate(total=Count('id'))
            .filter(total__gt=1)
        )
        duplicate_questions = sum(row['total'] for row in duplicate_groups)
        total_questions = active_questions.count()
        missing_feedback = active_questions.filter(justificacion='').count()
        invalid_answer = active_questions.exclude(respuesta_correcta__in=['A', 'B', 'C', 'D']).count()

        self.stdout.write(f'Objetos revisados: {scanned}')
        self.stdout.write(f'Objetos corregidos: {changed}')
        self.stdout.write(f'Preguntas activas: {total_questions}')
        self.stdout.write(f'Preguntas sin justificación: {missing_feedback}')
        self.stdout.write(f'Preguntas con respuesta inválida: {invalid_answer}')
        self.stdout.write(
            f'Preguntas activas con hash_contenido duplicado: {duplicate_questions} '
            f'en {len(duplicate_groups)} grupos'
        )
        if suspicious:
            self.stdout.write(self.style.WARNING(f'Textos sospechosos pendientes: {len(suspicious)}'))
            for item in suspicious[:20]:
                self.stdout.write(self.style.WARNING(str(item)))
        else:
            self.stdout.write(self.style.SUCCESS('Sin textos corruptos visibles detectados.'))
        if missing_feedback or invalid_answer or duplicate_questions:
            # Se reporta como advertencia, no se aborta el build: un problema de
            # contenido (una pregunta sin justificacion, un hash duplicado) no
            # deberia poder bloquear el despliegue de un arreglo de codigo no
            # relacionado (ver build.sh, que usa "set -o errexit").
            self.stdout.write(self.style.WARNING(
                'Hay problemas de calidad de datos pendientes de revisar en el admin (no bloquean el deploy).'
            ))
