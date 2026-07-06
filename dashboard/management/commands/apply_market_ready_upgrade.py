from decimal import Decimal
import hashlib

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.text import slugify

from academics.models import Category, Module
from banco.models import BancoPregunta, Categoria, Subcategoria
from commerce.models import Product
from contenidos.models import Modulo, Tema
from simulacros.models import Simulacro

MODULES = [
    {
        'slug': 'diagnostico-inicial', 'tipo': 'diagnostico_inicial', 'title': 'Diagnostico inicial',
        'area': 'general', 'competencia': 'Diagnostico integral', 'tipo_sim': 'diagnostico',
        'description': 'Identifica brechas de lectura, pedagogia, normativa, juicio situacional y razonamiento aplicado antes de iniciar la ruta.',
        'topics': ['Mapa de fortalezas y brechas', 'Lectura de consignas', 'Toma de decisiones inicial', 'Uso de resultados para plan de mejora'],
    },
    {
        'slug': 'lectura-critica-aplicada', 'tipo': 'lectura_critica_aplicada', 'title': 'Lectura critica aplicada',
        'area': 'lectura_critica', 'competencia': 'Lectura critica', 'tipo_sim': 'tematico',
        'description': 'Entrena inferencia, intencion comunicativa, estructura argumentativa y evaluacion de evidencia en textos complejos.',
        'topics': ['Inferencia y supuestos', 'Tesis y argumentos', 'Intencion del autor', 'Evaluacion de evidencia'],
    },
    {
        'slug': 'competencias-pedagogicas', 'tipo': 'competencias_pedagogicas', 'title': 'Competencias pedagogicas',
        'area': 'componente_pedagogico', 'competencia': 'Pedagogia y didactica', 'tipo_sim': 'tematico',
        'description': 'Casos de planeacion, evaluacion formativa, inclusion, didactica y gestion del aula con criterio profesional docente.',
        'topics': ['Planeacion curricular', 'Evaluacion formativa', 'Inclusion y DUA', 'Didactica situada'],
    },
    {
        'slug': 'competencias-comportamentales-tjs', 'tipo': 'competencias_tjs', 'title': 'Competencias comportamentales / TJS',
        'area': 'psicotecnico', 'competencia': 'Juicio situacional docente', 'tipo_sim': 'tjs',
        'description': 'Situaciones de convivencia, liderazgo, comunicacion, trabajo en equipo e iniciativa en contexto escolar.',
        'topics': ['Comunicacion asertiva', 'Liderazgo', 'Trabajo en equipo', 'Orientacion al logro'],
    },
    {
        'slug': 'normativa-contexto-docente', 'tipo': 'normativa_contexto', 'title': 'Normativa y contexto docente',
        'area': 'general', 'competencia': 'Normativa educativa aplicada', 'tipo_sim': 'tematico',
        'description': 'Aplicacion contextual de Decreto 1278, Ley 115, inclusion, convivencia escolar y funciones docentes.',
        'topics': ['Estatuto docente', 'Ley General de Educacion', 'Convivencia escolar', 'Inclusion y ajustes razonables'],
    },
    {
        'slug': 'simulacros-por-area', 'tipo': 'simulacros_area', 'title': 'Simulacros por area',
        'area': 'matematicas', 'competencia': 'Razonamiento cuantitativo aplicado', 'tipo_sim': 'area',
        'description': 'Entrenamiento disciplinar y razonamiento cuantitativo con graficas, tablas, proporciones y datos escolares.',
        'topics': ['Razonamiento cuantitativo', 'Matematicas aplicadas', 'Interpretacion de datos', 'Problemas contextualizados'],
    },
    {
        'slug': 'simulacro-final-concurso', 'tipo': 'simulacro_final', 'title': 'Simulacro final tipo concurso',
        'area': 'general', 'competencia': 'Integracion CNSC', 'tipo_sim': 'elite',
        'description': 'Prueba integral con mezcla de competencias, lectura critica, pedagogia, normativa, TJS y razonamiento aplicado.',
        'topics': ['Gestion del tiempo', 'Integracion de competencias', 'Analisis de resultados', 'Estrategia de cierre'],
    },
    {
        'slug': 'reporte-progreso-plan-mejora', 'tipo': 'reporte_mejora', 'title': 'Reporte de progreso y plan de mejora',
        'area': 'general', 'competencia': 'Metacognicion y mejora', 'tipo_sim': 'tematico',
        'description': 'Analiza desempeno, prioriza brechas y convierte resultados de simulacros en decisiones concretas de estudio.',
        'topics': ['Lectura de resultados', 'Priorizacion de brechas', 'Plan semanal', 'Seguimiento de mejora'],
    },
]

