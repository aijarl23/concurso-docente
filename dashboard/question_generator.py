
from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Sequence, Tuple

ELITE_SLUG = 'elite-cnsc-2026'
AREA_MODULE_SLUG = 'simulacros-por-area'
QUESTION_CATEGORY = 'Banco Premium CNSC 2026 SNCS'
SIMILARITY_THRESHOLD = 0.92
QUESTIONS_PER_SIMULACRO = 30

REFERENCE_CALIBRATION = {
    'source': 'PDF simulacros concurso docente aportados por el usuario',
    'use_policy': 'Calibracion de estilo y dificultad; no copia literal de preguntas fuente.',
}

WORD_REPLACEMENTS = {
    'Diagnostico': 'Diagn\u00f3stico', 'diagnostico': 'diagn\u00f3stico',
    'critica': 'cr\u00edtica', 'Critica': 'Cr\u00edtica', 'critico': 'cr\u00edtico',
    'Pedagogia': 'Pedagog\u00eda', 'pedagogia': 'pedagog\u00eda', 'pedagogica': 'pedag\u00f3gica', 'pedagogico': 'pedag\u00f3gico',
    'Matematicas': 'Matem\u00e1ticas', 'matematicas': 'matem\u00e1ticas',
    'Tecnologia': 'Tecnolog\u00eda', 'tecnologia': 'tecnolog\u00eda', 'Ingles': 'Ingl\u00e9s', 'ingles': 'ingl\u00e9s',
    'Cientifico': 'Cient\u00edfico', 'cientifico': 'cient\u00edfico', 'Metacognicion': 'Metacognici\u00f3n',
    'modulos': 'm\u00f3dulos', 'modulo': 'm\u00f3dulo', 'area': '\u00e1rea', 'areas': '\u00e1reas',
    'unico': '\u00fanico', 'segun': 'seg\u00fan', 'tambien': 'tambi\u00e9n', 'informacion': 'informaci\u00f3n',
    'accion': 'acci\u00f3n', 'actuacion': 'actuaci\u00f3n', 'decision': 'decisi\u00f3n', 'evaluacion': 'evaluaci\u00f3n',
    'interpretacion': 'interpretaci\u00f3n', 'institucion': 'instituci\u00f3n', 'conexion': 'conexi\u00f3n',
    'sistematica': 'sistem\u00e1tica', 'etica': '\u00e9tica', 'tecnica': 't\u00e9cnica', 'tecnico': 't\u00e9cnico',
    'valida': 'v\u00e1lida', 'valido': 'v\u00e1lido', 'analisis': 'an\u00e1lisis', 'estandar': 'est\u00e1ndar',
    'Practicas': 'Pr\u00e1cticas', 'practicas': 'pr\u00e1cticas', 'publica': 'p\u00fablica', 'proposito': 'prop\u00f3sito',
    'habitos': 'h\u00e1bitos', 'basico': 'b\u00e1sico', 'basica': 'b\u00e1sica', 'politicas': 'pol\u00edticas',
    'educacion': 'educaci\u00f3n', 'situacion': 'situaci\u00f3n', 'gestion': 'gesti\u00f3n', 'mas': 'm\u00e1s',
    'opcion': 'opci\u00f3n', 'limites': 'l\u00edmites', 'automatica': 'autom\u00e1tica', 'desempeno': 'desempe\u00f1o',
    'desempenos': 'desempe\u00f1os', 'planeacion': 'planeaci\u00f3n', 'rubricas': 'r\u00fabricas', 'graficas': 'gr\u00e1ficas',
    'utiles': '\u00fatiles', 'conclusion': 'conclusi\u00f3n', 'solucion': 'soluci\u00f3n', 'intervencion': 'intervenci\u00f3n',
    'aplicacion': 'aplicaci\u00f3n', 'orientacion': 'orientaci\u00f3n', 'comparacion': 'comparaci\u00f3n', 'inclusion': 'inclusi\u00f3n',
    'ensenanza': 'ense\u00f1anza', 'tramite': 'tr\u00e1mite', 'presion': 'presi\u00f3n', 'rapida': 'r\u00e1pida',
    'revision': 'revisi\u00f3n', 'poblacion': 'poblaci\u00f3n', 'autentica': 'aut\u00e9ntica', 'participacion': 'participaci\u00f3n',
    'academico': 'acad\u00e9mico', 'academicos': 'acad\u00e9micos', 'comite': 'comit\u00e9', 'secuencia': 'secuencia',
    'retroalimentacion': 'retroalimentaci\u00f3n', 'logica': 'l\u00f3gica', 'logicas': 'l\u00f3gicas',
    'coordinacion': 'coordinaci\u00f3n', 'intencion': 'intenci\u00f3n', 'valoracion': 'valoraci\u00f3n',
    'comunicacion': 'comunicaci\u00f3n', 'priorizacion': 'priorizaci\u00f3n', 'resolucion': 'resoluci\u00f3n',
    'genericas': 'gen\u00e9ricas', 'mecanicos': 'mec\u00e1nicos', 'periodos': 'per\u00edodos', 'practica': 'pr\u00e1ctica',
    'integracion': 'integraci\u00f3n', 'hipotesis': 'hip\u00f3tesis', 'proposito': 'prop\u00f3sito', 'ciudadania': 'ciudadan\u00eda',
}

