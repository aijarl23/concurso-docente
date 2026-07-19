from django.core.management.base import BaseCommand
from django.db import transaction

from banco.models import BancoPregunta, Categoria
from simulacros.models import Simulacro

TJS_CATEGORIA = 'Prueba de Juicio Situacional (PJS)'
SIMULACRO_NOMBRE = 'PJS - Prueba de Juicio Situacional'


class Command(BaseCommand):
    help = (
        'Activa el banco TJS curado (225 items reales, 6 competencias del CNSC) y arma '
        'el simulacro premium mezclado con cobertura de las 6 competencias, retirando '
        'el banco anterior generado por plantilla (categoria "Banco Curado SNCS/CNSC 2026").'
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--per-competencia',
            type=int,
            default=5,
            help='Cuantos items por competencia incluir en el simulacro mezclado (default: 5, total 30).',
        )

    def handle(self, *args, **options):
        per_competencia = options['per_competencia']

        try:
            categoria = Categoria.objects.get(nombre=TJS_CATEGORIA)
        except Categoria.DoesNotExist:
            self.stderr.write(self.style.ERROR(f'No existe la categoria "{TJS_CATEGORIA}".'))
            return

        # Buscar por nombre, no por id: id34 y id35 en local (sqlite) no tienen
        # por que coincidir con el id real en produccion (Postgres), son bases
        # de datos independientes con su propio autoincrement.
        simulacro = (
            Simulacro.objects.filter(nombre=SIMULACRO_NOMBRE, tipo='tjs')
            .order_by('-activo', 'id')
            .first()
        )
        if not simulacro:
            self.stderr.write(self.style.ERROR(f'No se encontro el simulacro TJS premium "{SIMULACRO_NOMBRE}".'))
            return

        with transaction.atomic():
            preguntas_viejas = list(simulacro.preguntas.all())

            activadas = BancoPregunta.objects.filter(categoria=categoria, activa=False).update(activa=True)

            # OJO: no usar .distinct() aqui - el Meta.ordering por defecto de
            # BancoPregunta incluye "id", lo que rompe DISTINCT en values_list()
            # (Django agrega "id" al SELECT para poder ordenar, y cada fila
            # termina siendo "distinta"). Deduplicar en Python en su lugar.
            nombres_competencia = sorted(set(
                BancoPregunta.objects.filter(categoria=categoria)
                .exclude(subcategoria__isnull=True)
                .values_list('subcategoria__nombre', flat=True)
            ))

            seleccionadas = []
            for nombre in nombres_competencia:
                items = list(
                    BancoPregunta.objects.filter(
                        categoria=categoria, subcategoria__nombre=nombre, activa=True
                    ).order_by('id')[:per_competencia]
                )
                seleccionadas.extend(items)

            simulacro.preguntas.set(seleccionadas)
            simulacro.tiempo_limite_minutos = max(
                (len(seleccionadas) * simulacro.tiempo_por_pregunta_segundos) // 60, 1
            )
            simulacro.save(update_fields=['tiempo_limite_minutos'])

            retiradas = 0
            for pregunta in preguntas_viejas:
                if pregunta.categoria_id != categoria.id and pregunta.activa:
                    pregunta.activa = False
                    pregunta.save(update_fields=['activa'])
                    retiradas += 1

        self.stdout.write(self.style.SUCCESS(
            f'Activadas {activadas} preguntas del banco TJS curado (categoria "{TJS_CATEGORIA}").\n'
            f'Competencias encontradas: {len(nombres_competencia)} -> {sorted(nombres_competencia)}\n'
            f'Simulacro id={simulacro.id} reconfigurado con {len(seleccionadas)} preguntas '
            f'({per_competencia} por competencia), tiempo_limite_minutos={simulacro.tiempo_limite_minutos}.\n'
            f'Retiradas (desactivadas) {retiradas} preguntas del banco generado por plantilla.'
        ))
