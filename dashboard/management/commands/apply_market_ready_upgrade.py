
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction

from academics.models import Category, Module
from banco.models import BancoPregunta, Categoria, Subcategoria
from commerce.models import Product
from contenidos.models import Modulo, Tema
from dashboard.question_generator import (
    AREA_MODULE_SLUG,
    AREA_SIMULACROS,
    ELITE_SLUG,
    MODULES,
    QUESTION_CATEGORY,
    GenerationRegistry,
    generate_question_set,
)
from simulacros.models import Simulacro

FULL_ACCESS_PRICE = Decimal('20000')


class Command(BaseCommand):
    help = 'Regenera la plataforma premium con pago ?nico y banco SNCS validado contra duplicados.'

    @transaction.atomic
    def handle(self, *args, **options):
        category, _ = Category.objects.update_or_create(
            slug='ruta-premium-cnsc-2026',
            defaults={
                'name': 'Ruta Premium Concurso Docente SNCS 2026',
                'category_type': 'simulacros',
                'description': 'Ruta integral con diagn?stico, competencias, simulacros, retroalimentaci?n y plan de mejora.',
                'icon': 'bi-stars',
                'order': 1,
                'active': True,
            },
        )
        banco_cat, _ = Categoria.objects.get_or_create(nombre=QUESTION_CATEGORY)
        BancoPregunta.objects.update(activa=False)

        valid_module_slugs = [module['slug'] for module in MODULES] + [ELITE_SLUG]
        Modulo.objects.exclude(tipo__in=[module['tipo'] for module in MODULES]).update(activo=False)
        Product.objects.exclude(module__slug__in=valid_module_slugs).update(active=False)

        registry = GenerationRegistry()
        total_questions = 0
        active_sim_names = []

        for order, data in enumerate(MODULES, 1):
            content_module, _ = Modulo.objects.update_or_create(
                tipo=data['tipo'],
                defaults={
                    'titulo': data['title'],
                    'descripcion': data['description'],
                    'orden': order,
                    'activo': True,
                },
            )
            Tema.objects.filter(modulo=content_module).update(activo=False)
            for topic_order, topic in enumerate(data['topics'], 1):
                Tema.objects.update_or_create(
                    modulo=content_module,
                    orden=topic_order,
                    defaults={
                        'titulo': topic,
                        'descripcion': f'Entrenamiento aplicado en {topic.lower()} con casos tipo SNCS.',
                        'activo': True,
                    },
                )

            module, _ = Module.objects.update_or_create(
                slug=data['slug'],
                defaults={
                    'category': category,
                    'title': data['title'],
                    'short_description': data['description'][:300],
                    'description': data['description'],
                    'difficulty_level': 'sncs_expert',
                    'estimated_time_minutes': 90,
                    'is_active': True,
                    'is_premium': True,
                },
            )
            Product.objects.update_or_create(
                module=module,
                defaults={'price': FULL_ACCESS_PRICE, 'sale_price': FULL_ACCESS_PRICE, 'active': False},
            )

            if data['slug'] == AREA_MODULE_SLUG:
                continue

            questions = self._build_questions_for_module(banco_cat, data, registry)
            total_questions += len(questions)
            sim_name = f'{data["title"]} - Simulacro premium'
            simulacro, _ = Simulacro.objects.update_or_create(
                nombre=sim_name,
                defaults={
                    'descripcion': data['description'],
                    'tipo': data['tipo_sim'],
                    'module': module,
                    'area': data['area'],
                    'tiempo_limite_minutos': 90,
                    'tiempo_por_pregunta_segundos': 180,
                    'puntaje_minimo_aprobacion': 70,
                    'es_premium': True,
                    'paquete_codigo': ELITE_SLUG,
                    'activo': True,
                },
            )
            simulacro.preguntas.set(questions)
            active_sim_names.append(sim_name)

        area_module_data = next(module for module in MODULES if module['slug'] == AREA_MODULE_SLUG)
        area_module = Module.objects.get(slug=AREA_MODULE_SLUG)
        for area_data in AREA_SIMULACROS:
            module_data = {
                **area_module_data,
                'title': f'Simulacro por ?rea - {area_data["label"]}',
                'area': area_data['area'],
                'competencia': area_data['competencia'],
                'description': f'Banco disciplinar para {area_data["label"]} con lectura cr?tica, datos, problemas contextualizados y decisi?n pedag?gica.',
            }
            questions = self._build_questions_for_module(banco_cat, module_data, registry)
            total_questions += len(questions)
            sim_name = f'Simulacro por ?rea - {area_data["label"]}'
            simulacro, _ = Simulacro.objects.update_or_create(
                nombre=sim_name,
                defaults={
                    'descripcion': module_data['description'],
                    'tipo': 'area',
                    'module': area_module,
                    'area': area_data['area'],
                    'tiempo_limite_minutos': 90,
                    'tiempo_por_pregunta_segundos': 180,
                    'puntaje_minimo_aprobacion': 70,
                    'es_premium': True,
                    'paquete_codigo': ELITE_SLUG,
                    'activo': True,
                },
            )
            simulacro.preguntas.set(questions)
            active_sim_names.append(sim_name)

        elite, _ = Module.objects.update_or_create(
            slug=ELITE_SLUG,
            defaults={
                'category': category,
                'title': 'Acceso completo ConcursoDocente SNCS 2026',
                'short_description': 'Acceso completo a todos los m?dulos, simulacros y retroalimentaciones por un pago ?nico.',
                'description': 'Incluye diagn?stico, lectura cr?tica, competencias pedag?gicas, TJS, normativa, ?reas, simulacro final y plan de mejora.',
                'difficulty_level': 'sncs_expert',
                'estimated_time_minutes': 480,
                'is_active': True,
                'is_premium': True,
            },
        )
        Product.objects.update_or_create(
            module=elite,
            defaults={'price': FULL_ACCESS_PRICE, 'sale_price': FULL_ACCESS_PRICE, 'active': True},
        )
        Product.objects.filter(module__slug__in=[module['slug'] for module in MODULES]).update(
            active=False,
            price=FULL_ACCESS_PRICE,
            sale_price=FULL_ACCESS_PRICE,
        )
        Product.objects.exclude(module__slug__in=valid_module_slugs).update(active=False)
        Simulacro.objects.exclude(nombre__in=active_sim_names).update(activo=False)

        self.stdout.write(self.style.SUCCESS(
            f'Plataforma actualizada: pago ?nico COP 20.000, {len(active_sim_names)} simulacros, '
            f'{total_questions} preguntas SNCS validadas y {len(registry.hashes)} hashes ?nicos.'
        ))

    def _build_questions_for_module(self, banco_cat, data, registry):
        subcat, _ = Subcategoria.objects.get_or_create(categoria=banco_cat, nombre=data['title'])
        questions = []
        for item in generate_question_set(data, registry=registry):
            pregunta, _ = BancoPregunta.objects.update_or_create(
                titulo=item.id,
                defaults={
                    'categoria': banco_cat,
                    'subcategoria': subcat,
                    'contexto': item.contexto,
                    'enunciado': item.enunciado,
                    'opcion_a': item.opciones['A'],
                    'opcion_b': item.opciones['B'],
                    'opcion_c': item.opciones['C'],
                    'opcion_d': item.opciones['D'],
                    'respuesta_correcta': item.respuesta_correcta,
                    'justificacion': item.explicacion,
                    'fuente_normativa': f'SNCS/ICFES calibrado con simulacros de referencia; subtema={item.subtema}; hash={item.hash_contenido}',
                    'dificultad': item.nivel_dificultad,
                    'nivel_dificultad': item.nivel_dificultad,
                    'hash_contenido': item.hash_contenido,
                    'area': item.area,
                    'competencia': item.competencia,
                    'tiempo_limite_segundos': 180,
                    'es_premium': True,
                    'activa': True,
                },
            )
            questions.append(pregunta)
        return questions