PHRASE_REPLACEMENTS = {
    'Cual actuacion': '\u00bfCu\u00e1l actuaci\u00f3n',
    'Que uso': '\u00bfQu\u00e9 uso',
    'Que alternativa': '\u00bfQu\u00e9 alternativa',
    'Cual inferencia': '\u00bfCu\u00e1l inferencia',
    'Que ajuste': '\u00bfQu\u00e9 ajuste',
    'Que accion': '\u00bfQu\u00e9 acci\u00f3n',
    'Cual valor': '\u00bfCu\u00e1l valor',
}


def polish_text(value: str) -> str:
    for source, target in PHRASE_REPLACEMENTS.items():
        value = value.replace(source, target)
    for source, target in WORD_REPLACEMENTS.items():
        value = re.sub(rf'\b{re.escape(source)}\b', target, value)
    literal_fixes = {
        'nucleo': 'n\u00facleo',
        'reunion': 'reuni\u00f3n',
        'didactica': 'did\u00e1ctica',
        'didactico': 'did\u00e1ctico',
        'Diseno': 'Dise\u00f1o',
        'diseno': 'dise\u00f1o',
        'Indagacion': 'Indagaci\u00f3n',
        'indagacion': 'indagaci\u00f3n',
        'explicacion': 'explicaci\u00f3n',
        'fenomenos': 'fen\u00f3menos',
        'variacion': 'variaci\u00f3n',
        'tamano': 'tama\u00f1o',
    }
    for source, target in literal_fixes.items():
        value = value.replace(source, target)
    return value

