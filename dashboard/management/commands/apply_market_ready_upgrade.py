from decimal import Decimal
import hashlib

from django.core.management.base import BaseCommand
from django.db import transaction

from academics.models import Category, Module
from banco.models import BancoPregunta, Categoria, Subcategoria
from commerce.models import Product
from contenidos.models import Modulo, Tema
from simulacros.models import Simulacro

ELITE_SLUG = 'elite-cnsc-2026'
AREA_MODULE_SLUG = 'simulacros-por-area'
FULL_ACCESS_PRICE = Decimal('20000')

MODULES = [
    {
        'slug': 'diagnostico-inicial', 'tipo': 'diagnostico_inicial', 'title': 'Diagnostico inicial',
        'area': 'general', 'competencia': 'Diagnostico integral', 'tipo_sim': 'diagnostico',
        'description': 'Identifica brechas reales de lectura, pedagogia, normativa, juicio situacional y manejo del tiempo antes de iniciar la ruta.',
        'topics': ['Mapa de fortalezas y brechas', 'Lectura de consignas', 'Toma de decisiones inicial', 'Plan de mejora inicial'],
    },
    {
        'slug': 'lectura-critica-aplicada', 'tipo': 'lectura_critica_aplicada', 'title': 'Lectura critica aplicada',
        'area': 'lectura_critica', 'competencia': 'Lectura critica', 'tipo_sim': 'tematico',
        'description': 'Entrena inferencia, tesis, intencion comunicativa, supuestos, estructura argumentativa y valoracion de evidencias.',
        'topics': ['Inferencia y supuestos', 'Tesis y argumentos', 'Intencion del autor', 'Evaluacion de evidencia'],
    },
    {
        'slug': 'competencias-pedagogicas', 'tipo': 'competencias_pedagogicas', 'title': 'Competencias pedagogicas',
        'area': 'componente_pedagogico', 'competencia': 'Pedagogia y didactica', 'tipo_sim': 'tematico',
        'description': 'Casos de planeacion, evaluacion formativa, inclusion, didactica situada y gestion del aula.',
        'topics': ['Planeacion curricular', 'Evaluacion formativa', 'Inclusion y DUA', 'Didactica situada'],
    },
    {
        'slug': 'competencias-comportamentales-tjs', 'tipo': 'competencias_tjs', 'title': 'Competencias comportamentales / TJS',
        'area': 'psicotecnico', 'competencia': 'Juicio situacional docente', 'tipo_sim': 'tjs',
        'description': 'Situaciones de convivencia, comunicacion, liderazgo, iniciativa, trabajo en equipo y orientacion al logro.',
        'topics': ['Comunicacion asertiva', 'Liderazgo', 'Trabajo en equipo', 'Orientacion al logro'],
    },
    {
        'slug': 'normativa-contexto-docente', 'tipo': 'normativa_contexto', 'title': 'Normativa y contexto docente',
        'area': 'general', 'competencia': 'Normativa educativa aplicada', 'tipo_sim': 'tematico',
        'description': 'Aplicacion contextual de Ley 115, Decreto 1278, inclusion, convivencia escolar y responsabilidad docente.',
        'topics': ['Estatuto docente', 'Ley General de Educacion', 'Convivencia escolar', 'Inclusion y ajustes razonables'],
    },
    {
        'slug': AREA_MODULE_SLUG, 'tipo': 'simulacros_area', 'title': 'Simulacros por area',
        'area': 'general', 'competencia': 'Competencia disciplinar aplicada', 'tipo_sim': 'area',
        'description': 'Entrenamiento disciplinar por area con lectura critica, datos, problemas contextualizados y decision pedagogica.',
        'topics': ['Comprension disciplinar', 'Problemas contextualizados', 'Analisis de datos', 'Decision pedagogica por area'],
    },
    {
        'slug': 'simulacro-final-concurso', 'tipo': 'simulacro_final', 'title': 'Simulacro final tipo concurso',
        'area': 'general', 'competencia': 'Integracion CNSC', 'tipo_sim': 'elite',
        'description': 'Prueba integral con mezcla de lectura critica, pedagogia, normativa, TJS y razonamiento aplicado.',
        'topics': ['Gestion del tiempo', 'Integracion de competencias', 'Analisis de resultados', 'Estrategia de cierre'],
    },
    {
        'slug': 'reporte-progreso-plan-mejora', 'tipo': 'reporte_mejora', 'title': 'Reporte de progreso y plan de mejora',
        'area': 'general', 'competencia': 'Metacognicion y mejora', 'tipo_sim': 'tematico',
        'description': 'Convierte resultados en decisiones de estudio, priorizacion de brechas y seguimiento verificable.',
        'topics': ['Lectura de resultados', 'Priorizacion de brechas', 'Plan semanal', 'Seguimiento de mejora'],
    },
]

