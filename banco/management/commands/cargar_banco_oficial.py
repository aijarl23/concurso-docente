import hashlib
import importlib.util
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

LOTES_DIR = Path(settings.BASE_DIR) / '_resources' / 'banco_oficial'


class Command(BaseCommand):
    help = (
        'Descubre automaticamente todos los lotes de items del Banco Oficial en '
        '_resources/banco_oficial/*.py (cualquier archivo .py que defina ITEMS, '
        'CATEGORIA, SUBCATEGORIA, COMPETENCIA y AREA) y los importa + activa en '
        'un solo paso: equivale a correr importar_lote_oficial seguido de '
        'activar_lote_oficial para cada lote encontrado.\n\n'
        'Pensado para que agregar un nuevo tema al Banco Oficial de Preguntas '
        '(comite CNSC) no requiera tocar build.sh ni ningun otro archivo de '
        'plataforma: basta con dejar el nuevo archivo .py del lote en '
        '_resources/banco_oficial/ y hacer commit. Idempotente (update_or_create '
        'por codigo + activacion idempotente) - correr de nuevo sobre lotes ya '
        'cargados no tiene efecto adicional. Ignora archivos .py sin ITEMS '
        '(scripts auxiliares u otros lotes en formato distinto).\n\n'
        'Correr despues de seed_modulos/apply_market_ready_upgrade y antes de '
        'sync_banco_simulacros; forma parte del pipeline automatico de build.sh.'
    )

    def handle(self, *args, **options):
        from banco.models import BancoPregunta, Categoria, Subcategoria

        if not LOTES_DIR.is_dir():
            self.stdout.write('No existe _resources/banco_oficial/; nada que cargar.')
            return

        total_creadas = 0
        total_actualizadas = 0
        total_activadas = 0
        lotes_procesados = 0

        for ruta in sorted(LOTES_DIR.glob('*.py')):
            spec = importlib.util.spec_from_file_location(f'lote_{ruta.stem}', ruta)
            modulo = importlib.util.module_from_spec(spec)
            try:
                spec.loader.exec_module(modulo)
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'  [omitido] {ruta.name}: error al cargar ({e})'))
                continue

            items = getattr(modulo, 'ITEMS', None)
            if items is None:
                continue  # script auxiliar sin lote (ej. reconstruccion_total_banco)

            categoria_nombre = getattr(modulo, 'CATEGORIA', None)
            subcategoria_nombre = getattr(modulo, 'SUBCATEGORIA', None)
            competencia = getattr(modulo, 'COMPETENCIA', None)
            area = getattr(modulo, 'AREA', 'general')
            if not (categoria_nombre and subcategoria_nombre and competencia):
                self.stdout.write(self.style.WARNING(
                    f'  [omitido] {ruta.name}: define ITEMS pero le falta CATEGORIA/SUBCATEGORIA/COMPETENCIA'
                ))
                continue

            lotes_procesados += 1
            categoria, _ = Categoria.objects.get_or_create(nombre=categoria_nombre)
            subcategoria = Subcategoria.objects.filter(
                categoria=categoria, nombre=subcategoria_nombre
            ).order_by('id').first()
            if subcategoria is None:
                subcategoria = Subcategoria.objects.create(
                    categoria=categoria, nombre=subcategoria_nombre
                )

            creadas = 0
            actualizadas = 0
            with transaction.atomic():
                for item in items:
                    raw = f"{categoria.nombre}|{item['contexto']}|{item['enunciado']}|{item['respuesta_correcta']}"
                    hash_contenido = hashlib.sha256(raw.encode('utf-8')).hexdigest()[:40]

                    _, creada = BancoPregunta.objects.update_or_create(
                        titulo=item['codigo'],
                        defaults={
                            'categoria': categoria,
                            'subcategoria': subcategoria,
                            'competencia': competencia,
                            'area': area,
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
                            'estado': 'publicado',
                            'activa': True,
                            'es_premium': False,
                        },
                    )
                    creadas += int(creada)
                    actualizadas += int(not creada)

            total_creadas += creadas
            total_actualizadas += actualizadas
            total_activadas += creadas + actualizadas
            self.stdout.write(
                f'  {ruta.name}: {creadas} creada(s), {actualizadas} actualizada(s) '
                f'-> {categoria_nombre} / {subcategoria_nombre} (competencia="{competencia}")'
            )

        self.stdout.write(self.style.SUCCESS(
            f'Banco Oficial: {lotes_procesados} lote(s) procesados, '
            f'{total_creadas} pregunta(s) nueva(s), {total_actualizadas} actualizada(s), '
            f'{total_activadas} publicada(s) y activa(s). '
            f'Corre "python manage.py sync_banco_simulacros" para conectarlas a sus simulacros.'
        ))