MODULES = [
    {'slug': 'diagnostico-inicial', 'tipo': 'diagnostico_inicial', 'title': 'Diagnostico inicial', 'area': 'general', 'competencia': 'Diagnostico integral', 'tipo_sim': 'diagnostico', 'description': 'Identifica brechas reales de lectura, pedagogia, normativa, juicio situacional y manejo del tiempo antes de iniciar la ruta.', 'topics': ['Analisis de errores', 'Comprension de consigna', 'Gestion del tiempo', 'Plan de estudio']},
    {'slug': 'lectura-critica-aplicada', 'tipo': 'lectura_critica_aplicada', 'title': 'Lectura critica aplicada', 'area': 'lectura_critica', 'competencia': 'Lectura critica', 'tipo_sim': 'tematico', 'description': 'Entrena inferencia, tesis, intencion comunicativa, supuestos, estructura argumentativa y valoracion de evidencias.', 'topics': ['Inferencia textual', 'Tesis y argumento', 'Intencion del autor', 'Evaluacion de evidencia']},
    {'slug': 'competencias-pedagogicas', 'tipo': 'competencias_pedagogicas', 'title': 'Competencias pedagogicas', 'area': 'componente_pedagogico', 'competencia': 'Pedagogia y didactica', 'tipo_sim': 'tematico', 'description': 'Casos de planeacion, evaluacion formativa, inclusion, didactica situada y gestion del aula.', 'topics': ['Planeacion curricular', 'Evaluacion formativa', 'Inclusion y DUA', 'Didactica situada']},
    {'slug': 'competencias-comportamentales-tjs', 'tipo': 'competencias_tjs', 'title': 'Competencias comportamentales / TJS', 'area': 'psicotecnico', 'competencia': 'Juicio situacional docente', 'tipo_sim': 'tjs', 'description': 'Situaciones de convivencia, comunicacion, liderazgo, iniciativa, trabajo en equipo y orientacion al logro.', 'topics': ['Comunicacion asertiva', 'Liderazgo pedagogico', 'Trabajo colaborativo', 'Orientacion al logro']},
    {'slug': 'normativa-contexto-docente', 'tipo': 'normativa_contexto', 'title': 'Normativa y contexto docente', 'area': 'general', 'competencia': 'Normativa educativa aplicada', 'tipo_sim': 'tematico', 'description': 'Aplicacion contextual de Ley 115, Decreto 1278, evaluacion, inclusion, convivencia escolar y responsabilidad docente.', 'topics': ['Estatuto docente', 'Ley General de Educacion', 'Convivencia escolar', 'Inclusion y ajustes razonables']},
    {'slug': AREA_MODULE_SLUG, 'tipo': 'simulacros_area', 'title': 'Simulacros por area', 'area': 'general', 'competencia': 'Competencia disciplinar aplicada', 'tipo_sim': 'area', 'description': 'Entrenamiento disciplinar por area con lectura critica, datos, problemas contextualizados y decision pedagogica.', 'topics': ['Comprension disciplinar', 'Problemas contextualizados', 'Analisis de datos', 'Decision pedagogica por area']},
    {'slug': 'simulacro-final-concurso', 'tipo': 'simulacro_final', 'title': 'Simulacro final tipo concurso', 'area': 'general', 'competencia': 'Integracion SNCS', 'tipo_sim': 'elite', 'description': 'Prueba integral con mezcla de lectura critica, pedagogia, normativa, TJS y razonamiento aplicado.', 'topics': ['Integracion de competencias', 'Gestion del tiempo', 'Analisis de resultados', 'Estrategia de cierre']},
    {'slug': 'reporte-progreso-plan-mejora', 'tipo': 'reporte_mejora', 'title': 'Reporte de progreso y plan de mejora', 'area': 'general', 'competencia': 'Metacognicion y mejora', 'tipo_sim': 'tematico', 'description': 'Convierte resultados en decisiones de estudio, priorizacion de brechas y seguimiento verificable.', 'topics': ['Lectura de resultados', 'Priorizacion de brechas', 'Plan semanal', 'Seguimiento de mejora']},
]

AREA_SIMULACROS = [
    {'area': 'ingles', 'label': 'Ingles', 'competencia': 'Comprension lectora funcional en ingles'},
    {'area': 'tecnologia', 'label': 'Tecnologia e Informatica', 'competencia': 'Tecnologia educativa e informatica aplicada'},
    {'area': 'matematicas', 'label': 'Matematicas', 'competencia': 'Razonamiento cuantitativo aplicado'},
    {'area': 'ciencias_naturales', 'label': 'Ciencias Naturales', 'competencia': 'Pensamiento cientifico aplicado'},
    {'area': 'ciencias_sociales', 'label': 'Ciencias Sociales', 'competencia': 'Pensamiento social y ciudadano'},
]

LEVEL_SEQUENCE = ['basico', 'intermedio', 'avanzado', 'intermedio', 'avanzado']
LEVEL_CODE = {'basico': 'B', 'intermedio': 'I', 'avanzado': 'A'}
AREA_CODE = {'general': 'GEN', 'lectura_critica': 'LEC', 'componente_pedagogico': 'PED', 'psicotecnico': 'TJS', 'ingles': 'ING', 'tecnologia': 'TEC', 'matematicas': 'MAT', 'ciencias_naturales': 'NAT', 'ciencias_sociales': 'SOC'}

SCENARIOS = [
    ('una institucion rural con conectividad intermitente', 'registros de asistencia, bitacoras de clase y resultados por competencia'),
    ('un grado sexto con dificultades para justificar respuestas', 'rubricas, respuestas abiertas y tiempos de resolucion'),
    ('un comite academico que revisa dos periodos consecutivos', 'tablas de avance, actas y muestras de cuadernos'),
    ('una reunion con familias sobre apoyos diferenciados', 'informe de orientacion, observaciones de aula y acuerdos previos'),
    ('un equipo de area que compara simulacros aplicados en fechas distintas', 'porcentajes de acierto, errores frecuentes y cambios de muestra'),
    ('una sede urbana con alta rotacion de estudiantes', 'historial de matricula, reportes convivenciales y productos parciales'),
    ('un consejo directivo que exige mejorar indicadores institucionales', 'resultados externos, plan de mejoramiento y seguimiento docente'),
    ('un grupo multigrado que trabaja por proyectos', 'portafolios, entrevistas breves y evidencias de desempeno'),
    ('una institucion que incorpora herramientas digitales', 'reportes de uso, criterios de acceso y evidencias de aprendizaje'),
    ('un docente nuevo que recibe un curso con rezago acumulado', 'diagnostico inicial, lista de cotejo y observacion directa'),
]