AREA_SIMULACROS = [
    {'area': 'ingles', 'label': 'Ingles', 'competencia': 'Comprension lectora funcional en ingles'},
    {'area': 'tecnologia', 'label': 'Tecnologia e Informatica', 'competencia': 'Tecnologia educativa e informatica aplicada'},
    {'area': 'matematicas', 'label': 'Matematicas', 'competencia': 'Razonamiento cuantitativo aplicado'},
    {'area': 'ciencias_naturales', 'label': 'Ciencias Naturales', 'competencia': 'Pensamiento cientifico aplicado'},
    {'area': 'ciencias_sociales', 'label': 'Ciencias Sociales', 'competencia': 'Pensamiento social y ciudadano'},
]

CONTEXTS = [
    'una sede rural con conectividad intermitente y grupos multigrado',
    'un grado sexto con bajo desempeno lector y alta participacion oral',
    'un comite de evaluacion que revisa resultados de dos periodos academicos',
    'una reunion con familias donde se discuten ajustes razonables',
    'un equipo de area que analiza resultados de simulacro y evidencias de aula',
    'una institucion que implementa una plataforma digital sin criterios pedagogicos claros',
    'un consejo academico que debe priorizar acciones con recursos limitados',
    'un grupo de estudiantes que resuelve ejercicios mecanicos pero falla en transferencia',
    'una situacion de convivencia que afecta la confianza entre estudiantes y docentes',
    'una planeacion con actividades atractivas pero evaluacion poco alineada',
]

EVIDENCES = [
    'registros de observacion, resultados por competencia y comentarios de estudiantes',
    'rubricas, productos parciales y actas de seguimiento institucional',
    'graficas de avance, asistencia y desempeno comparadas por curso',
    'relatos de familias, informe de orientacion y evidencias de participacion',
    'resultados de pruebas internas, tiempos de respuesta y errores frecuentes',
    'lineamientos del PEI, plan de mejoramiento y acuerdos del area',
    'indicadores de convivencia, reportes de aula y compromisos previos',
    'portafolios, desempenos orales y retroalimentaciones acumuladas',
    'tablas de desempeno, bases de comparacion y cambios de muestra',
    'preguntas falladas, justificaciones del estudiante y condiciones de aplicacion',
]

TENSIONS = [
    'Algunos actores piden una solucion inmediata para mostrar gestion visible.',
    'Parte del equipo propone repetir actividades sin revisar la causa del error.',
    'La coordinacion solicita una decision trazable y proporcional.',
    'Varias familias reclaman equidad, aunque confunden ajuste razonable con ventaja injustificada.',
    'Los docentes tienen datos utiles, pero no todos apuntan a la misma conclusion.',
    'El tiempo es limitado y la decision puede afectar aprendizaje, convivencia y confianza.',
    'La opcion mas rapida puede ocultar barreras de participacion.',
    'Una lectura literal de la norma no resuelve por si sola el problema pedagogico.',
    'El promedio general mejora, pero persisten errores en inferencia y argumentacion.',
    'La intervencion debe ser viable, comunicable y evaluable posteriormente.',
]

TASKS = [
    ('decision', 'A partir del caso, cual actuacion resulta mas pertinente?'),
    ('inferencia', 'Cual inferencia esta mejor sustentada por la informacion disponible?'),
    ('riesgo', 'Que riesgo debe evitar principalmente el docente?'),
    ('evidencia', 'Que uso de la evidencia permite tomar una decision mas valida?'),
    ('prioridad', 'Cual debe ser la prioridad de intervencion?'),
    ('mejora', 'Que accion convierte el resultado en una mejora verificable?'),
]

