from django.core.management.base import BaseCommand, CommandError
from django.db import transaction


class Command(BaseCommand):
    help = (
        'Activa un lote de items del Banco Oficial previamente importado con '
        'importar_lote_oficial (estado=en_revision, activa=False) tras su revision '
        'pedagogica/normativa (Constitucion Cap. 11). Pasa el lote a '
        'estado=publicado, activa=True. No crea, no borra ni reescribe el '
        'contenido de ninguna pregunta - solo cambia su estado de publicacion. '
        'Idempotente: correr dos veces sobre el mismo lote no tiene efecto '
        'adicional. Uso tipico despues de importar_lote_oficial:\n\n'
        '  python manage.py activar_lote_oficial --categoria "Lectura Crítica" '
        '--subcategoria "Inferencia textual"\n\n'
        'Luego de activar, correr sync_banco_simulacros para que el modulo '
        'quede disponible para los estudiantes.'
    )

    def add_arguments(self, parser):
        parser.add_argument('--categoria', default=None, help='Nombre del modulo (Categoria) a activar')
        parser.add_argument(
            '--subcategoria', default=None,
            help='Nombre del subtema (Subcategoria); si se omite, activa todo el modulo indicado'
        )
        parser.add_argument(
            '--all-pending', action='store_true',
            help='Activa TODOS los lotes en_revision de TODAS las categorias (usar solo si ya se revisaron todos)'
        )

    def handle(self, *args, **options):
        from banco.models import BancoPregunta, Categoria

        if options['all_pending']:
            qs = BancoPregunta.objects.filter(estado='en_revision')
        else:
            categoria_nombre = options['categoria']
            if not categoria_nombre:
                raise CommandError('Especifica --categoria "Nombre del modulo" o usa --all-pending')
            try:
                categoria = Categoria.objects.get(nombre=categoria_nombre)
            except Categoria.DoesNotExist:
                disponibles = ', '.join(Categoria.objects.values_list('nombre', flat=True)) or '(ninguna)'
                raise CommandError(f'No existe la Categoria "{categoria_nombre}". Disponibles: {disponibles}')
            qs = BancoPregunta.objects.filter(estado='en_revision', categoria=categoria)
            if options['subcategoria']:
                qs = qs.filter(subcategoria__nombre=options['subcategoria'])

        total = qs.count()
        if total == 0:
            self.stdout.write('No hay items en_revision que coincidan con el filtro. Nada que activar.')
            return

        with transaction.atomic():
            actualizados = qs.update(estado='publicado', activa=True)

        self.stdout.write(self.style.SUCCESS(
            f'Activados {actualizados} item(s) del Banco Oficial. '
            f'Corre "python manage.py sync_banco_simulacros" para conectarlos a sus simulacros.'
        ))
