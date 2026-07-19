from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = (
        'Desactiva todo el contenido generico/plantillado del banco (categoria '
        '"Banco Curado SNCS/CNSC 2026" y similares), dejando activo unicamente '
        'el banco PJS ya auditado y validado. No borra filas -> reversible, no '
        'rompe el historial de Intento/RespuestaIntento de usuarios existentes. '
        'Es el punto de partida limpio para reescribir cada modulo con el mismo '
        'rigor que ya se aplico a PJS.'
    )

    PRESERVAR_CATEGORIA = 'Prueba de Juicio Situacional (PJS)'

    def handle(self, *args, **options):
        from banco.models import BancoPregunta
        from simulacros.models import Simulacro

        desactivadas = (
            BancoPregunta.objects.filter(activa=True)
            .exclude(categoria__nombre=self.PRESERVAR_CATEGORIA)
            .update(activa=False)
        )

        # Sin esto, los simulacros que dependian de ese banco quedarian
        # visibles como "disponibles" pero con 0 preguntas -> peor
        # experiencia que si no aparecieran. Se desactivan tambien,
        # excepto los que ya tengan preguntas PJS activas.
        simulacros_vacios = 0
        for sim in Simulacro.objects.filter(activo=True):
            if not sim.preguntas.filter(activa=True).exists():
                sim.activo = False
                sim.save(update_fields=['activo'])
                simulacros_vacios += 1

        self.stdout.write(self.style.SUCCESS(
            f'Desactivadas {desactivadas} preguntas fuera de "{self.PRESERVAR_CATEGORIA}". '
            f'Desactivados {simulacros_vacios} simulacros que quedaron sin preguntas activas. '
            f'El banco activo ahora es unicamente PJS, mientras se reescribe el resto '
            f'modulo por modulo.'
        ))