MODULE_FOCUS = {
    'diagnostico-inicial': {
        'issue': 'distinguir si los errores provienen de lectura de consigna, falta conceptual, ansiedad o manejo del tiempo',
        'correct': 'Analizar patrones de error por competencia, tiempo usado y tipo de consigna para construir una ruta de estudio priorizada.',
        'why': 'El diagnostico solo sirve si transforma el puntaje en informacion accionable y diferencia causas de error.'
    },
    'lectura-critica-aplicada': {
        'issue': 'valorar tesis, evidencia, supuestos y limites de una conclusion antes de aceptarla',
        'correct': 'Identificar tesis, evidencias, supuestos y alcance de la conclusion antes de elegir una interpretacion.',
        'why': 'La lectura critica exige justificar la interpretacion con relaciones logicas del texto, no con coincidencias literales.'
    },
    'competencias-pedagogicas': {
        'issue': 'alinear desempenos esperados, actividades, evidencias, criterios y retroalimentacion',
        'correct': 'Redisenar la secuencia para alinear proposito, desempeno, evidencia, criterios y retroalimentacion formativa.',
        'why': 'La calidad pedagogica se verifica en la coherencia entre lo que se espera, se ensena, se evalua y se retroalimenta.'
    },
    'competencias-comportamentales-tjs': {
        'issue': 'actuar con escucha, respeto, limites claros, registro y seguimiento institucional',
        'correct': 'Escuchar a los actores, verificar informacion, comunicar limites y acordar acciones proporcionales con seguimiento.',
        'why': 'En TJS la respuesta adecuada protege convivencia, dignidad, evidencia institucional y orientacion al logro.'
    },
    'normativa-contexto-docente': {
        'issue': 'aplicar la norma segun su finalidad educativa, el debido proceso y el derecho a aprender',
        'correct': 'Usar la norma como marco, contrastarla con evidencias del caso y documentar una decision proporcional.',
        'why': 'La norma no opera como cita aislada; debe orientar una decision contextual, trazable y garantista.'
    },
    'simulacros-por-area': {
        'issue': 'resolver una situacion disciplinar usando conceptos, datos y lectura contextual del problema',
        'correct': 'Relacionar conceptos disciplinares, datos del caso y explicaciones de los estudiantes antes de decidir la intervencion.',
        'why': 'La competencia disciplinar se evidencia cuando el docente usa el saber del area para interpretar y actuar pedagogicamente.'
    },
    'simulacro-final-concurso': {
        'issue': 'integrar lectura critica, pedagogia, normativa y juicio situacional en una sola decision',
        'correct': 'Priorizar una respuesta integral, viable y sustentada que atienda aprendizaje, derechos, convivencia y seguimiento.',
        'why': 'El simulacro final exige integrar competencias; una respuesta parcial suele ser insuficiente.'
    },
    'reporte-progreso-plan-mejora': {
        'issue': 'convertir resultados en metas de estudio medibles y revisables',
        'correct': 'Definir un plan especifico por brecha, con practica deliberada, revision de errores y nuevo intento comparable.',
        'why': 'El progreso real depende de patrones de error y acciones verificables, no solo de repetir simulacros.'
    },
}

AREA_FOCUS = {
    'ingles': 'interpretar proposito comunicativo, inferencia contextual y vocabulario funcional en un texto breve de aula',
    'tecnologia': 'evaluar una solucion digital considerando seguridad, pertinencia pedagogica y acceso de los estudiantes',
    'matematicas': 'interpretar proporciones, variaciones y representaciones antes de concluir sobre el desempeno',
    'ciencias_naturales': 'formular explicaciones con variables, evidencias y relaciones causa-efecto verificables',
    'ciencias_sociales': 'analizar fuentes, temporalidad, territorio, ciudadania y conflicto de interpretaciones',
}