SCENARIOS = [
    'Un colegio oficial observa bajo desempeno en lectura y debate si intensificar talleres mecanicos o revisar evidencias por curso.',
    'El consejo academico analiza resultados con brechas entre sedes rurales y urbanas sin reducir el problema a falta de esfuerzo estudiantil.',
    'Una familia solicita ajustes para un estudiante con barreras de participacion y el equipo debe decidir con base en inclusion y trazabilidad.',
    'Docentes de distintas areas discuten si una rubrica debe privilegiar producto final o proceso cuando hay evidencias parciales.',
    'La coordinacion pide una respuesta ante conflicto de aula que afecta convivencia, aprendizaje y confianza de la comunidad.',
    'Un informe de periodo muestra mejora en asistencia pero estancamiento en comprension; el equipo debe interpretar datos no concluyentes.',
    'La institucion quiere adoptar una plataforma digital sin confundir innovacion tecnologica con mejora pedagogica verificable.',
    'Un grupo docente revisa preguntas de simulacro y detecta que algunas premian memoria normativa en vez de juicio profesional.',
    'La rectoria solicita priorizar acciones con recursos limitados y evidencias incompletas sobre aprendizajes fundamentales.',
    'Un comite de evaluacion debate como retroalimentar sin etiquetar estudiantes ni bajar expectativas de aprendizaje.',
    'En una prueba piloto, varios aspirantes fallan no por contenido sino por interpretar mal el alcance de la pregunta.',
    'Un docente nuevo propone una estrategia pertinente, pero necesita articularla con PEI, estandares y evaluacion formativa.',
    'La sede rural reporta conectividad intermitente y el area debe ajustar actividades sin excluir a estudiantes.',
    'Un caso de convivencia exige diferenciar sancion, restauracion, prevencion y corresponsabilidad institucional.',
    'Un analisis de graficas muestra variaciones porcentuales que pueden inducir conclusiones apresuradas si se ignora la base de comparacion.',
    'El equipo directivo revisa indicadores y necesita distinguir correlacion, tendencia y decision pedagogica razonable.',
    'Una planeacion tiene actividades atractivas, pero no evidencia alineacion clara entre objetivo, desempeno y evaluacion.',
    'Los estudiantes resuelven ejercicios, aunque no transfieren el procedimiento a situaciones nuevas del contexto escolar.',
    'Una docente registra avances cualitativos que no aparecen en el promedio numerico y debe argumentar su valor pedagogico.',
    'El comite curricular revisa si una adaptacion es flexibilizacion pertinente o reduccion injustificada del nivel esperado.',
    'Un simulacro institucional genera ansiedad y se debate como convertir el resultado en oportunidad formativa.',
    'Un texto de politica publica presenta fines amplios, pero el evaluado debe identificar implicaciones concretas para el aula.',
    'La comunidad educativa exige resultados inmediatos y el docente debe responder sin sacrificar evidencia ni etica profesional.',
    'Un instrumento de evaluacion muestra sesgos de contexto que afectan la validez de las conclusiones.',
    'El area de matematicas analiza tablas de desempeno y debe decidir si reforzar calculo, lectura de datos o argumentacion.',
    'Una reunion de padres deriva en acusaciones generales y el docente necesita comunicar decisiones con claridad y respeto.',
    'La institucion compara dos periodos academicos con tamanos de muestra distintos y debe evitar una interpretacion lineal.',
    'Un plan de mejoramiento lista muchas acciones, pero no jerarquiza impacto, viabilidad ni seguimiento.',
    'Un aspirante debe decidir que alternativa protege el derecho a aprender sin desconocer normas institucionales.',
    'Un reporte final sintetiza aciertos y errores, pero requiere transformar datos en una ruta concreta de estudio.'
]

STEMS = [
    'A partir del caso, la decision mas pertinente consiste en:',
    'La inferencia mejor sustentada por la situacion es:',
    'El criterio que debe orientar la actuacion docente es:',
    'La alternativa que evita una lectura superficial del problema es:',
    'Desde una perspectiva de mejoramiento institucional, conviene:',
]


def norm(value):
    return ''.join(ch.lower() for ch in value if ch.isalnum())[:180]