CONTEXT_MARKERS = [
    'durante la revision inicial de evidencias',
    'en la reunion de area',
    'al preparar la retroalimentacion',
    'en el seguimiento del periodo',
    'al ajustar el plan de aula',
    'en la socializacion con familias',
    'durante el comite academico',
    'en la revision del SIEE',
    'al contrastar resultados internos',
    'en la planeacion de la siguiente secuencia',
    'durante la observacion de clase',
    'al revisar portafolios de estudiantes',
    'en el analisis de convivencia',
    'al definir apoyos diferenciados',
    'durante la jornada pedagogica',
    'en el cierre del simulacro',
    'al formular el plan de mejora',
    'en la verificacion de aprendizajes',
    'durante el acompanamiento docente',
    'al priorizar brechas de desempeno',
    'en la interpretacion de reportes',
    'al seleccionar evidencias de avance',
    'durante la discusion institucional',
    'en la toma de decisiones curriculares',
    'al revisar el objetivo de aprendizaje',
    'durante la aplicacion de ajustes',
    'en el seguimiento a acuerdos',
    'al valorar la participacion estudiantil',
    'durante la comparacion de resultados',
    'en la organizacion de nuevas actividades',
]

COGNITIVE_TASKS = [
    ('decision', 'Cual actuacion debe priorizar el docente para responder al caso con mayor criterio profesional?'),
    ('evidence', 'Que uso de la evidencia permite sustentar mejor la decision pedagogica?'),
    ('risk', 'Que alternativa representa el riesgo tecnico mas relevante que debe evitarse?'),
    ('inference', 'Cual inferencia se deriva de manera mas valida de la informacion disponible?'),
    ('alignment', 'Que ajuste mejora la coherencia entre proposito, accion y evaluacion?'),
    ('followup', 'Que accion permite verificar si la intervencion produjo mejora real?'),
]

