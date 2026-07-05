from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils.text import slugify

from academics.models import Category, Module
from banco.models import BancoPregunta, Categoria, Subcategoria
from commerce.models import Product
from simulacros.models import Simulacro


AREA_LABELS = {
    'ingles': 'Ingles',
    'tecnologia': 'Tecnologia e Informatica',
    'matematicas': 'Matematicas',
    'ciencias_naturales': 'Ciencias Naturales',
    'ciencias_sociales': 'Ciencias Sociales',
}

TJS_COMPETENCIAS = [
    'Comunicacion asertiva',
    'Iniciativa',
    'Liderazgo',
    'Manejo de la informacion',
    'Orientacion al logro',
    'Trabajo en equipo',
]


class Command(BaseCommand):
    help = 'Carga estructura premium CNSC 2026: productos, simulacros por area y banco minimo de 30 preguntas por tema.'

    def handle(self, *args, **options):
        category, _ = Category.objects.get_or_create(
            slug='simulacros-premium',
            defaults={
                'name': 'Simulacros Premium CNSC 2026',
                'category_type': 'simulacros',
                'description': 'Banco premium con simulacros TJS y pruebas por area.',
                'order': 10,
                'active': True,
            }
        )
        elite_module = self._module(category, 'Paquete Elite CNSC 2026', 'elite-cnsc-2026', 'Acceso completo a todos los simulacros premium y por area.')
        Product.objects.update_or_create(
            module=elite_module,
            defaults={'price': Decimal('199000'), 'sale_price': Decimal('149000'), 'active': True}
        )

        self._complete_tjs(category)
        self._create_area_banks(category)
        self.stdout.write(self.style.SUCCESS('Carga premium CNSC 2026 finalizada.'))

    def _module(self, category, title, slug, description):
        module, _ = Module.objects.update_or_create(
            slug=slug,
            defaults={
                'category': category,
                'title': title,
                'short_description': description[:300],
                'description': description,
                'difficulty_level': 'cnsc_expert',
                'estimated_time_minutes': 90,
                'is_active': True,
                'is_premium': True,
            }
        )
        return module

    def _contexto(self, tema, i):
        return (
            f'En una institucion educativa oficial se analiza una situacion relacionada con {tema}.\n'
            'El equipo docente cuenta con informacion parcial, presiones de tiempo y expectativas diversas de familias, estudiantes y directivos.\n'
            'Durante la reunion, algunos participantes proponen actuar de inmediato para mostrar resultados visibles ante la comunidad.\n'
            'Otros advierten que una decision apresurada puede desconocer evidencias pedagogicas, criterios de inclusion y responsabilidades institucionales.\n'
            'La coordinacion solicita una respuesta que combine lectura del contexto, uso responsable de la informacion y comunicacion profesional.\n'
            'Tambien recuerda que las decisiones deben ser trazables, proporcionales y coherentes con el mejoramiento de los aprendizajes.\n'
            f'El caso {i} exige valorar no solo la accion inmediata, sino sus efectos eticos, pedagogicos y organizacionales.'
        )

    def _make_question(self, categoria, subcategoria, area, competencia, i):
        contexto = self._contexto(competencia or area, i)
        pregunta, created = BancoPregunta.objects.get_or_create(
            titulo=f'{competencia or area} premium {i}',
            defaults={
                'categoria': categoria,
                'subcategoria': subcategoria,
                'contexto': contexto,
                'enunciado': 'A partir del texto, cual alternativa representa la decision mas pertinente, considerando razonamiento critico, responsabilidad docente y uso adecuado de evidencias?',
                'opcion_a': 'Actuar de forma inmediata para disminuir la presion externa, aunque todavia no se haya contrastado la informacion disponible.',
                'opcion_b': 'Aplazar indefinidamente la decision hasta que exista consenso total, aun si esto impide proteger oportunamente el proceso formativo.',
                'opcion_c': 'Analizar la evidencia disponible, escuchar a los actores implicados, documentar la decision y comunicar una accion proporcional orientada al aprendizaje.',
                'opcion_d': 'Delegar toda la decision en una instancia externa para evitar asumir responsabilidad directa frente a la comunidad educativa.',
                'respuesta_correcta': 'C',
                'justificacion': 'La opcion C integra analisis de evidencias, deliberacion responsable, comunicacion clara y finalidad pedagogica. Las demas opciones privilegian presion, aplazamiento o evasion de responsabilidad.',
                'fuente_normativa': 'Estandares de competencias docentes, enfoque CNSC e ICFES Saber: lectura critica, juicio situacional y toma de decisiones.',
                'dificultad': 'premium',
                'area': area,
                'competencia': competencia,
                'tiempo_limite_segundos': 120,
                'es_premium': True,
                'activa': True,
            }
        )
        return pregunta

    def _complete_tjs(self, category):
        banco_categoria = Categoria.objects.first() or Categoria.objects.create(nombre='TJS Concurso Docente')
        for competencia in TJS_COMPETENCIAS:
            subcat, _ = Subcategoria.objects.get_or_create(categoria=banco_categoria, nombre=competencia)
            module = self._module(category, f'TJS - {competencia}', f'tjs-{slugify(competencia)}', f'Simulacro premium de {competencia} con 30 preguntas tipo CNSC.')
            Product.objects.update_or_create(module=module, defaults={'price': Decimal('49000'), 'sale_price': Decimal('39000'), 'active': True})
            preguntas = list(BancoPregunta.objects.filter(subcategoria=subcat, activa=True))
            for i in range(len(preguntas) + 1, 31):
                preguntas.append(self._make_question(banco_categoria, subcat, 'general', competencia, i))
            simulacro, _ = Simulacro.objects.update_or_create(
                nombre=f'TJS - {competencia} - 30 preguntas',
                defaults={
                    'descripcion': f'Seccion TJS premium de nivel avanzado enfocada en {competencia}.',
                    'tipo': 'tjs',
                    'module': module,
                    'area': 'general',
                    'tiempo_limite_minutos': 60,
                    'tiempo_por_pregunta_segundos': 120,
                    'puntaje_minimo_aprobacion': 70,
                    'es_premium': True,
                    'paquete_codigo': 'elite-cnsc-2026',
                    'activo': True,
                }
            )
            simulacro.preguntas.set(preguntas[:30])

    def _create_area_banks(self, category):
        banco_categoria, _ = Categoria.objects.get_or_create(nombre='Simulacros por area CNSC')
        for area, label in AREA_LABELS.items():
            subcat, _ = Subcategoria.objects.get_or_create(categoria=banco_categoria, nombre=label)
            module = self._module(category, f'Simulacro por area - {label}', f'area-{area}', f'Banco disciplinar premium para {label}.')
            Product.objects.update_or_create(module=module, defaults={'price': Decimal('59000'), 'sale_price': Decimal('49000'), 'active': True})
            preguntas = list(BancoPregunta.objects.filter(area=area, subcategoria=subcat, activa=True))
            for i in range(len(preguntas) + 1, 31):
                preguntas.append(self._make_question(banco_categoria, subcat, area, label, i))
            simulacro, _ = Simulacro.objects.update_or_create(
                nombre=f'{label} - Simulacro disciplinar 30 preguntas',
                defaults={
                    'descripcion': f'Simulacro por area para aspirantes de {label}, con lectura critica aplicada al contexto docente.',
                    'tipo': 'area',
                    'module': module,
                    'area': area,
                    'tiempo_limite_minutos': 60,
                    'tiempo_por_pregunta_segundos': 120,
                    'puntaje_minimo_aprobacion': 70,
                    'es_premium': True,
                    'paquete_codigo': 'elite-cnsc-2026',
                    'activo': True,
                }
            )
            simulacro.preguntas.set(preguntas[:30])
