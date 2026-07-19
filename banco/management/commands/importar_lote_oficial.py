import hashlib
import importlib.util
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction


class Command(BaseCommand):
    help = (
        'Importa un lote de items del Banco Oficial (Blueprint del Banco de Items) '
        'desde un archivo .py con una lista ITEMS. Cada item queda con '
        'estado="en_revision" y activa=False - no llega a ningun usuario hasta '
        'que se confirme la revision pedagogica/normativa final (Constitucion '
        'Cap. 11) y se active explicitamente con activar_lote_oficial.'
    )

    def add_arguments(self, parser):
        parser.add_argument('archivo', help='Ruta al archivo .py del lote (con variable ITEMS)')
        parser.add_argument('--categoria', required=True, help='Nombre del modulo (Categoria)')
        parser.add_argument('--subcategoria', required=True, help='Nombre del subtema (Subcategoria)')
        parser.add_argument('--competencia', required=True)
        parser.add_argument('--area', default='general')

    def handle(self, *args, **options):
        from banco.models import BancoPregunta, Categoria, Subcategoria

        ruta = Path(options['archivo'])
        if not ruta.exists():
            raise CommandError(f'No existe el archivo: {ruta}')

        spec = importlib.util.spec_from_file_location('lote_module', ruta)
        modulo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(modulo)
        items = modulo.ITEMS

        categoria, _ = Categoria.objects.get_or_create(nombre=options['categoria'])
        subcategoria = Subcategoria.objects.filter(
            categoria=categoria, nombre=options['subcategoria']
        ).order_by('id').first()
        if subcategoria is None:
            subcategoria = Subcategoria.objects.create(
                categoria=categoria, nombre=options['subcategoria']
            )

        creadas = 0
        actualizadas = 0
        with transaction.atomic():
            for item in items:
                raw = f"{categoria.nombre}|{item['contexto']}|{item['enunciado']}|{item['respuesta_correcta']}"
                hash_contenido = hashlib.sha256(raw.encode('utf-8')).hexdigest()[:40]

                pregunta, creada = BancoPregunta.objects.update_or_create(
                    titulo=item['codigo'],
                    defaults={
                        'categoria': categoria,
                        'subcategoria': subcategoria,
                        'competencia': options['competencia'],
                        'area': options['area'],
                        'contexto': item['contexto'],
                        'enunciado': item['enunciado'],
                        'opcion_a': item['opcion_a'],
                        'opcion_b': item['opcion_b'],
                        'opcion_c': item['opcion_c'],
                        'opcion_d': item['opcion_d'],
                        'respuesta_correcta': item['respuesta_correcta'],
                        'tipo_item': item.get('tipo_item', 'estandar'),
                        'idoneidad_a': item.get('idoneidad', {}).get('a') if item.get('idoneidad') else None,
                        'idoneidad_b': item.get('idoneidad', {}).get('b') if item.get('idoneidad') else None,
                        'idoneidad_c': item.get('idoneidad', {}).get('c') if item.get('idoneidad') else None,
                        'idoneidad_d': item.get('idoneidad', {}).get('d') if item.get('idoneidad') else None,
                        'justificacion': item['justificacion'],
                        'fuente_normativa': item.get('fuente_normativa', ''),
                        'dificultad': item['nivel_dificultad'],
                        'nivel_dificultad': item['nivel_dificultad'],
                        'proceso_cognitivo': item.get('proceso_cognitivo', ''),
                        'hash_contenido': hash_contenido,
                        'autor': 'IA',
                        'estado': 'en_revision',
                        'activa': False,
                    },
                )
                creadas += int(creada)
                actualizadas += int(not creada)

        self.stdout.write(self.style.SUCCESS(
            f'Lote importado desde {ruta.name}: {creadas} creadas, {actualizadas} actualizadas. '
            f'Estado: en_revision, activa=False. Modulo: {categoria.nombre} / {subcategoria.nombre}.'
        ))