TOPIC_BLUEPRINTS = {
    'diagnostico-inicial': [('analisis de patrones de error','Diagnostico integral','diferenciar errores de comprension, dominio conceptual y manejo del tiempo antes de disenar la ruta de estudio','atribuir todo el resultado a falta de estudio sin revisar patrones'), ('lectura de consignas','Comprension de instrucciones evaluativas','identificar la accion cognitiva solicitada por la consigna y contrastarla con la evidencia del estudiante','responder por palabras clave sin precisar la tarea'), ('priorizacion de brechas','Planeacion metacognitiva','organizar el estudio por brechas de mayor impacto y no por preferencias personales','estudiar primero lo mas comodo aunque no sea lo mas deficitario')],
    'lectura-critica-aplicada': [('tesis y argumentos','Lectura critica','reconocer la tesis, la evidencia que la sostiene y el alcance de la conclusion','confundir un ejemplo llamativo con la idea central'), ('inferencia contextual','Inferencia textual','inferir solo lo que el texto permite justificar sin anadir supuestos externos','extrapolar mas alla de la informacion del texto'), ('intencion comunicativa','Interpretacion del proposito','distinguir si el texto informa, contrasta, cuestiona o persuade mediante sus marcas argumentativas','asumir intencion critica solo porque el texto menciona un problema')],
    'competencias-pedagogicas': [('evaluacion formativa','Evaluacion educativa','usar la evaluacion para retroalimentar, ajustar la ensenanza y hacer seguimiento verificable','reducir la evaluacion a calificacion final'), ('planeacion didactica','Diseno de experiencias de aprendizaje','alinear proposito, desempenos, actividades, evidencias y criterios de valoracion','proponer actividades atractivas sin relacion con el objetivo'), ('inclusion y ajustes razonables','Educacion inclusiva','remover barreras de participacion sin disminuir expectativas de aprendizaje','confundir ajuste razonable con exoneracion automatica')],
    'competencias-comportamentales-tjs': [('comunicacion asertiva','Juicio situacional docente','escuchar, verificar hechos, comunicar limites y acordar seguimiento institucional','responder por presion o confrontacion personal'), ('liderazgo pedagogico','Liderazgo e iniciativa','movilizar al equipo con evidencias, acuerdos y responsabilidades verificables','imponer decisiones sin construir legitimidad ni seguimiento'), ('trabajo colaborativo','Trabajo en equipo','articular aportes del equipo sin diluir la responsabilidad profesional','delegar el caso por completo para evitar conflicto')],
    'normativa-contexto-docente': [('debido proceso','Normativa educativa aplicada','aplicar la norma al caso concreto, documentar la decision y respetar el debido proceso','citar la norma sin analizar proporcionalidad ni contexto'), ('convivencia escolar','Convivencia y responsabilidad docente','activar la ruta institucional con enfoque pedagogico, restaurativo y documentado','resolver informalmente situaciones que requieren trazabilidad'), ('derecho a la educacion','Garantia de derechos','equilibrar exigencia academica, permanencia, participacion y ajustes razonables','priorizar el tramite sobre el derecho efectivo a aprender')],
    'simulacro-final-concurso': [('integracion de competencias','Integracion SNCS','integrar lectura del caso, evidencia, norma, pedagogia y seguimiento en una sola respuesta','elegir una respuesta parcialmente correcta pero incompleta'), ('gestion estrategica del tiempo','Toma de decisiones bajo presion','priorizar preguntas por demanda cognitiva y controlar tiempo sin sacrificar comprension','responder rapido por intuicion en preguntas de alto peso'), ('analisis posterior al simulacro','Mejora basada en evidencia','clasificar errores por causa y convertirlos en practica deliberada','repetir simulacros sin revisar el tipo de error')],
    'reporte-progreso-plan-mejora': [('lectura de resultados','Metacognicion y mejora','interpretar porcentajes junto con tiempo, dificultad y tipo de error','mirar solo el puntaje global'), ('plan semanal','Autorregulacion del aprendizaje','definir metas cortas, evidencias de avance y nuevo intento comparable','formular metas generales sin criterio de verificacion'), ('seguimiento de brechas','Gestion del progreso','revisar si la intervencion reduce errores persistentes y ajustar la ruta','cambiar de tema sin comprobar mejora')],
}

AREA_BLUEPRINTS = {
    'ingles': [('main idea and inference','Comprension lectora funcional en ingles','identify the communicative purpose from context clues and not from isolated vocabulary','translate isolated words without reading the paragraph purpose'), ('classroom instructions','Uso funcional del ingles en aula','infer the appropriate instruction according to the learning task and audience','choose a grammatically possible sentence that does not fit the classroom goal')],
    'tecnologia': [('ciudadania digital','Tecnologia educativa e informatica aplicada','seleccionar herramientas considerando seguridad, accesibilidad, proposito pedagogico y evidencia de aprendizaje','elegir la aplicacion mas novedosa sin criterios pedagogicos'), ('analisis de datos educativos','Uso pedagogico de datos digitales','depurar datos, revisar permisos y transformar reportes en decisiones didacticas','aceptar reportes automaticos sin validar calidad de datos')],
    'matematicas': [('variacion porcentual','Razonamiento cuantitativo aplicado','aplicar variaciones sucesivas sobre la base actual y no sumar porcentajes de forma lineal','sumar descuentos o incrementos como si usaran la misma base'), ('proporcionalidad y razon','Modelacion matematica escolar','identificar la relacion proporcional y justificarla con unidades y razon constante','comparar numeros absolutos sin considerar la base'), ('interpretacion de graficas','Lectura de representaciones','distinguir tendencia, variacion relativa y tamano de muestra antes de concluir','confundir aumento absoluto con mejor desempeno relativo')],
    'ciencias_naturales': [('diseno experimental','Pensamiento cientifico aplicado','controlar variables, formular hipotesis contrastable y usar evidencia observable','concluir causalidad con una sola observacion'), ('explicacion de fenomenos','Indagacion cientifica escolar','relacionar datos, variable independiente, variable dependiente y posible explicacion','memorizar definiciones sin interpretar evidencias')],
    'ciencias_sociales': [('analisis de fuentes','Pensamiento social y ciudadano','contrastar fuente, intencion, contexto y evidencia antes de aceptar una interpretacion','tomar una fuente como neutral por estar escrita formalmente'), ('convivencia y ciudadania','Resolucion de conflictos sociales','reconocer actores, intereses, derechos y mecanismos institucionales de participacion','reducir el conflicto a una opinion individual sin contexto')],
}

