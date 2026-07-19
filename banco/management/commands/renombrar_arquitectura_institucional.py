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
        # Cada nombre viejo se mapea con y sin tildes: repair_text_quality ya
        # habia corregido acentos en algunas filas en deploys anteriores, y
        # otras seguian sin corregir - sin las dos variantes, el filtro por
        # nombre exacto no encuentra la fila y queda huerfana (paso con
        # "Diagnostico" y "Lectura critica" en el primer intento de este rename).
        'Diagnostico inicial - Simulacro premium': 'Diagnóstico Inicial',
        'Diagnóstico inicial - Simulacro premium': 'Diagnóstico Inicial',
        'Lectura critica aplicada - Simulacro premium': 'Lectura Crítica',
        'Lectura crítica aplicada - Simulacro premium': 'Lectura Crítica',
        'Competencias pedagogicas - Simulacro premium': 'Competencias Pedagógicas',
        'Competencias pedagógicas - Simulacro premium': 'Competencias Pedagógicas',
        'Competencias comportamentales / TJS - Simulacro premium': 'Análisis de Casos',
        'PJS - Prueba de Juicio Situacional': 'Análisis de Casos',
        'Normativa y contexto docente - Simulacro premium': 'Normatividad Educativa',
        'Simulacro final tipo concurso - Simulacro premium': 'Simulacro Integral',
        'Reporte de progreso y plan de mejora - Simulacro premium': 'Análisis del Desempeño',
        # Segunda ronda: nombres institucionales largos (primera version del
        # rename, ya aplicados en produccion) -> version definitiva de maximo
        # 3 palabras, pedida explicitamente por el usuario.
        'Evaluación Diagnóstica de Entrada': 'Diagnóstico Inicial',
        'Componente de Lectura Crítica': 'Lectura Crítica',
        'Prueba Pedagógica - Enseñanza, Formación y Valoración': 'Competencias Pedagógicas',
        'Marco Normativo del Ejercicio Docente': 'Normatividad Educativa',
        'Componente Disciplinar por Área de Conocimiento': 'Competencias Disciplinares',
        'Simulacro Integral del Concurso': 'Simulacro Integral',
        'Informe de Desempeño y Plan de Fortalecimiento': 'Análisis del Desempeño',
    }

    RENOMBRES_CATEGORIA = {}

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

        self.stdout.write(self.style.SUCCESS(f'Simulacros renombrados: {total}'))
