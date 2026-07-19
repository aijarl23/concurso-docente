from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = (
        'Renombra en sitio (sin crear filas nuevas) los Simulacro existentes que '
        'quedaron con el nombre anterior, luego de institucionalizar la nomenclatura '
        '(ver informe de arquitectura). Preserva id, Intento e historial: es un '
        'rename, no un create+delete. Correr una sola vez; es idempotente (si ya '
        'esta renombrado, no encuentra el nombre viejo y no hace nada).'
    )

    RENOMBRES_SIMULACRO = {
        'Diagnostico inicial - Simulacro premium': 'Evaluación Diagnóstica de Entrada',
        'Lectura critica aplicada - Simulacro premium': 'Componente de Lectura Crítica',
        'Competencias pedagogicas - Simulacro premium': 'Prueba Pedagógica - Enseñanza, Formación y Valoración',
        'Competencias pedagógicas - Simulacro premium': 'Prueba Pedagógica - Enseñanza, Formación y Valoración',
        'Competencias comportamentales / TJS - Simulacro premium': 'PJS - Prueba de Juicio Situacional',
        'Normativa y contexto docente - Simulacro premium': 'Marco Normativo del Ejercicio Docente',
        'Simulacro final tipo concurso - Simulacro premium': 'Simulacro Integral del Concurso',
        'Reporte de progreso y plan de mejora - Simulacro premium': 'Informe de Desempeño y Plan de Fortalecimiento',
    }

    RENOMBRES_CATEGORIA = {
        'Test de Juicios Situacionales (TJS)': 'Prueba de Juicio Situacional (PJS)',
    }

    def handle(self, *args, **options):
        from banco.models import Categoria
        from simulacros.models import Simulacro

        for nombre_viejo, nombre_nuevo in self.RENOMBRES_CATEGORIA.items():
            actualizadas = Categoria.objects.filter(nombre=nombre_viejo).update(nombre=nombre_nuevo)
            if actualizadas:
                self.stdout.write(f'Categoria renombrada: "{nombre_viejo}" -> "{nombre_nuevo}"')

        total = 0
        for nombre_viejo, nombre_nuevo in self.RENOMBRES_SIMULACRO.items():
            if nombre_viejo == nombre_nuevo:
                continue
            afectados = Simulacro.objects.filter(nombre=nombre_viejo)
            count = afectados.count()
            if count == 0:
                continue
            if count > 1:
                self.stdout.write(self.style.WARNING(
                    f'"{nombre_viejo}": {count} filas con ese nombre (deberia ser 1 '
                    f'tras deduplicar_datos) - se renombran todas.'
                ))
            afectados.update(nombre=nombre_nuevo)
            self.stdout.write(f'Renombrado: "{nombre_viejo}" -> "{nombre_nuevo}" ({count} fila(s))')
            total += count

        # El acronimo oficial de la CNSC es PJS (Prueba de Juicio Situacional),
        # no TJS. Cubre nombres auxiliares/inactivos (bancos por competencia,
        # variantes V2) que no estan en el mapa exacto de arriba.
        restantes = Simulacro.objects.filter(nombre__icontains='TJS')
        for s in restantes:
            nuevo = s.nombre.replace('TJS', 'PJS')
            s.nombre = nuevo
            s.save(update_fields=['nombre'])
            self.stdout.write(f'Renombrado (TJS->PJS generico): "{nuevo}"')
            total += 1

        self.stdout.write(self.style.SUCCESS(f'Simulacros renombrados: {total}'))