@dataclass
class QuestionItem:
    id: str
    area: str
    competencia: str
    nivel_dificultad: str
    contexto: str
    enunciado: str
    opciones: Dict[str, str]
    respuesta_correcta: str
    explicacion: str
    hash_contenido: str
    subtema: str

    def as_dict(self):
        return {'id': self.id, 'area': self.area, 'competencia': self.competencia, 'nivel_dificultad': self.nivel_dificultad, 'contexto': self.contexto, 'enunciado': self.enunciado, 'opciones': self.opciones, 'respuesta_correcta': self.respuesta_correcta, 'explicacion': self.explicacion, 'hash_contenido': self.hash_contenido, 'subtema': self.subtema}

@dataclass
class GenerationRegistry:
    hashes: set = field(default_factory=set)
    signatures: List[Tuple[str, set]] = field(default_factory=list)
    option_memory: set = field(default_factory=set)
    subtopic_counts: Dict[str, int] = field(default_factory=dict)

def normalize(value: str) -> str:
    value = value.lower()
    value = re.sub(r'[^a-z???????0-9\s]', ' ', value)
    return re.sub(r'\s+', ' ', value).strip()

def token_set(value: str) -> set:
    stop = {'que','para','con','una','del','los','las','por','como','debe','de','la','el','en','al','se'}
    return {t for t in normalize(value).split() if len(t) > 3 and t not in stop}

def content_hash(*parts: str) -> str:
    raw = '|'.join(normalize(part) for part in parts)
    return hashlib.sha1(raw.encode('utf-8')).hexdigest()[:12]

def jaccard(a: set, b: set) -> float:
    return len(a & b) / len(a | b) if a and b else 0.0

def rotate_options(options: Sequence[str], seed: int) -> Tuple[Dict[str, str], str]:
    correct = options[0]
    shift = seed % 4
    ordered = list(options[shift:]) + list(options[:shift])
    labels = ['A','B','C','D']
    return dict(zip(labels, ordered)), labels[ordered.index(correct)]

def tuple_to_topic(raw):
    return {'subtema': raw[0], 'competencia': raw[1], 'correct_principle': raw[2], 'typical_error': raw[3]}

def choose_topic(module, index):
    raw = (AREA_BLUEPRINTS[module['area']] if module['slug'] == AREA_MODULE_SLUG else TOPIC_BLUEPRINTS[module['slug']])[index % (len(AREA_BLUEPRINTS[module['area']]) if module['slug'] == AREA_MODULE_SLUG else len(TOPIC_BLUEPRINTS[module['slug']]))]
    return tuple_to_topic(raw)

def build_context(module, topic, level, index, salt):
    scenario, evidence = SCENARIOS[(index + salt) % len(SCENARIOS)]
    grade = 3 + ((index + salt) % 9)
    tensions = ['El equipo docente necesita decidir sin reducir el problema a una impresion general.', 'La coordinacion solicita una accion sustentada y verificable en el corto plazo.', 'Algunos actores proponen una solucion rapida, pero la evidencia muestra matices importantes.', 'La institucion debe evitar que el procedimiento formal oculte la causa pedagogica del problema.', 'El caso exige distinguir entre datos disponibles, supuestos y consecuencias de la decision.']
    complexity = {'basico':'El caso ofrece senales suficientes para reconocer el concepto central evaluado.', 'intermedio':'La decision exige relacionar evidencia, proposito de la intervencion y efecto esperado.', 'avanzado':'La situacion incluye datos parciales, presion institucional y riesgo de una conclusion apresurada.'}[level]
    return polish_text(f'En {scenario}, un docente de grado {grade} analiza una situacion relacionada con {topic["subtema"]}. Cuenta con {evidence}. {tensions[(index*2+salt)%len(tensions)]} {complexity} La respuesta debe centrarse en {topic["competencia"]} y resolver una sola tarea evaluativa.')

def build_stem(task_key, level):
    stem = dict(COGNITIVE_TASKS)[task_key]
    suffix = {'basico':' Seleccione la opcion conceptualmente correcta.', 'intermedio':' Seleccione la opcion mas coherente con la informacion del caso.', 'avanzado':' Seleccione la opcion que integra mejor evidencia, criterio tecnico y seguimiento.'}[level]
    return polish_text(stem + suffix)