DISTRACTORS = [
    'Aplicar la medida mas visible para reducir la presion externa, aunque no explique la causa del problema.',
    'Esperar informacion perfecta y consenso total antes de actuar, aun cuando ya existen evidencias suficientes.',
    'Delegar la decision en otra instancia sin formular una accion pedagogica propia y trazable.',
    'Promediar todos los datos y asumir que el resultado global explica por completo el desempeno.',
    'Elegir la alternativa que repite palabras del caso sin relacionar evidencias, consecuencias y contexto.',
    'Priorizar el cumplimiento formal del procedimiento aunque no se conecte con aprendizaje o inclusion.',
    'Aumentar tareas o simulacros sin revisar el patron de error ni la demanda cognitiva de las preguntas.',
    'Generalizar una conclusion a partir de un dato aislado sin revisar poblacion, condiciones y proposito.',
    'Trasladar la responsabilidad a la familia sin mediacion pedagogica ni seguimiento institucional.',
    'Cambiar toda la ruta de estudio por un resultado puntual sin analizar dificultad ni tiempo usado.',
]

STEM_SUFFIX = {
    'decision': 'Seleccione la opcion que responde con mayor criterio profesional.',
    'inferencia': 'Seleccione la conclusion que no excede la evidencia del caso.',
    'riesgo': 'Seleccione el error de actuacion que comprometeria mas la validez de la decision.',
    'evidencia': 'Seleccione el tratamiento mas riguroso de la informacion disponible.',
    'prioridad': 'Seleccione el foco de intervencion con mayor impacto pedagogico.',
    'mejora': 'Seleccione la accion que permite seguimiento y mejora real.',
}

WORD_REPLACEMENTS = {
    'Diagnostico': 'Diagn\u00f3stico',
    'diagnostico': 'diagn\u00f3stico',
    'critica': 'cr\u00edtica',
    'Critica': 'Cr\u00edtica',
    'critico': 'cr\u00edtico',
    'Critico': 'Cr\u00edtico',
    'Pedagogia': 'Pedagog\u00eda',
    'pedagogia': 'pedagog\u00eda',
    'Didactica': 'Did\u00e1ctica',
    'didactica': 'did\u00e1ctica',
    'Matematicas': 'Matem\u00e1ticas',
    'matematicas': 'matem\u00e1ticas',
    'Tecnologia': 'Tecnolog\u00eda',
    'tecnologia': 'tecnolog\u00eda',
    'Ingles': 'Ingl\u00e9s',
    'ingles': 'ingl\u00e9s',
    'Cientifico': 'Cient\u00edfico',
    'cientifico': 'cient\u00edfico',
    'Metacognicion': 'Metacognici\u00f3n',
    'metacognicion': 'metacognici\u00f3n',
    'modulos': 'm\u00f3dulos',
    'modulo': 'm\u00f3dulo',
    'area': '\u00e1rea',
    'areas': '\u00e1reas',
    'unico': '\u00fanico',
    'segun': 'seg\u00fan',
    'tambien': 'tambi\u00e9n',
    'informacion': 'informaci\u00f3n',
    'accion': 'acci\u00f3n',
    'actuacion': 'actuaci\u00f3n',
    'decision': 'decisi\u00f3n',
    'evaluacion': 'evaluaci\u00f3n',
    'interpretacion': 'interpretaci\u00f3n',
    'institucion': 'instituci\u00f3n',
    'conexion': 'conexi\u00f3n',
    'dificultad': 'dificultad',
    'sistematica': 'sistem\u00e1tica',
    'etica': '\u00e9tica',
    'tecnica': 't\u00e9cnica',
    'valida': 'v\u00e1lida',
    'analisis': 'an\u00e1lisis',
    'estandar': 'est\u00e1ndar',
    'Practicas': 'Pr\u00e1cticas',
    'practicas': 'pr\u00e1cticas',
    'publica': 'p\u00fablica',
    'proposito': 'prop\u00f3sito',
    'propositos': 'prop\u00f3sitos',
    'habitos': 'h\u00e1bitos',
    'basicas': 'b\u00e1sicas',
    'politicas': 'pol\u00edticas',
    'educacion': 'educaci\u00f3n',
    'situacion': 'situaci\u00f3n',
    'gestion': 'gesti\u00f3n',
    'mas': 'm\u00e1s',
    'opcion': 'opci\u00f3n',
    'opciones': 'opciones',
    'limites': 'l\u00edmites',
    'automatica': 'autom\u00e1tica',
    'automatico': 'autom\u00e1tico',
    'desempeno': 'desempe\u00f1o',
    'desempenos': 'desempe\u00f1os',
    'planeacion': 'planeaci\u00f3n',
    'rubricas': 'r\u00fabricas',
    'graficas': 'gr\u00e1ficas',
    'utiles': '\u00fatiles',
    'conclusion': 'conclusi\u00f3n',
    'conclusiones': 'conclusiones',
    'solucion': 'soluci\u00f3n',
    'intervencion': 'intervenci\u00f3n',
    'aplicacion': 'aplicaci\u00f3n',
    'orientacion': 'orientaci\u00f3n',
    'comparacion': 'comparaci\u00f3n',
    'inclusion': 'inclusi\u00f3n',
    'ensenanza': 'ense\u00f1anza',
    'tramite': 'tr\u00e1mite',
    'presion': 'presi\u00f3n',
    'rapida': 'r\u00e1pida',
    'proporcional': 'proporcional',
    'proposito': 'prop\u00f3sito',
    'revision': 'revisi\u00f3n',
    'poblacion': 'poblaci\u00f3n',
    'autentica': 'aut\u00e9ntica',
    'curricular': 'curricular',
    'convivencia': 'convivencia',
    'familias': 'familias',
    'participacion': 'participaci\u00f3n',
    'academico': 'acad\u00e9mico',
    'academicos': 'acad\u00e9micos',
    'comite': 'comit\u00e9',
    'conectividad': 'conectividad',
    'multigrado': 'multigrado',
    'secuencia': 'secuencia',
    'retroalimentacion': 'retroalimentaci\u00f3n',
    'normativa': 'normativa',
    'logica': 'l\u00f3gica',
    'logicas': 'l\u00f3gicas',
    'coordinacion': 'coordinaci\u00f3n',
    'intencion': 'intenci\u00f3n',
    'valoracion': 'valoraci\u00f3n',
    'comunicacion': 'comunicaci\u00f3n',
    'liderazgo': 'liderazgo',
    'priorizacion': 'priorizaci\u00f3n',
    'resolucion': 'resoluci\u00f3n',
    'genericas': 'gen\u00e9ricas',
    'mecanicos': 'mec\u00e1nicos',
    'periodos': 'per\u00edodos',
    'intermitente': 'intermitente',
    'demanda': 'demanda',
    'cognitiva': 'cognitiva',
    'practica': 'pr\u00e1ctica',
    'integracion': 'integraci\u00f3n',
}