def context_for(module, scenario, i):
    return (
        f'{scenario}\n'
        f'El caso se ubica en la competencia {module["competencia"]} y exige analizar informacion, no repetir una definicion.\n'
        'Los actores cuentan con evidencias parciales, restricciones de tiempo y responsabilidades institucionales verificables.\n'
        'Una respuesta apresurada podria mejorar la percepcion inmediata, pero tambien invisibilizar causas pedagogicas o barreras de participacion.\n'
        'Una respuesta puramente normativa tampoco basta si no interpreta el contexto y sus efectos sobre el aprendizaje.\n'
        'El reto consiste en articular datos, comunicacion profesional, proporcionalidad y seguimiento.\n'
        f'El item {i} demanda seleccionar la opcion con mayor validez pedagogica, etica y tecnica.'
    )


def options_for(module, i):
    comp = module['competencia'].lower()
    if 'cuantitativo' in comp:
        return (
            'Comparar solo los valores absolutos y concluir que el grupo con mayor numero de respuestas correctas tuvo mejor desempeno.',
            'Calcular proporciones, revisar el tamano de los grupos y relacionar la tendencia con una decision pedagogica verificable.',
            'Descartar la tabla porque los datos cuantitativos no permiten orientar decisiones pedagogicas.',
            'Promediar todos los resultados sin distinguir area, periodo ni condiciones de aplicacion.'
        )
    if 'normativa' in comp:
        return (
            'Aplicar la norma de manera literal sin analizar finalidad, contexto ni garantia del derecho a la educacion.',
            'Usar la norma como marco, contrastarla con evidencias del caso y documentar una decision proporcional y comunicable.',
            'Delegar la decision en otra instancia para evitar responsabilidad profesional directa.',
            'Priorizar la costumbre institucional aunque contradiga criterios de inclusion o debido proceso.'
        )
    if 'juicio' in comp:
        return (
            'Responder de inmediato para reducir la tension, aun sin escuchar a los actores involucrados.',
            'Escuchar, verificar informacion, comunicar limites y acordar acciones de seguimiento con responsabilidad institucional.',
            'Evitar intervenir hasta que el conflicto desaparezca por si solo.',
            'Trasladar el problema a las familias sin mediacion pedagogica.'
        )
    if 'lectura' in comp:
        return (
            'Elegir la opcion que repite palabras del texto, aunque no explique la relacion entre las ideas.',
            'Identificar tesis, evidencias, supuestos y consecuencias antes de valorar la conclusion propuesta.',
            'Seleccionar la interpretacion mas amplia, aunque no este sustentada en el texto.',
            'Reducir el texto a una opinion personal del lector.'
        )
    return (
        'Adoptar la accion mas visible para mostrar gestion inmediata ante la comunidad.',
        'Analizar evidencias, definir una intervencion proporcional, comunicarla y prever seguimiento de sus efectos.',
        'Aplazar toda decision hasta contar con informacion perfecta y consenso total.',
        'Centrar la respuesta en requisitos formales sin relacionarlos con aprendizajes ni inclusion.'
    )