def build_options(topic, task_key, level, index):
    focus = topic['correct_principle']
    error = topic['typical_error']
    subtema = topic['subtema']
    competencia = topic['competencia']
    level_clause = {
        'basico': 'con una lectura directa del criterio central',
        'intermedio': 'contrastando evidencias, proposito y efecto esperado',
        'avanzado': 'anticipando consecuencias, trazabilidad y seguimiento posterior',
    }[level]
    marker = CONTEXT_MARKERS[index % len(CONTEXT_MARKERS)]

    correct = {
        'decision': f'Analizar la situacion desde {subtema}, aplicar el criterio de {focus} y dejar una accion verificable, {level_clause}, {marker}.',
        'evidence': f'Contrastar las evidencias del caso para {focus}, evitando conclusiones apoyadas en un unico dato, {level_clause}, {marker}.',
        'risk': f'Evitar {error}, porque ese error distorsiona el analisis de {subtema} y debilita la decision profesional, {level_clause}, {marker}.',
        'inference': f'Inferir que el caso exige {focus}, sin agregar supuestos externos ni ampliar indebidamente la conclusion, {level_clause}, {marker}.',
        'alignment': f'Reajustar proposito, actividades, evidencias y criterios para que todos respondan a {focus}, {level_clause}, {marker}.',
        'followup': f'Definir una evidencia posterior que permita comprobar si la intervencion logro {focus}, {level_clause}, {marker}.',
    }[task_key]

    distractors = [
        f'Tomar la decision principalmente desde {error}, aunque esa ruta no resuelva el nucleo de {subtema}, {marker}.',
        f'Postergar cualquier actuacion hasta lograr acuerdo total, aun cuando ya existen evidencias suficientes sobre {subtema}, {marker}.',
        f'Remitir el caso a otra instancia sin formular criterios profesionales relacionados con {competencia}, {marker}.',
    ]
    if level == 'basico':
        distractors[1] = f'Elegir la alternativa que repite palabras del caso sin conectarlas con {competencia} ni con {subtema}, {marker}.'
    elif level == 'avanzado':
        distractors[2] = f'Promediar los datos disponibles y asumir que ese resultado explica por completo el problema de {subtema}, {marker}.'
    return [polish_text(v) for v in [correct] + distractors]

def build_math_item(index, salt):
    base = 1200000 + ((index + salt) % 7) * 85000
    first = 8 + ((index + salt) % 5) * 3
    second = 5 + ((index + salt) % 4) * 2
    final = round(base * (1 - first / 100) * (1 + second / 100))
    linear = round(base * (1 - (first - second) / 100))
    only_first = round(base * (1 - first / 100))
    wrong_base = round(base * (1 + second / 100) * (1 - first / 100)) + (10000 if index % 2 else -10000)
    context = f'Una institucion proyecta comprar material didactico por ${base:,.0f}. Primero obtiene un descuento del {first}% por compra institucional y luego debe asumir un incremento del {second}% por transporte sobre el valor ya descontado. El comite compara varias respuestas para decidir si el calculo respeta la variacion sucesiva y no una suma lineal de porcentajes.'.replace(',', '.')
    stem = 'Cual valor representa correctamente el costo final aproximado de la compra?'
    options = [f'${final:,.0f}, porque el incremento se aplica sobre el valor posterior al descuento.'.replace(',', '.'), f'${linear:,.0f}, porque basta restar el descuento neto de {first-second} puntos porcentuales.'.replace(',', '.'), f'${only_first:,.0f}, porque el transporte no modifica el precio base de la compra.'.replace(',', '.'), f'${wrong_base:,.0f}, porque los porcentajes pueden aplicarse en cualquier base sin alterar el resultado.'.replace(',', '.')]
    explanation = f'La respuesta correcta aplica variaciones sucesivas: primero descuento del {first}% y luego incremento del {second}% sobre el valor descontado. Las demas opciones suman porcentajes linealmente, ignoran el transporte o cambian la base de calculo.'
    return polish_text(context), polish_text(stem), [polish_text(v) for v in options], polish_text(explanation)