PHRASE_REPLACEMENTS = {
    'pedagogica': 'pedag\u00f3gica',
    'pedagogico': 'pedag\u00f3gico',
    'institucionales': 'institucionales',
    'institucional': 'institucional',
    'accionable': 'accionable',
    'A partir del caso, cu\u00e1l actuaci\u00f3n resulta m\u00e1s pertinente?': '\u00bfCu\u00e1l actuaci\u00f3n resulta m\u00e1s pertinente a partir del caso?',
    'A partir del caso, cual actuacion resulta mas pertinente?': '\u00bfCu\u00e1l actuaci\u00f3n resulta m\u00e1s pertinente a partir del caso?',
    'Seleccione la opci\u00f3n que responde con mayor criterio profesional.': 'Seleccione la opci\u00f3n que responde con mayor criterio profesional.',
    'Que acci\u00f3n': 'Qu\u00e9 acci\u00f3n',
    'Que accion': 'Qu\u00e9 acci\u00f3n',
    'como actuar': 'c\u00f3mo actuar',
}


def repair_mojibake(value):
    if '\u00c3' not in value and '\u00c2' not in value:
        return value
    try:
        return value.encode('latin1').decode('utf-8')
    except UnicodeError:
        return value


def polish_text(value):
    import re

    value = repair_mojibake(value)
    for source, target in PHRASE_REPLACEMENTS.items():
        value = value.replace(source, target)
    for source, target in WORD_REPLACEMENTS.items():
        value = re.sub(rf'\b{re.escape(source)}\b', target, value)
    return repair_mojibake(value)

def rotate_options(options, i):
    shift = (i - 1) % 4
    rotated = options[shift:] + options[:shift]
    return rotated, 'ABCD'[rotated.index(options[0])]


