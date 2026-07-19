from django.core.management.base import BaseCommand
from django.db import transaction


class Command(BaseCommand):
    help = (
        'Reconstruccion total del banco de contenido, a peticion explicita del '
        'usuario: borra de forma DEFINITIVA (no reversible) todas las preguntas, '
        'opciones, justificaciones y categorias existentes. Tambien elimina los '
        'simulacros auxiliares obsoletos ligados al banco TJS/PJS descartado '
        '(bancos por competencia, banco completo, variante V2), que ya estaban '
        'inactivos y sin uso real por ningun usuario. '
        'NO borra Simulacro.objects (los 8-9 simulacros principales sobreviven, '
        'quedan vacios e inactivos hasta que se reescriba cada uno con contenido '
        'nuevo) ni Intento/RespuestaIntento directamente - el resultado general '
        '(puntaje, fecha) de intentos pasados se conserva; solo se pierde el '
        'detalle pregunta-por-pregunta via cascada desde BancoPregunta.'
    )

    # Simulacros auxiliares del banco TJS/PJS descartado: siempre estuvieron
    # inactivos (nunca alcanzables por un usuario real vía la interfaz), no
    # tienen proposito sin el banco de origen que se esta borrando.
    NOMBRES_SIMULACRO_A_BORRAR = [
        'PJS - Comunicación asertiva - 15 preguntas',
        'PJS - Comunicación asertiva - 30 preguntas',
        'PJS - Iniciativa - 15 preguntas',
        'PJS - Iniciativa - 30 preguntas',
        'PJS - Liderazgo - 15 preguntas',
        'PJS - Liderazgo - 30 preguntas',
        'PJS - Manejo de la información - 15 preguntas',
        'PJS - Manejo de la información - 30 preguntas',
        'PJS - Orientación al logro - 15 preguntas',
        'PJS - Orientación al logro - 30 preguntas',
        'PJS - Trabajo en equipo - 15 preguntas',
        'PJS - Trabajo en equipo - 30 preguntas',
        'PJS Concurso Docente CNSC - Banco completo 90 preguntas',
        'Competencias comportamentales / PJS - Simulacro premium V2',
        'Simulacros por área - Simulacro premium',
        'Simulacros por área - Simulacro premium V2',
    ]

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirmar', action='store_true',
            help='Requerido para ejecutar de verdad. Sin esta bandera, solo reporta que borraria.',
        )

    def handle(self, *args, **options):
        from banco.models import BancoPregunta, Categoria
        from seguimiento.models import Intento
        from simulacros.models import Simulacro

        confirmar = options['confirmar']

        total_preguntas = BancoPregunta.objects.count()
        total_categorias = Categoria.objects.count()

        auxiliares = Simulacro.objects.filter(nombre__in=self.NOMBRES_SIMULACRO_A_BORRAR)
        con_historial = []
        for sim in auxiliares:
            n = Intento.objects.filter(simulacro=sim).count()
            if n:
                con_historial.append((sim.nombre, n))

        self.stdout.write(f'Preguntas a borrar: {total_preguntas}')
        self.stdout.write(f'Categorias a borrar: {total_categorias}')
        self.stdout.write(f'Simulacros auxiliares a borrar: {auxiliares.count()}')
        if con_historial:
            self.stdout.write(self.style.WARNING(
                f'ADVERTENCIA: {len(con_historial)} de esos simulacros auxiliares SI tienen '
                f'intentos registrados (no deberian, estaban inactivos): {con_historial}'
            ))

        if not confirmar:
            self.stdout.write(self.style.WARNING(
                'Modo simulacion (sin --confirmar). No se borro nada. '
                'Vuelve a correr con --confirmar para ejecutar de verdad.'
            ))
            return

        with transaction.atomic():
            borradas_preguntas = BancoPregunta.objects.all().delete()
            borradas_categorias = Categoria.objects.all().delete()
            borrados_auxiliares = auxiliares.delete()

            # Los simulacros principales sobreviven pero ya no tienen preguntas:
            # se marcan inactivos hasta que se reescriban con contenido nuevo.
            desactivados = 0
            for sim in Simulacro.objects.filter(activo=True):
                if not sim.preguntas.filter(activa=True).exists():
                    sim.activo = False
                    sim.save(update_fields=['activo'])
                    desactivados += 1

        self.stdout.write(self.style.SUCCESS(
            f'Borrado definitivo completado. Preguntas: {borradas_preguntas[0]}. '
            f'Categorias: {borradas_categorias[0]}. Simulacros auxiliares: {borrados_auxiliares[0]}. '
            f'Simulacros principales desactivados (sin contenido): {desactivados}.'
        ))