def build_question(module, index, registry, salt=0):
    topic = choose_topic(module, index + salt)
    level = LEVEL_SEQUENCE[(index + salt) % len(LEVEL_SEQUENCE)]
    task_key = COGNITIVE_TASKS[(index + salt) % len(COGNITIVE_TASKS)][0]
    if module.get('area') == 'matematicas' and (index + salt) % 3 == 0:
        context, stem, option_list, explanation = build_math_item(index, salt)
    else:
        context = build_context(module, topic, level, index, salt)
        stem = build_stem(task_key, level)
        option_list = build_options(topic, task_key, level, index)
        explanation = polish_text(f'La opcion correcta se sostiene porque permite {topic["correct_principle"]}. Los distractores son plausibles, pero fallan porque implican {topic["typical_error"]}, aplazan sin criterio o delegan la decision sin evidencia suficiente.')
    options, correct_label = rotate_options(option_list, index + salt + len(module['slug']))
    h = content_hash(module['slug'], module.get('area', ''), context, stem, options[correct_label])
    qid = f'SNCS-{AREA_CODE.get(module.get("area", "general"), "GEN")}-{LEVEL_CODE[level]}-{index+1:04d}-{h[:6].upper()}'
    return QuestionItem(qid, module.get('area', 'general'), polish_text(topic['competencia']), level, context, stem, options, correct_label, explanation, h, polish_text(topic['subtema']))

def validate_item(item, registry):
    if item.hash_contenido in registry.hashes:
        raise ValueError(f'Hash duplicado: {item.id}')
    if item.respuesta_correcta not in {'A','B','C','D'} or set(item.opciones.keys()) != {'A','B','C','D'}:
        raise ValueError(f'Estructura de opciones invalida: {item.id}')
    normalized_options = [normalize(v) for v in item.opciones.values()]
    if len(set(normalized_options)) != 4 or any(not option for option in normalized_options):
        raise ValueError(f'Opciones repetidas o vacias: {item.id}')
    reused = registry.option_memory.intersection(normalized_options)
    if reused:
        raise ValueError(f'Opcion reciclada literalmente en {item.id}: {next(iter(reused))[:80]}')
    forbidden = ['excepto', 'no corresponde', 'no es correcta', 'todas las anteriores', 'ninguna de las anteriores']
    if any(term in normalize(item.enunciado) for term in forbidden):
        raise ValueError(f'Enunciado ambiguo o de descarte: {item.id}')
    if item.enunciado.count('?') > 1:
        raise ValueError(f'Enunciado con mas de una pregunta: {item.id}')
    signature_tokens = token_set(item.contexto + ' ' + item.enunciado)
    for other_id, other_tokens in registry.signatures:
        if jaccard(signature_tokens, other_tokens) > SIMILARITY_THRESHOLD:
            raise ValueError(f'Pregunta semanticamente similar a {other_id}: {item.id}')
    if len(item.explicacion.strip()) < 120:
        raise ValueError(f'Explicacion insuficiente: {item.id}')

def register_item(item, registry):
    registry.hashes.add(item.hash_contenido)
    registry.signatures.append((item.id, token_set(item.contexto + ' ' + item.enunciado)))
    registry.option_memory.update(normalize(v) for v in item.opciones.values())
    registry.subtopic_counts[item.subtema] = registry.subtopic_counts.get(item.subtema, 0) + 1

def generate_question_set(module, count=QUESTIONS_PER_SIMULACRO, registry=None):
    registry = registry or GenerationRegistry()
    items = []
    for index in range(count):
        last_error = None
        for salt in range(120):
            candidate = build_question(module, index, registry, salt=salt)
            try:
                validate_item(candidate, registry)
            except ValueError as exc:
                last_error = exc
                continue
            register_item(candidate, registry)
            items.append(candidate)
            break
        else:
            raise ValueError(f'No se pudo generar pregunta unica para {module["title"]} #{index + 1}: {last_error}')
    return items

def iter_generation_modules():
    for module in MODULES:
        if module['slug'] != AREA_MODULE_SLUG:
            yield module
    area_module = next(module for module in MODULES if module['slug'] == AREA_MODULE_SLUG)
    for area in AREA_SIMULACROS:
        yield {**area_module, 'title': f'Simulacro por area - {area["label"]}', 'area': area['area'], 'competencia': area['competencia'], 'description': f'Banco disciplinar para {area["label"]} con lectura critica, datos, problemas contextualizados y decision pedagogica.'}