def build_item(module, i):
    focus = MODULE_FOCUS[module['slug']]
    task_key, stem = TASKS[(i - 1) % len(TASKS)]
    context = CONTEXTS[(i - 1) % len(CONTEXTS)]
    evidence = EVIDENCES[(i * 2 - 1) % len(EVIDENCES)]
    tension = TENSIONS[(i * 3 - 1) % len(TENSIONS)]
    grade = 5 + (i % 7)
    correct = focus['correct']
    if module['slug'] == AREA_MODULE_SLUG:
        issue = AREA_FOCUS.get(module['area'], focus['issue'])
        correct = f'Analizar {issue}, relacionarlo con evidencias de aula y definir una intervencion proporcional y evaluable.'
    else:
        issue = focus['issue']

    contexto = (
        f'En {context}, el docente de grado {grade} debe resolver una situacion asociada con este reto profesional: {issue}.\n'
        f'El equipo cuenta con {evidence}.\n'
        f'{tension}\n'
        'La situacion no se resuelve con memoria normativa ni con una respuesta automatica: exige leer el contexto, valorar evidencias y anticipar consecuencias.\n'
        'La decision debe ser viable en una institucion educativa oficial, respetar el derecho al aprendizaje y permitir seguimiento posterior.\n'
        f'La competencia evaluada es {module["competencia"]}, por lo que la respuesta debe mostrar criterio profesional y no solo buena intencion.'
    )
    wrongs = [DISTRACTORS[(i + offset * 2) % len(DISTRACTORS)] for offset in range(3)]
    options, answer = rotate_options([correct] + wrongs, i)
    return {
        'contexto': polish_text(contexto),
        'enunciado': polish_text(f'{stem} {STEM_SUFFIX[task_key]}'),
        'opciones': [polish_text(option) for option in options],
        'respuesta': answer,
        'justificacion': polish_text(
            f'La opcion {answer} es correcta porque atiende la competencia {module["competencia"]}: {focus["why"]} '
            'Los distractores son plausibles, pero fallan porque actuan por presion, aplazan sin criterio, delegan responsabilidad, '
            'generalizan datos o privilegian el tramite sobre el aprendizaje.'
        ),
    }


def ensure_unique_options(item):
    normalized = [option.strip().lower() for option in item['opciones']]
    if len(set(normalized)) != 4:
        raise ValueError(f'Opciones duplicadas en item: {item["enunciado"]}')