class Command(BaseCommand):
    help = 'Aplica auditoria comercial y academica: precios, ruta de 8 modulos y banco premium v2.'

    @transaction.atomic
    def handle(self, *args, **options):
        category, _ = Category.objects.update_or_create(
            slug='ruta-premium-cnsc-2026',
            defaults={
                'name': 'Ruta Premium Concurso Docente CNSC 2026',
                'category_type': 'simulacros',
                'description': 'Ruta integral de preparacion con diagnostico, competencias, simulacros y plan de mejora.',
                'icon': 'bi-stars',
                'order': 1,
                'active': True,
            }
        )
        banco_cat, _ = Categoria.objects.get_or_create(nombre='Banco Premium CNSC 2026 V2')

        # Desactiva solo el banco generico anterior de plantilla repetitiva.
        BancoPregunta.objects.filter(
            enunciado__startswith='A partir del texto, cual alternativa representa la decision mas pertinente'
        ).update(activa=False)

        Modulo.objects.exclude(tipo__in=[module['tipo'] for module in MODULES]).update(activo=False)

        created_questions = 0
        for order, data in enumerate(MODULES, 1):
            content_module, _ = Modulo.objects.update_or_create(
                tipo=data['tipo'],
                defaults={'titulo': data['title'], 'descripcion': data['description'], 'orden': order, 'activo': True}
            )
            Tema.objects.filter(modulo=content_module).update(activo=False)
            for topic_order, topic in enumerate(data['topics'], 1):
                Tema.objects.update_or_create(
                    modulo=content_module,
                    orden=topic_order,
                    defaults={'titulo': topic, 'descripcion': f'Entrenamiento aplicado en {topic.lower()} con casos tipo CNSC/ICFES.', 'activo': True}
                )

            module, _ = Module.objects.update_or_create(
                slug=data['slug'],
                defaults={
                    'category': category,
                    'title': data['title'],
                    'short_description': data['description'][:300],
                    'description': data['description'],
                    'difficulty_level': 'cnsc_expert',
                    'estimated_time_minutes': 90,
                    'is_active': True,
                    'is_premium': True,
                }
            )
            Product.objects.update_or_create(
                module=module,
                defaults={'price': Decimal('15000'), 'sale_price': Decimal('15000'), 'active': True}
            )
            subcat, _ = Subcategoria.objects.get_or_create(categoria=banco_cat, nombre=data['title'])
            questions = []
            for i in range(1, 31):
                scenario = SCENARIOS[(i - 1) % len(SCENARIOS)]
                contexto = context_for(data, scenario, i)
                stem = STEMS[(i - 1) % len(STEMS)]
                a, b, c, d = options_for(data, i)
                fingerprint = hashlib.sha1(f"{data['slug']}|{i}|{contexto}|{stem}".encode('utf-8')).hexdigest()[:10]
                pregunta, was_created = BancoPregunta.objects.update_or_create(
                    titulo=f'{data["title"]} V2 {i:02d} {fingerprint}',
                    defaults={
                        'categoria': banco_cat,
                        'subcategoria': subcat,
                        'contexto': contexto,
                        'enunciado': stem,
                        'opcion_a': a,
                        'opcion_b': b,
                        'opcion_c': c,
                        'opcion_d': d,
                        'respuesta_correcta': 'B',
                        'justificacion': 'La opcion B integra lectura del contexto, uso de evidencia, proporcionalidad, comunicacion profesional y seguimiento. Las demas opciones son reduccionistas: privilegian inmediatez, formalismo, evasion o generalizaciones no sustentadas.',
                        'fuente_normativa': 'CNSC/ICFES: razonamiento critico, competencias docentes, Ley 115, Decreto 1278, Decreto 1421 y convivencia escolar segun pertinencia del caso.',
                        'dificultad': 'elite',
                        'area': data['area'],
                        'competencia': data['competencia'],
                        'tiempo_limite_segundos': 120,
                        'es_premium': True,
                        'activa': True,
                    }
                )
                created_questions += int(was_created)
                questions.append(pregunta)

            simulacro, _ = Simulacro.objects.update_or_create(
                nombre=f'{data["title"]} - Simulacro premium V2',
                defaults={
                    'descripcion': data['description'],
                    'tipo': data['tipo_sim'],
                    'module': module,
                    'area': data['area'],
                    'tiempo_limite_minutos': 60,
                    'tiempo_por_pregunta_segundos': 120,
                    'puntaje_minimo_aprobacion': 70,
                    'es_premium': True,
                    'paquete_codigo': 'elite-cnsc-2026',
                    'activo': True,
                }
            )
            simulacro.preguntas.set(questions)

        elite, _ = Module.objects.update_or_create(
            slug='elite-cnsc-2026',
            defaults={
                'category': category,
                'title': 'Acceso completo ConcursoDocente CNSC 2026',
                'short_description': 'Oferta de lanzamiento: todos los modulos, simulacros premium y reportes por un solo pago.',
                'description': 'Incluye diagnostico, lectura critica, competencias pedagogicas, TJS, normativa, areas, simulacro final y plan de mejora.',
                'difficulty_level': 'cnsc_expert',
                'estimated_time_minutes': 480,
                'is_active': True,
                'is_premium': True,
            }
        )
        Product.objects.update_or_create(
            module=elite,
            defaults={'price': Decimal('35000'), 'sale_price': Decimal('25000'), 'active': True}
        )

        # Precios definitivos: paquetes completos 35k/25k; modulos individuales 15k.
        Product.objects.exclude(module=elite).update(price=Decimal('15000'), sale_price=Decimal('15000'), active=True)

        self.stdout.write(self.style.SUCCESS(
            f'Upgrade aplicado: {len(MODULES)} modulos, {created_questions} preguntas nuevas, precios actualizados.'
        ))
