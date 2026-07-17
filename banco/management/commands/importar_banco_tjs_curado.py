import json
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

from banco.models import BancoPregunta, Categoria, Subcategoria
from simulacros.models import Simulacro

BANK_PATH = Path(settings.BASE_DIR) / '_resources' / 'tjs_import' / 'tjs_bank_final.json'
CATEGORY_NAME = 'Test de Juicios Situacionales (TJS)'
FULL_SIM_NAME = 'TJS Concurso Docente CNSC - Banco completo 90 preguntas'


def normalize_title(item: dict) -> str:
    return f"{item['codigo']} - {item['competencia']}"


def tipo_item_de(item: dict) -> str:
    tipo = (item.get('tipo_item') or '').upper()
    if 'MENOS' in tipo:
        return 'menos_adecuada'
    return 'mas_adecuada'


class Command(BaseCommand):
    help = (
        'Importa el banco TJS curado (225 items reales, 6 competencias del CNSC) desde '
        '_resources/tjs_import/tjs_bank_final.json. Idempotente (update_or_create por '
        'titulo), seguro de correr en cada deploy. Reemplaza al script suelto '
        'scripts/data_import/import_tjs_bank.py, que nunca corrio contra produccion '
        '(solo se ejecuto localmente de forma manual, por eso el banco nunca llego a Postgres).'
    )

    def handle(self, *args, **options):
        if not BANK_PATH.exists():
            self.stderr.write(self.style.ERROR(f'No existe el archivo fuente: {BANK_PATH}'))
            return

        payload = json.loads(BANK_PATH.read_text(encoding='utf-8'))

        with transaction.atomic():
            category, _ = Categoria.objects.get_or_create(nombre=CATEGORY_NAME)

            subcategories = {}
            for name in payload['counts'].keys():
                # No usar get_or_create: ya existen subcategorias duplicadas con
                # el mismo nombre (de corridas anteriores del script suelto), y
                # get_or_create truena con MultipleObjectsReturned si hay mas de
                # una. Tomar la primera existente en vez de fallar.
                subcat = Subcategoria.objects.filter(categoria=category, nombre=name).order_by('id').first()
                if not subcat:
                    subcat = Subcategoria.objects.create(categoria=category, nombre=name)
                subcategories[name] = subcat

            created = 0
            updated = 0
            questions_by_competency = {name: [] for name in payload['counts'].keys()}
            all_questions = []

            for item in payload['questions']:
                idoneidad = item.get('idoneidad') or {}
                question, was_created = BancoPregunta.objects.update_or_create(
                    titulo=normalize_title(item),
                    defaults={
                        'categoria': category,
                        'subcategoria': subcategories[item['competencia']],
                        'contexto': item['contexto'],
                        'enunciado': item['enunciado'],
                        'opcion_a': item['opcion_a'],
                        'opcion_b': item['opcion_b'],
                        'opcion_c': item['opcion_c'],
                        'opcion_d': item['opcion_d'],
                        'respuesta_correcta': item['respuesta_correcta'],
                        'tipo_item': tipo_item_de(item),
                        'idoneidad_a': idoneidad.get('a'),
                        'idoneidad_b': idoneidad.get('b'),
                        'idoneidad_c': idoneidad.get('c'),
                        'idoneidad_d': idoneidad.get('d'),
                        'justificacion': item['justificacion'],
                        'fuente_normativa': 'CNSC - Competencias comportamentales docentes / Test de Juicios Situacionales',
                        'dificultad': 'elite',
                        'activa': True,
                    },
                )
                created += int(was_created)
                updated += int(not was_created)
                questions_by_competency[item['competencia']].append(question)
                all_questions.append(question)

            full, _ = Simulacro.objects.update_or_create(
                nombre=FULL_SIM_NAME,
                defaults={
                    'descripcion': (
                        'Banco completo y balanceado de Test de Juicios Situacionales para '
                        'Concurso Docente CNSC. Incluye 15 items por competencia comportamental.'
                    ),
                    'tipo': 'simulacro',
                    'tiempo_limite_minutos': 180,
                    'puntaje_minimo_aprobacion': 70,
                    'activo': False,
                },
            )
            full.preguntas.set(all_questions)

            for competency, questions in sorted(questions_by_competency.items()):
                sim, _ = Simulacro.objects.update_or_create(
                    nombre=f'TJS - {competency} - 15 preguntas',
                    defaults={
                        'descripcion': f'Seccion TJS de nivel avanzado enfocada en {competency}.',
                        'tipo': 'simulacro',
                        'tiempo_limite_minutos': 35,
                        'puntaje_minimo_aprobacion': 70,
                        'activo': False,
                    },
                )
                sim.preguntas.set(questions)

        self.stdout.write(self.style.SUCCESS(
            f'Banco TJS curado importado: {created} creadas, {updated} actualizadas, '
            f'{len(all_questions)} total en categoria "{CATEGORY_NAME}".'
        ))