class Command(BaseCommand):
    help = 'Deja la plataforma lista: banco premium auditado, 8 modulos, 5 areas y pago unico de COP 20.000.'

    @transaction.atomic
    def handle(self, *args, **options):
        category, _ = Category.objects.update_or_create(
            slug='ruta-premium-cnsc-2026',
            defaults={
                'name': 'Ruta Premium Concurso Docente CNSC 2026',
                'category_type': 'simulacros',
                'description': 'Ruta integral con diagnostico, competencias, simulacros, retroalimentacion y plan de mejora.',
                'icon': 'bi-stars',
                'order': 1,
                'active': True,
            },
        )
        banco_cat, _ = Categoria.objects.get_or_create(nombre='Banco Premium CNSC 2026 V3')
        BancoPregunta.objects.update(activa=False)

        valid_module_slugs = [module['slug'] for module in MODULES] + [ELITE_SLUG]
        Modulo.objects.exclude(tipo__in=[module['tipo'] for module in MODULES]).update(activo=False)
        Product.objects.exclude(module__slug__in=valid_module_slugs).update(active=False)

        created_questions = 0
        active_sim_names = []
        for order, data in enumerate(MODULES, 1):
            content_module, _ = Modulo.objects.update_or_create(
                tipo=data['tipo'],
                defaults={'titulo': data['title'], 'descripcion': data['description'], 'orden': order, 'activo': True},
            )
            Tema.objects.filter(modulo=content_module).update(activo=False)
            for topic_order, topic in enumerate(data['topics'], 1):
                Tema.objects.update_or_create(
                    modulo=content_module,
                    orden=topic_order,
                    defaults={'titulo': topic, 'descripcion': f'Entrenamiento aplicado en {topic.lower()} con casos tipo CNSC.', 'activo': True},
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
                },
            )
            Product.objects.update_or_create(
                module=module,
                defaults={'price': FULL_ACCESS_PRICE, 'sale_price': FULL_ACCESS_PRICE, 'active': False},
            )

            if data['slug'] == AREA_MODULE_SLUG:
                continue

            questions = self._build_questions_for_module(banco_cat, data)
            created_questions += questions['created']
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
            simulacro.preguntas.set(questions['items'])
            active_sim_names.append(sim_name)

        area_module_data = next(module for module in MODULES if module['slug'] == AREA_MODULE_SLUG)
        area_module = Module.objects.get(slug=AREA_MODULE_SLUG)
        for area_data in AREA_SIMULACROS:
            module_data = {
                **area_module_data,
                'title': f'Simulacro por area - {area_data["label"]}',
                'area': area_data['area'],
                'competencia': area_data['competencia'],
                'description': f'Banco disciplinar para {area_data["label"]} con lectura critica, datos y decisiones pedagogicas.',
            }
            questions = self._build_questions_for_module(banco_cat, module_data)
            created_questions += questions['created']
            sim_name = f'Simulacro por area - {area_data["label"]}'
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
            simulacro.preguntas.set(questions['items'])
            active_sim_names.append(sim_name)

        elite, _ = Module.objects.update_or_create(
            slug=ELITE_SLUG,
            defaults={
                'category': category,
                'title': 'Acceso completo ConcursoDocente CNSC 2026',
                'short_description': 'Acceso completo a todos los modulos, simulacros y retroalimentaciones por un pago unico.',
                'description': 'Incluye diagnostico, lectura critica, competencias pedagogicas, TJS, normativa, areas, simulacro final y plan de mejora.',
                'difficulty_level': 'cnsc_expert',
                'estimated_time_minutes': 480,
                'is_active': True,
                'is_premium': True,
            },
        )
        Product.objects.update_or_create(
            module=elite,
            defaults={'price': FULL_ACCESS_PRICE, 'sale_price': FULL_ACCESS_PRICE, 'active': True},
        )
        Product.objects.filter(module__slug__in=[module['slug'] for module in MODULES]).update(active=False, price=FULL_ACCESS_PRICE, sale_price=FULL_ACCESS_PRICE)
        Product.objects.exclude(module__slug__in=valid_module_slugs).update(active=False)
        Simulacro.objects.exclude(nombre__in=active_sim_names).update(activo=False)

        self.stdout.write(self.style.SUCCESS(
            f'Plataforma actualizada: 1 producto activo por COP 20.000, {len(active_sim_names)} simulacros y {created_questions} preguntas nuevas/auditadas.'
        ))

    def _build_questions_for_module(self, banco_cat, data):
        subcat, _ = Subcategoria.objects.get_or_create(categoria=banco_cat, nombre=data['title'])
        items = []
        created_count = 0
        for i in range(1, 31):
            item = build_item(data, i)
            ensure_unique_options(item)
            a, b, c, d = item['opciones']
            fingerprint = hashlib.sha1(f'{data["slug"]}|{data["area"]}|{i}|{item["contexto"]}|{item["enunciado"]}'.encode('utf-8')).hexdigest()[:10]
            pregunta, was_created = BancoPregunta.objects.update_or_create(
                titulo=f'{data["title"]} V4 {i:02d} {fingerprint}',
                defaults={
                    'categoria': banco_cat,
                    'subcategoria': subcat,
                    'contexto': item['contexto'],
                    'enunciado': item['enunciado'],
                    'opcion_a': a,
                    'opcion_b': b,
                    'opcion_c': c,
                    'opcion_d': d,
                    'respuesta_correcta': item['respuesta'],
                    'justificacion': item['justificacion'],
                    'fuente_normativa': 'CNSC/ICFES: lectura critica, juicio situacional, competencias docentes y resolucion de casos contextualizados.',
                    'dificultad': 'elite',
                    'area': data['area'],
                    'competencia': data['competencia'],
                    'tiempo_limite_segundos': 180,
                    'es_premium': True,
                    'activa': True,
                },
            )
            created_count += int(was_created)
            items.append(pregunta)
        return {'items': items, 'created': created_count}



