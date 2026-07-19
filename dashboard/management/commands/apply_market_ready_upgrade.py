from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction

from academics.models import Category, Module
from commerce.models import Product
from contenidos.models import Modulo, Tema
from dashboard.question_generator import ELITE_SLUG, MODULES

FULL_ACCESS_PRICE = Decimal('20000')


class Command(BaseCommand):
    help = (
        'Sincroniza la estructura del catalogo (categoria, modulos de contenido, '
        'productos y precios) a partir de MODULES en dashboard/question_generator.py. '
        'NO genera ni toca preguntas del banco - eso es responsabilidad de un '
        'comando de importacion dedicado por cada modulo, escrito cuando ese '
        'modulo tenga contenido nuevo y validado.'
    )

    @transaction.atomic
    def handle(self, *args, **options):
        category, _ = Category.objects.update_or_create(
            slug='ruta-premium-cnsc-2026',
            defaults={
                'name': 'Programa de Preparación Concurso Docente CNSC',
                'category_type': 'simulacros',
                'description': 'Ruta integral con diagnóstico, componentes, simulacros, retroalimentación y plan de fortalecimiento.',
                'icon': 'bi-stars',
                'order': 1,
                'active': True,
            },
        )

        valid_module_slugs = [module['slug'] for module in MODULES] + [ELITE_SLUG]
        Modulo.objects.exclude(tipo__in=[module['tipo'] for module in MODULES]).update(activo=False)
        Product.objects.exclude(module__slug__in=valid_module_slugs).update(active=False)

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
                        'descripcion': f'Entrenamiento aplicado en {topic.lower()}.',
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

        elite, _ = Module.objects.update_or_create(
            slug=ELITE_SLUG,
            defaults={
                'category': category,
                'title': 'Programa Integral de Preparación CNSC',
                'short_description': 'Matrícula única a todos los componentes, simulacros y retroalimentación.',
                'description': 'Incluye diagnóstico, lectura crítica, componentes pedagógicos, análisis de casos, marco normativo, componente disciplinar, simulacro integral e informe de desempeño.',
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

        self.stdout.write(self.style.SUCCESS(
            f'Catalogo sincronizado: {len(MODULES)} modulos, pago único COP {FULL_ACCESS_PRICE}. '
            f'El banco de preguntas se administra por separado, modulo por modulo.'
        ))
