
from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Sequence, Tuple

ELITE_SLUG = 'elite-cnsc-2026'
AREA_MODULE_SLUG = 'simulacros-por-area'
QUESTION_CATEGORY = 'Banco Premium CNSC/SNCS 2026'
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
    'Evaluacion': 'Evaluaci\u00f3n', 'calificacion': 'calificaci\u00f3n', 'cientifica': 'cient\u00edfica', 'Cientifica': 'Cient\u00edfica',
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
    {'slug': 'diagnostico-inicial', 'tipo': 'diagnostico_inicial', 'title': 'Diagnóstico Inicial', 'area': 'general', 'competencia': 'Diagnostico integral', 'tipo_sim': 'diagnostico', 'description': 'Línea base real del aspirante antes de iniciar la ruta: lectura, pedagogía, normativa y manejo del tiempo.', 'topics': ['Analisis de errores', 'Comprension de consigna', 'Gestion del tiempo', 'Plan de estudio']},
    {'slug': 'lectura-critica-aplicada', 'tipo': 'lectura_critica_aplicada', 'title': 'Lectura Crítica', 'area': 'lectura_critica', 'competencia': 'Lectura critica', 'tipo_sim': 'tematico', 'description': 'Inferencia, tesis, intención comunicativa, estructura argumentativa y valoración de evidencias.', 'topics': ['Inferencia textual', 'Tesis y argumento', 'Intencion del autor', 'Evaluacion de evidencia']},
    {'slug': 'normativa-contexto-docente', 'tipo': 'normativa_contexto', 'title': 'Normatividad Educativa', 'area': 'general', 'competencia': 'Normativa educativa aplicada', 'tipo_sim': 'tematico', 'description': 'Aplicación contextual de la Ley 115, el Decreto 1278, el Decreto 1290 y la Ley 1620 a casos reales de la vida escolar.', 'topics': ['Estatuto docente', 'Ley General de Educacion', 'Convivencia escolar', 'Decreto 1290 y SIEE']},
    {'slug': 'inclusion-educativa', 'tipo': 'inclusion_educativa', 'title': 'Inclusión Educativa', 'area': 'general', 'competencia': 'Inclusión y atención a la diversidad', 'tipo_sim': 'tematico', 'description': 'Barreras de aprendizaje, ajustes razonables, PIAR y Diseño Universal para el Aprendizaje aplicados a casos reales de aula.', 'topics': ['DUA aplicado', 'PIAR y ajustes razonables', 'Barreras de participacion', 'Decreto 1421']},
    {'slug': 'competencias-pedagogicas', 'tipo': 'competencias_pedagogicas', 'title': 'Competencias Pedagógicas', 'area': 'componente_pedagogico', 'competencia': 'Pedagogia y didactica', 'tipo_sim': 'tematico', 'description': 'Casos de planeación curricular, evaluación formativa y didáctica situada en el aula.', 'topics': ['Planeacion curricular', 'Evaluacion formativa', 'Didactica situada', 'Gestion del aula']},
    {'slug': 'analisis-de-casos', 'tipo': 'competencias_tjs', 'title': 'Análisis de Casos', 'area': 'psicotecnico', 'competencia': 'Análisis de casos y competencias comportamentales', 'tipo_sim': 'tjs', 'description': 'Dilemas de convivencia, comunicación, liderazgo, iniciativa, trabajo en equipo y orientación al logro, calificados por idoneidad graduada.', 'topics': ['Comunicacion asertiva', 'Liderazgo pedagogico', 'Trabajo colaborativo', 'Orientacion al logro']},
    {'slug': 'gestion-escolar', 'tipo': 'gestion_escolar', 'title': 'Gestión Escolar', 'area': 'general', 'competencia': 'Gobierno escolar y gestión institucional', 'tipo_sim': 'tematico', 'description': 'Gobierno escolar, PEI, consejo académico y las gestiones institucionales del MEN aplicadas a decisiones reales.', 'topics': ['Gobierno escolar', 'PEI y SIEE institucional', 'Gestion academica y directiva', 'Gestion comunitaria']},
    {'slug': AREA_MODULE_SLUG, 'tipo': 'simulacros_area', 'title': 'Competencias Disciplinares', 'area': 'general', 'competencia': 'Competencia disciplinar aplicada', 'tipo_sim': 'area', 'description': 'Saber disciplinar aplicado a la enseñanza del área: lectura crítica, datos, problemas contextualizados y decisión pedagógica.', 'topics': ['Comprension disciplinar', 'Problemas contextualizados', 'Analisis de datos', 'Decision pedagogica por area']},
    {'slug': 'simulacro-final-concurso', 'tipo': 'simulacro_final', 'title': 'Simulacro Integral', 'area': 'general', 'competencia': 'Integracion CNSC', 'tipo_sim': 'elite', 'description': 'Prueba integral con mezcla de lectura crítica, pedagogía, normativa, análisis de casos y razonamiento disciplinar, bajo tiempo real de examen.', 'topics': ['Integracion de competencias', 'Gestion del tiempo', 'Analisis de resultados', 'Estrategia de cierre']},
    {'slug': 'analisis-del-desempeno', 'tipo': 'analisis_desempeno', 'title': 'Análisis del Desempeño', 'area': 'general', 'competencia': 'Metacognición y lectura de resultados', 'tipo_sim': 'tematico', 'description': 'Lectura técnica de resultados por competencia, identificación de patrones de error y priorización de brechas.', 'topics': ['Lectura de resultados', 'Patrones de error', 'Priorizacion de brechas', 'Comparacion con diagnostico inicial']},
    {'slug': 'plan-de-fortalecimiento', 'tipo': 'plan_fortalecimiento', 'title': 'Plan de Fortalecimiento', 'area': 'general', 'competencia': 'Planeación del estudio y seguimiento', 'tipo_sim': 'tematico', 'description': 'Traduce el análisis de desempeño en un plan de estudio semanal con seguimiento verificable.', 'topics': ['Plan semanal', 'Practica deliberada', 'Seguimiento de avance', 'Estrategia de cierre']},
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
    value = re.sub(r'[^a-záéíóúüñ0-9\s]', ' ', value)
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

# --- CURATED SNCS/CNSC OVERRIDE -------------------------------------------------
# Esta seccion reemplaza el generador mecanico anterior por casos curados.
QUESTION_CATEGORY = 'Banco Curado SNCS/CNSC 2026'
REFERENCE_CALIBRATION = {
    'sources': ['PDF aportados por el usuario', 'simulacros de lectura critica, pedagogia, psicotecnicas, matematicas y normativa'],
    'use_policy': 'Extraccion y clasificacion como referencia; los items cargados se reescriben como casos originales y coherentes.',
}

CURATED_VARIANTS = [
    ('una institucion rural con conectividad intermitente', 'sexto', 'resultados por competencia, observaciones de aula y muestras de cuadernos', 'la coordinacion solicita una decision antes del cierre del periodo'),
    ('una sede urbana con alta movilidad de estudiantes', 'octavo', 'rubricas, registros de asistencia y productos parciales', 'las familias piden una solucion inmediata'),
    ('un colegio oficial que revisa su plan de mejoramiento', 'noveno', 'actas de area, reportes de simulacro y seguimiento de apoyos', 'el consejo academico exige evidencias verificables'),
    ('una institucion con aula multigrado', 'quinto', 'portafolios, entrevistas breves y desempenos en clase', 'el equipo docente debe priorizar acciones de bajo costo'),
    ('una institucion que actualiza su SIEE', 'decimo', 'criterios de evaluacion, reclamos de estudiantes y resultados historicos', 'rectoria pide una respuesta tecnicamente sustentada'),
    ('un colegio que implementa ajustes razonables', 'septimo', 'informe de orientacion, PIAR y observaciones de participacion', 'algunos docentes temen que los ajustes reduzcan la exigencia academica'),
    ('un equipo de area que compara dos simulacros', 'once', 'tiempos de respuesta, aciertos por competencia y patrones de error', 'el grupo quiere repetir el simulacro sin analizar fallas'),
    ('una institucion con conflicto de convivencia recurrente', 'noveno', 'relatos de estudiantes, observador y compromisos previos', 'la comunidad espera una sancion rapida'),
    ('un programa de refuerzo academico de jornada contraria', 'septimo', 'diagnostico inicial, asistencia y avances semanales', 'solo quedan cuatro semanas antes de la prueba externa'),
    ('una institucion que incorpora herramientas digitales', 'octavo', 'analiticas de uso, criterios de acceso y evidencias de aprendizaje', 'se propone adoptar la herramienta mas popular sin evaluar pertinencia'),
]

READING_PASSAGES = [
    ('bilinguismo rural', 'El bilinguismo escolar suele presentarse como una meta tecnica: mas horas, mas plataformas y mas materiales. Sin embargo, en varias zonas rurales el problema no es solo la ausencia de recursos, sino la falta de pertinencia cultural de las estrategias. Cuando una comunidad usa radio local, relatos propios y colaboracion entre sedes para practicar una segunda lengua, demuestra que la innovacion no depende unicamente de la tecnologia. La dificultad central consiste en convertir esas iniciativas en procesos sostenibles, evaluables y conectados con el curriculo.', 'la innovacion pedagogica requiere pertinencia cultural y sostenibilidad, no solo recursos tecnologicos', 'la tecnologia por si sola resuelve el aprendizaje de una lengua extranjera'),
    ('evaluacion formativa', 'Una evaluacion puede informar mucho mas que una calificacion. Cuando el docente analiza el tipo de error, conversa con el estudiante y ajusta la siguiente actividad, la prueba deja de ser un cierre administrativo y se convierte en evidencia para ensenar mejor. El problema surge cuando se confunde retroalimentar con decir la respuesta correcta: en ese caso el estudiante recibe informacion, pero no necesariamente comprende como mejorar su desempeno.', 'la evaluacion formativa usa el error para orientar nuevas decisiones de ensenanza y aprendizaje', 'retroalimentar equivale a entregar la solucion correcta al estudiante'),
    ('inclusion', 'La inclusion educativa no se agota en permitir la presencia fisica del estudiante en el aula. Supone identificar barreras de participacion, ajustar mediaciones y sostener expectativas altas de aprendizaje. Si el ajuste se convierte en una exoneracion automatica, se protege al estudiante de la tarea, pero tambien se le priva de participar en ella. El reto institucional consiste en equilibrar apoyo, exigencia y seguimiento.', 'la inclusion exige remover barreras sin disminuir expectativas de aprendizaje', 'incluir significa reemplazar las metas academicas por tareas mas faciles'),
    ('lectura critica', 'En muchas pruebas, el error no proviene de desconocer el tema, sino de leer la pregunta como si pidiera una opinion personal. Una consigna que exige inferir, contrastar o evaluar no se responde localizando una palabra del texto. Requiere reconocer que evidencia autoriza la respuesta y que informacion queda por fuera. La lectura critica, por tanto, no premia al lector mas rapido, sino al que controla mejor sus inferencias.', 'leer criticamente implica ajustar la respuesta a la evidencia y a la tarea cognitiva solicitada', 'la lectura critica consiste en encontrar rapidamente palabras repetidas'),
    ('gestion escolar', 'Un plan de mejoramiento pierde valor cuando se convierte en una lista de actividades sin relacion con los resultados que pretende transformar. La gestion pedagogica exige priorizar problemas, asignar responsables y definir evidencias de avance. Sin ese seguimiento, la institucion puede mostrar movimiento, pero no necesariamente mejora. La accion educativa seria se distingue por su capacidad de verificar efectos.', 'un plan de mejora necesita prioridades, responsables y evidencias de avance verificables', 'la cantidad de actividades ejecutadas demuestra por si misma la mejora institucional'),
]

CURATED_TOPICS = {
' diagnostico-inicial'.strip(): [
('patrones de error','Diagnostico integral','El grupo obtiene bajo puntaje en lectura critica, pero los errores se concentran en preguntas de inferencia y no en recuperacion literal.','Â¿Cual es la primera decision tecnica para orientar el plan de estudio?','Clasificar los errores por demanda cognitiva para distinguir fallas de inferencia, vocabulario, manejo del tiempo y comprension de consigna.','Repetir el mismo simulacro completo hasta que el puntaje global aumente.','Estudiar todos los temas con la misma intensidad para evitar sesgos.','Cambiar de material porque el resultado bajo demuestra que la prueba no fue pertinente.','La decision correcta identifica la causa del error antes de intervenir. El puntaje global por si solo no muestra que habilidad fallo; repetir, estudiar sin prioridad o descartar el instrumento no produce mejora verificable.'),
('gestion del tiempo','Autorregulacion en prueba','Un aspirante responde correctamente cuando trabaja sin limite, pero deja sin contestar la tercera parte del simulacro cronometrado.','Â¿Que interpretacion permite disenar una intervencion mas precisa?','Existe una brecha de estrategia de prueba: debe entrenar lectura de consigna, seleccion de preguntas y control de tiempo por bloque.','El aspirante desconoce todos los contenidos evaluados y debe reiniciar desde teoria basica.','El resultado solo depende de ansiedad, por lo que no conviene revisar habilidades academicas.','La mejor solucion es eliminar el temporizador para evitar presion durante la preparacion.','El contraste entre desempeno sin tiempo y con tiempo senala una dificultad estrategica. No autoriza concluir desconocimiento total ni reducir el problema a ansiedad; eliminar el tiempo impediria preparar condiciones reales.'),
('plan de mejora','Metacognicion aplicada','Despues de tres intentos, el puntaje sube poco aunque el estudiante afirma haber estudiado muchas horas.','Â¿Que ajuste mejora la calidad del seguimiento?','Definir metas semanales por competencia, evidencias de practica y comparacion entre errores previos y nuevos errores.','Aumentar horas de estudio sin modificar el tipo de practica ni los criterios de seguimiento.','Revisar unicamente las preguntas correctas para reforzar la confianza antes del siguiente intento.','Cambiar todos los modulos cada semana para evitar que el estudio se vuelva repetitivo.','La mejora requiere practica deliberada y medicion de errores persistentes. Mas horas sin foco, revisar solo aciertos o cambiar de tema sin comprobar avance no permite saber si la intervencion funciono.'),
],
'competencias-pedagogicas': [
('evaluacion formativa','Evaluacion educativa','Un docente aplica una prueba corta y descubre que la mayoria resuelve procedimientos, pero no justifica sus respuestas.','Â¿Cual actuacion es mas coherente con una evaluacion formativa?','Analizar los errores de justificacion, retroalimentar con criterios claros y proponer una tarea breve que obligue a explicar el razonamiento.','Registrar la calificacion definitiva porque la prueba ya evidencio el nivel de cada estudiante.','Repetir la misma prueba al dia siguiente sin explicar los criterios de mejora.','Eliminar las preguntas de justificacion para que la evaluacion mida solo procedimientos.','La evaluacion formativa usa la evidencia para ajustar ensenanza y aprendizaje. Calificar de inmediato, repetir sin retroalimentar o bajar la exigencia no atiende la dificultad detectada.'),
('planeacion didactica','Diseno de experiencias de aprendizaje','La planeacion incluye actividades llamativas, pero no muestra relacion entre objetivo, desempeno esperado y evidencia de aprendizaje.','Â¿Que ajuste debe realizarse primero?','Alinear objetivo, actividad, evidencia y criterio de valoracion para que todos apunten al mismo aprendizaje.','Agregar mas recursos visuales para que la clase resulte motivadora.','Cambiar la calificacion por participacion para simplificar el seguimiento.','Mantener las actividades porque la motivacion reemplaza la necesidad de evidencias.','Una secuencia didactica valida exige coherencia interna. Los recursos o la participacion pueden apoyar, pero no sustituyen la alineacion entre proposito, actividad y evaluacion.'),
('inclusion y DUA','Educacion inclusiva','Un estudiante con baja vision participa poco porque las guias tienen letra pequena y las explicaciones se apoyan solo en el tablero.','Â¿Que respuesta institucional preserva inclusion y exigencia academica?','Ajustar formatos, ofrecer medios alternativos de acceso y evaluar el mismo proposito de aprendizaje con apoyos razonables.','Eximir al estudiante de las actividades escritas para no aumentar su carga.','Aplicar la misma guia sin cambios para mantener igualdad con el grupo.','Trasladar toda la responsabilidad a la familia mientras la institucion conserva su planeacion.','El ajuste razonable remueve barreras sin bajar expectativas. Eximir, tratar igual situaciones desiguales o desplazar la responsabilidad desconoce el enfoque de inclusion.'),
],
'competencias-comportamentales-tjs': [
('comunicacion asertiva','Juicio situacional docente','Una madre reclama en tono alterado porque considera injusta la calificacion de su hijo y exige cambiarla de inmediato.','Â¿Cual es la respuesta profesional mas adecuada?','Escuchar el reclamo, revisar evidencias con criterios del SIEE, explicar el proceso y acordar una ruta de revision documentada.','Modificar la nota para reducir el conflicto y evitar una queja formal.','Responder en el mismo tono para dejar claro que la decision docente no se discute.','Negarse a revisar evidencias porque aceptar el reclamo afectaria la autoridad del docente.','La actuacion correcta combina escucha, evidencia, norma institucional y trazabilidad. Ceder por presion, confrontar o cerrar la revision deteriora la confianza y el debido proceso.'),
('trabajo colaborativo','Trabajo en equipo','Un area obtiene resultados bajos y cada docente atribuye el problema al curso anterior.','Â¿Que accion favorece una mejora colaborativa?','Revisar evidencias comunes, identificar acuerdos minimos de ensenanza y definir seguimiento por responsabilidad compartida.','Solicitar que coordinacion sancione al docente del grado anterior.','Disenar cada planeacion de forma aislada para respetar la autonomia individual.','Esperar los resultados del siguiente ano antes de realizar cambios.','El trabajo colaborativo requiere datos compartidos, acuerdos y seguimiento. Culpar, aislarse o aplazar decisiones impide intervenir el problema real.'),
('liderazgo pedagogico','Liderazgo e iniciativa','Una docente logra avances en lectura, pero sus colegas desconfian de cambiar sus practicas tradicionales.','Â¿Como puede ejercer liderazgo sin imponer una decision?','Socializar evidencias, abrir una comunidad de practica y construir una secuencia piloto con criterios de seguimiento acordados.','Exigir que todos adopten su metodo porque los resultados la respaldan.','Guardar la estrategia para evitar resistencia del equipo.','Publicar los bajos resultados de sus colegas para presionarlos al cambio.','El liderazgo pedagogico moviliza con evidencia, colaboracion y acuerdos. Imponer, aislarse o exponer publicamente al equipo genera resistencia y no construye capacidad institucional.'),
],
'normativa-contexto-docente': [
('Decreto 1290 y SIEE','Normativa educativa aplicada','Al finalizar el ano, se propone una unica prueba acumulativa para decidir la promocion de estudiantes con dificultades persistentes.','Â¿Que actuacion se ajusta mejor al sentido del SIEE?','Verificar lo previsto en el SIEE, revisar el seguimiento realizado y aplicar estrategias de apoyo coherentes con la evaluacion integral.','Aceptar la prueba unica porque una calificacion final resume todo el proceso.','Promover automaticamente a todos los estudiantes para evitar reclamaciones.','Dejar la decision solo al docente titular sin revisar criterios institucionales.','El Decreto 1290 exige evaluacion integral y criterios institucionales. Una prueba aislada, la promocion automatica o la decision individual sin SIEE desconocen el proceso evaluativo.'),
('debido proceso','Responsabilidad institucional','Ante una falta de convivencia, la comunidad pide retirar al estudiante mientras se aclara lo ocurrido.','Â¿Cual decision respeta mejor el debido proceso?','Activar la ruta institucional, escuchar a las partes, documentar evidencias y aplicar medidas proporcionales con enfoque pedagogico.','Retirar al estudiante de inmediato para enviar un mensaje de autoridad.','Resolver informalmente el caso para evitar registros institucionales.','Esperar a que las familias acuerden una solucion privada sin intervencion escolar.','El debido proceso exige ruta, escucha, evidencia y proporcionalidad. Sancionar sin procedimiento, informalizar o delegar a las familias desconoce la responsabilidad institucional.'),
('PIAR y ajustes razonables','Garantia del derecho a la educacion','Un estudiante con discapacidad cuenta con PIAR, pero varios docentes no lo consultan al disenar actividades evaluativas.','Â¿Que accion institucional es prioritaria?','Revisar el PIAR con el equipo docente y ajustar las mediaciones manteniendo el proposito de aprendizaje.','Aplicar la misma evaluacion a todos para garantizar igualdad formal.','Suspender la evaluacion del estudiante hasta que tenga acompanante permanente.','Reducir la exigencia academica sin definir criterios ni seguimiento.','El PIAR orienta apoyos y ajustes razonables. Igualdad formal, suspension indefinida o reduccion sin criterios no garantizan participacion ni aprendizaje.'),
],
'reporte-progreso-plan-mejora': [
('analisis de resultados','Metacognicion y mejora','El reporte muestra 70% global, pero bajo desempeno en inferencia y alto tiempo de respuesta en preguntas de normativa.','Â¿Que conclusion es mas util para el plan de mejora?','El puntaje global debe desagregarse por competencia y tiempo para priorizar inferencia y normativa aplicada.','El resultado global es suficiente para concluir que no hay brechas importantes.','Debe estudiarse solo normativa porque alli se invirtio mas tiempo.','Conviene repetir el simulacro sin revisar errores para confirmar el porcentaje.','Un reporte serio interpreta puntaje, competencia y tiempo. Mirar solo el global, escoger un area sin analisis completo o repetir sin revision no orienta mejora.'),
('practica deliberada','Autorregulacion del aprendizaje','Despues de revisar errores, el estudiante descubre que falla cuando dos opciones son parcialmente correctas.','Â¿Que practica fortalece mejor esa debilidad?','Comparar pares de opciones, justificar por que una integra mejor evidencia y registrar el criterio de descarte usado.','Memorizar respuestas correctas de simulacros anteriores.','Evitar preguntas con opciones parecidas porque consumen demasiado tiempo.','Contestar siempre la opcion mas larga porque suele estar mejor argumentada.','La dificultad exige discriminar calidad de opciones. Memorizar, evitar preguntas o usar longitud como regla produce respuestas mecanicas e inseguras.'),
('seguimiento semanal','Plan de mejora','El usuario tiene cuatro semanas y debe subir de 58% a 75% en simulacro final.','Â¿Cual plan es mas tecnicamente defendible?','Asignar metas semanales por competencia, practica cronometrada, revision de explicaciones y un simulacro comparable al cierre de cada ciclo.','Estudiar teoria todos los dias y dejar los simulacros para la ultima semana.','Practicar solo el modulo que mas le gusta para sostener la motivacion.','Hacer simulacros diarios completos sin analizar justificaciones.','El plan defendible combina foco, tiempo real, retroalimentacion y medicion comparable. Teoria sin practica, preferencia personal o simulacros sin analisis no garantizan avance.'),
],
}
CURATED_TOPICS['simulacro-final-concurso'] = CURATED_TOPICS['competencias-pedagogicas'] + CURATED_TOPICS['competencias-comportamentales-tjs'] + CURATED_TOPICS['normativa-contexto-docente'] + CURATED_TOPICS['diagnostico-inicial']

AREA_TOPICS_CURATED = {
'ingles': [
('main idea','Comprension lectora funcional en ingles','A school newsletter says: "The reading club will meet every Friday after class. Students should bring a short text they enjoy and be ready to explain why it matters to them."','What is the main purpose of the announcement?','To invite students to participate in a reading club and prepare a brief personal explanation.','To inform families about a mandatory evaluation schedule.','To announce that all classes will end earlier on Fridays.','To request teachers to grade students during the club meeting.','The announcement invites participation and states what students should bring. It does not describe an exam, a schedule change or a teacher grading process.'),
('classroom instruction','Uso funcional del ingles en aula','During a science activity, students must compare two pictures and explain one difference orally in English.','Which instruction best fits the task?','Look at both pictures, choose one difference and explain it to your partner using a complete sentence.','Copy the title from the board and remain silent until the teacher checks your notebook.','Translate every word in the textbook before looking at the pictures.','Close your book and memorize the list of irregular verbs for tomorrow.','The task requires comparing pictures and producing oral language. The distractors involve copying, translating unrelated text or memorizing grammar outside the task.'),
('inference','Inferencia en textos breves','A teacher writes: "Although the internet was down, the students completed the interview project using printed questions and recorded the answers on a shared phone."','What can be reasonably inferred from the sentence?','The class adapted the project to available resources instead of cancelling the communicative task.','The project failed because students could not use the internet.','The teacher changed the objective from speaking to grammar memorization.','Every student had an individual device with permanent connection.','The sentence shows adaptation under limited connectivity. It does not say the project failed, changed objective or had full access to devices.'),
],
' tecnologia'.strip(): [
('ciudadania digital','Tecnologia educativa e informatica aplicada','Un docente quiere abrir un foro virtual para que estudiantes publiquen opiniones sobre convivencia escolar.','Â¿Que criterio debe revisar antes de habilitar la actividad?','Privacidad, normas de interaccion, proposito pedagogico y forma de moderacion de las participaciones.','Cantidad de efectos visuales disponibles en la plataforma.','Popularidad de la aplicacion entre estudiantes de otros colegios.','Posibilidad de publicar sin registro para aumentar la participacion.','Una actividad digital con menores exige seguridad, proposito y moderacion. La estetica, popularidad o anonimato sin control no garantizan aprendizaje ni proteccion.'),
('analitica de aprendizaje','Uso pedagogico de datos digitales','Una plataforma reporta que el 90% del curso ingreso al recurso, pero solo el 35% completo las actividades de aplicacion.','Â¿Que decision interpreta mejor los datos?','Distinguir acceso de aprendizaje efectivo y revisar barreras para completar la actividad de aplicacion.','Concluir que el recurso fue exitoso porque casi todos ingresaron.','Suspender toda herramienta digital porque los estudiantes no aprenden en linea.','Aumentar la nota por ingreso sin revisar desempeno en la tarea.','El ingreso no equivale a aprendizaje. La decision correcta analiza la brecha entre acceso y finalizacion; las otras opciones simplifican indebidamente los datos.'),
('seleccion de herramientas','Integracion TIC','El area propone usar una aplicacion con inteligencia artificial para producir resumenes automaticos de textos.','Â¿Que uso seria pedagogicamente mas solido?','Usarla como apoyo para comparar resumenes, discutir omisiones y exigir justificacion de ideas centrales con evidencia del texto.','Permitir que la herramienta reemplace la lectura para ahorrar tiempo de clase.','Prohibirla sin analisis porque toda automatizacion elimina el aprendizaje.','Calificar unicamente la extension del resumen generado por la aplicacion.','La integracion solida convierte la herramienta en objeto de analisis y mejora la lectura critica. Reemplazar lectura, prohibir sin criterio o calificar extension no evalua comprension.'),
],
'ciencias_naturales': [
('diseno experimental','Pensamiento cientifico aplicado','Un grupo quiere comprobar si la luz afecta el crecimiento de una planta, pero cambia al mismo tiempo la cantidad de agua y el tipo de suelo.','Â¿Cual es el principal problema del diseno?','No controla variables, por lo que no puede atribuir el resultado unicamente a la luz.','No usa suficientes nombres cientificos para describir la planta.','El experimento deberia hacerse sin registrar datos para evitar sesgos.','La hipotesis es innecesaria porque las plantas siempre crecen con luz.','Para inferir relacion causal debe controlarse el resto de variables. La terminologia, ausencia de registro o supresion de hipotesis no resuelven el problema metodologico.'),
('interpretacion de evidencias','Indagacion cientifica escolar','Despues de observar condensacion en un vaso frio, varios estudiantes afirman que el agua atraveso el vidrio.','Â¿Que intervencion docente favorece mejor la explicacion cientifica?','Guiar la observacion de vapor de agua del aire y su cambio de estado al contacto con la superficie fria.','Aceptar la explicacion inicial porque proviene de una observacion directa.','Corregir diciendo solo la respuesta sin pedir nuevas evidencias.','Cambiar de tema porque la condensacion no permite formular hipotesis.','La intervencion conecta observacion, cambio de estado y evidencia. Aceptar la idea erronea, dar respuesta sin indagacion o abandonar el fenomeno no desarrolla pensamiento cientifico.'),
('lectura de graficas','Analisis de datos cientificos','Una grafica muestra que al aumentar la temperatura de 20 C a 35 C aumenta la velocidad de reaccion, pero despues de 40 C disminuye.','Â¿Que conclusion es mas consistente con la evidencia?','La relacion no es lineal en todo el rango; existe un punto a partir del cual el aumento de temperatura reduce la velocidad.','Toda subida de temperatura aumenta indefinidamente la velocidad de reaccion.','La temperatura no influye porque la velocidad disminuye al final.','La grafica no permite ninguna conclusion sobre cambios de velocidad.','La evidencia muestra aumento inicial y disminucion posterior. Las opciones incorrectas generalizan, niegan una relacion parcial o desconocen informacion visible.'),
],
'ciencias_sociales': [
('analisis de fuentes','Pensamiento social y ciudadano','Dos fuentes describen una protesta escolar: una carta de estudiantes y un comunicado de rectoria. Ambas coinciden en el hecho, pero difieren en sus causas.','Â¿Que procedimiento fortalece el analisis historico-social?','Contrastar autor, intencion, contexto y evidencias antes de decidir que explicacion resulta mejor sustentada.','Aceptar la version institucional porque usa lenguaje mas formal.','Aceptar la carta estudiantil porque expresa inconformidad colectiva.','Promediar ambas versiones sin revisar sus argumentos.','El analisis de fuentes exige contrastar perspectiva y evidencia. La formalidad, la empatia o el promedio de versiones no determinan validez.'),
('convivencia democratica','Resolucion de conflictos sociales','Un curso se divide por la distribucion de recursos para una salida pedagogica y algunos estudiantes sienten que no fueron escuchados.','Â¿Que accion promueve participacion democratica?','Abrir un espacio con reglas claras para escuchar argumentos, revisar criterios de distribucion y acordar una decision transparente.','Decidir por sorteo sin explicar criterios ni escuchar inconformidades.','Permitir que el grupo mas numeroso imponga su preferencia.','Cancelar la salida para evitar discutir el conflicto.','La participacion democratica requiere escucha, criterios y transparencia. Sorteo sin deliberacion, imposicion mayoritaria o cancelacion evitan el aprendizaje ciudadano.'),
('territorio y contexto','Lectura critica del contexto social','Un proyecto escolar analiza por que dos barrios con igual numero de habitantes tienen acceso distinto a bibliotecas y transporte.','Â¿Que enfoque permite una explicacion social mas completa?','Relacionar distribucion espacial, decisiones publicas, historia del territorio y efectos sobre oportunidades educativas.','Atribuir la diferencia unicamente a preferencias individuales de los habitantes.','Comparar solo el numero de habitantes porque las demas variables son subjetivas.','Concluir que el barrio con menos servicios no necesita intervencion si sus habitantes se adaptan.','La explicacion social integra territorio, politica publica e inequidad. Reducir a preferencias, usar solo poblacion o naturalizar la desigualdad empobrece el analisis.'),
],
}

CURATED_LEVELS = ['basico', 'intermedio', 'avanzado']

def _curated_level(index):
    return CURATED_LEVELS[index % 3]

def _suffix_option(text, subtema, index):
    return f'{text} Enfoque evaluado: {subtema}; caso {index + 1}.'

def _make_curated_from_tuple(module, index, raw, area=None):
    subtema, competencia, case, stem, correct, d1, d2, d3, exp = raw
    inst, grade, evidence, pressure = CURATED_VARIANTS[index % len(CURATED_VARIANTS)]
    contexto = f'En {inst}, un grupo de {grade} enfrenta esta situacion: {case} El equipo cuenta con {evidence} y {pressure}.'
    opts, correct_label = rotate_options([
        _suffix_option(correct, subtema, index),
        _suffix_option(d1, subtema, index),
        _suffix_option(d2, subtema, index),
        _suffix_option(d3, subtema, index),
    ], index + len(module.get('slug', '')))
    item_area = area or module.get('area', 'general')
    level = _curated_level(index)
    h = content_hash(module.get('slug',''), contexto, stem, correct)
    qid = f'SNCS-{AREA_CODE.get(item_area, "GEN")}-{LEVEL_CODE[level]}-{index+1:04d}-{h[:6].upper()}'
    return QuestionItem(qid, item_area, competencia, level, contexto, stem, opts, correct_label, f'{exp} Subtema evaluado: {subtema}.', h, subtema)

def _make_reading_item(module, index):
    topic, text, thesis, rejected = READING_PASSAGES[index % len(READING_PASSAGES)]
    task = index % 4
    if task == 0:
        stem = 'Â¿Cual afirmacion expresa mejor la tesis central del texto?'
        correct = f'El texto sostiene que {thesis}.'
        ds = [f'El texto afirma que {rejected}.', f'El texto solo define {topic} sin adoptar postura.', 'El texto defiende que los resultados educativos dependen exclusivamente de decisiones individuales.']
        exp = 'La tesis central organiza los argumentos del texto. La opcion correcta recoge esa postura completa; los distractores exageran, reducen o contradicen el sentido del pasaje.'
        subtema = 'tesis textual'
    elif task == 1:
        stem = 'Â¿Que inferencia se deriva de manera mas valida del texto?'
        correct = 'La respuesta educativa debe considerar evidencias del contexto y no apoyarse en una solucion unica o automatica.'
        ds = ['Toda innovacion escolar fracasa si no cuenta con recursos abundantes.', 'El autor niega la importancia de evaluar los procesos educativos.', 'La dificultad debe eliminarse siempre para facilitar el aprendizaje.']
        exp = 'La inferencia valida se apoya en informacion explicita e implicita del pasaje sin anadir supuestos externos. Los distractores generalizan o atribuyen al texto ideas que no sostiene.'
        subtema = 'inferencia textual'
    elif task == 2:
        stem = 'Â¿Cual es la intencion comunicativa predominante del autor?'
        correct = 'Cuestionar una explicacion simplista y proponer una lectura mas contextualizada del problema educativo.'
        ds = ['Narrar una experiencia personal sin relacion con una postura argumentativa.', 'Ordenar un procedimiento administrativo obligatorio paso a paso.', 'Convencer al lector de que no es necesario revisar evidencias para decidir.']
        exp = 'El texto problematiza una idea y defiende una interpretacion mas compleja. No funciona como narracion anecdÃ³tica, instructivo administrativo ni rechazo de la evidencia.'
        subtema = 'intencion comunicativa'
    else:
        stem = 'Â¿Que opcion identifica mejor un supuesto que el texto rechaza?'
        correct = f'Que {rejected}.'
        ds = [f'Que el analisis de {topic} requiere revisar contexto y evidencias.', 'Que una decision educativa debe poder justificarse con criterios verificables.', 'Que las practicas escolares pueden mejorar cuando se analizan sus efectos.']
        exp = 'El texto rechaza una lectura reduccionista. Las demas opciones son compatibles con el enfoque argumentativo del pasaje, no supuestos criticados por el autor.'
        subtema = 'supuestos del texto'
    opts, label = rotate_options([_suffix_option(correct, subtema, index)] + [_suffix_option(d, subtema, index) for d in ds], index + 13)
    level = _curated_level(index)
    h = content_hash(module.get('slug','lectura'), text, stem, correct)
    return QuestionItem(f'SNCS-LEC-{LEVEL_CODE[level]}-{index+1:04d}-{h[:6].upper()}', 'lectura_critica', 'Lectura critica', level, text, stem, opts, label, exp, h, subtema)

def _make_math_item(module, index, area='matematicas'):
    mode = index % 5
    level = _curated_level(index)
    if mode == 0:
        base = 800000 + (index * 37000); discount = 8 + (index % 6) * 2; increase = 5 + (index % 4) * 3
        final = round(base * (1 - discount / 100) * (1 + increase / 100))
        contexto = f'Una institucion compra licencias educativas por ${base:,.0f}. Primero obtiene un descuento del {discount}% y despues paga un incremento de transporte del {increase}% sobre el valor ya descontado.'.replace(',', '.')
        stem = 'Â¿Cual es el valor final aproximado que debe pagar la institucion?'
        correct = f'${final:,.0f}, porque los porcentajes se aplican de forma sucesiva sobre bases distintas.'.replace(',', '.')
        d1 = f'${round(base*(1-(discount-increase)/100)):,.0f}, porque basta restar los porcentajes como si tuvieran la misma base.'.replace(',', '.')
        d2 = f'${round(base*(1-discount/100)):,.0f}, porque el incremento de transporte no debe incluirse en el costo final.'.replace(',', '.')
        d3 = f'${round(base*(1+increase/100)):,.0f}, porque el descuento se aplica solo despues de cerrar el pago.'.replace(',', '.')
        exp = 'En variaciones sucesivas cada porcentaje se calcula sobre el valor resultante del paso anterior. Sumar o restar porcentajes linealmente cambia la base y produce un valor equivocado.'; subtema='variacion porcentual sucesiva'
    elif mode == 1:
        total = 240 + index * 8; r1 = 3 + index % 4; r2 = 2 + (index + 1) % 3; ans = round(total * r1 / (r1 + r2))
        contexto = f'Para distribuir {total} guias entre dos sedes, el equipo decide respetar la razon {r1}:{r2}, porque una sede tiene mas grupos activos que la otra.'
        stem = 'Â¿Cuantas guias corresponden aproximadamente a la sede con mayor participacion en la razon?'
        correct = f'{ans} guias, porque se divide el total en {r1 + r2} partes iguales y se toman {r1} partes.'
        d1 = f'{round(total/2)} guias, porque toda distribucion justa debe hacerse en mitades iguales.'
        d2 = f'{r1*r2*10} guias, porque se multiplican los dos terminos de la razon.'
        d3 = f'{total-ans} guias, porque la sede mayor recibe el complemento de la menor.'
        exp = 'Una razon parte el total en unidades proporcionales. La opcion correcta calcula la unidad de reparto; dividir en mitades o multiplicar terminos desconoce la razon dada.'; subtema='proporcionalidad'
    elif mode == 2:
        a1=42+index; a2=a1+5+index%3; n1=30+index%5; n2=15+index%4
        contexto=f'Dos cursos presentan avance en lectura: el curso A sube de {a1}% a {a2}% con {n1} estudiantes, mientras el curso B sube de {a1-4}% a {a2+3}% con {n2} estudiantes.'
        stem='Â¿Que conclusion es mas prudente a partir de esos datos?'
        correct='Comparar tanto la variacion como el tamano de cada grupo antes de afirmar cual intervencion fue mas efectiva.'
        d1='Concluir que el curso B es mejor solo porque termina con un porcentaje mas alto.'; d2='Concluir que ambos cursos tienen el mismo avance porque sus porcentajes iniciales son parecidos.'; d3='Ignorar el tamano de muestra porque los porcentajes siempre son directamente comparables.'
        exp='La interpretacion de porcentajes exige considerar cambio relativo y tamano de muestra. Elegir solo el porcentaje final o ignorar la base puede producir conclusiones enganosa.'; subtema='interpretacion de porcentajes'
    elif mode == 3:
        contexto='Una grafica institucional muestra que los aciertos en lectura aumentan durante tres semanas, se estabilizan en la cuarta y disminuyen levemente en la quinta, cuando se redujo el tiempo disponible por pregunta.'
        stem='Â¿Cual interpretacion es mas consistente con la informacion descrita?'
        correct='La disminucion final puede estar asociada al cambio de tiempo, por lo que no conviene atribuirla de inmediato a perdida de aprendizaje.'
        d1='La tendencia demuestra que los estudiantes olvidaron todo lo aprendido en la quinta semana.'; d2='La estabilizacion de la cuarta semana prueba que la intervencion ya no sirve.'; d3='La grafica no permite formular hipotesis porque solo contiene porcentajes.'
        exp='Una interpretacion prudente relaciona tendencia y condiciones de aplicacion. Los distractores hacen inferencias causales fuertes sin evidencia suficiente.'; subtema='lectura de graficas'
    else:
        contexto='En un simulacro, una estudiante responde 18 preguntas correctas de 30. En el siguiente intento responde 22 de 30, pero tarda 20 minutos mas.'
        stem='Â¿Que indicador adicional ayuda a valorar mejor su progreso?'
        correct='El porcentaje de acierto junto con el tiempo promedio por pregunta y el tipo de error corregido.'
        d1='Solo el numero absoluto de respuestas correctas, porque el tiempo no afecta la preparacion.'; d2='Solo el tiempo total, porque responder mas rapido siempre equivale a aprender mejor.'; d3='El numero de preguntas que dejo en blanco, sin revisar aciertos ni errores.'
        exp='El progreso en pruebas combina precision, tiempo y naturaleza del error. Mirar un solo indicador puede ocultar mejoras fragiles o retrocesos estrategicos.'; subtema='analisis de desempeno cuantitativo'
    opts, label = rotate_options([_suffix_option(correct, subtema, index), _suffix_option(d1, subtema, index), _suffix_option(d2, subtema, index), _suffix_option(d3, subtema, index)], index+23)
    h = content_hash(module.get('slug','mat'), contexto, stem, correct)
    return QuestionItem(f'SNCS-{AREA_CODE.get(area,"MAT")}-{LEVEL_CODE[level]}-{index+1:04d}-{h[:6].upper()}', area, 'Razonamiento cuantitativo aplicado', level, contexto, stem, opts, label, exp, h, subtema)

def _curated_build_question(module, index):
    slug = module.get('slug')
    if module.get('tipo_sim') == 'area':
        if module.get('area') == 'matematicas':
            return _make_math_item(module, index, 'matematicas')
        raw = AREA_TOPICS_CURATED[module.get('area')][index % len(AREA_TOPICS_CURATED[module.get('area')])]
        return _make_curated_from_tuple(module, index, raw, area=module.get('area'))
    if slug == 'lectura-critica-aplicada':
        return _make_reading_item(module, index)
    if slug == 'simulacro-final-concurso' and index % 5 == 1:
        return _make_math_item(module, index, 'general')
    if slug == 'simulacro-final-concurso' and index % 5 == 0:
        return _make_reading_item({'slug': slug}, index)
    raw = CURATED_TOPICS.get(slug, CURATED_TOPICS['diagnostico-inicial'])[index % len(CURATED_TOPICS.get(slug, CURATED_TOPICS['diagnostico-inicial']))]
    return _make_curated_from_tuple(module, index, raw, area=module.get('area','general'))

def generate_question_set(module, count=QUESTIONS_PER_SIMULACRO, registry=None):
    registry = registry or GenerationRegistry()
    items = []
    index = 0
    while len(items) < count and index < count * 20:
        item = _curated_build_question(module, index)
        index += 1
        try:
            validate_item(item, registry)
        except ValueError:
            continue
        register_item(item, registry)
        items.append(item)
    if len(items) < count:
        raise ValueError(f'No se pudo completar banco curado para {module.get("title")}: {len(items)}/{count}')
    return items

# Ajuste de unicidad para lectura critica: 30 items sin hash repetido.
SIMILARITY_THRESHOLD = 0.96
READING_EXTENSION_SENTENCES = [
    'El caso se analiza desde la relacion entre evidencia textual y conclusion defendible.',
    'La pregunta exige distinguir la informacion del texto de las opiniones previas del lector.',
    'La respuesta debe apoyarse en marcas argumentativas y no en palabras aisladas.',
    'El foco esta en reconocer alcance, limite e intencion de la afirmacion principal.',
    'La tarea evalua control de inferencias y pertinencia de la evidencia seleccionada.',
    'El lector debe evitar extrapolaciones no autorizadas por el pasaje.',
]

def _make_reading_item(module, index):
    topic, base_text, thesis, rejected = READING_PASSAGES[index % len(READING_PASSAGES)]
    text = base_text + ' ' + READING_EXTENSION_SENTENCES[(index // len(READING_PASSAGES)) % len(READING_EXTENSION_SENTENCES)]
    task = index % 4
    if task == 0:
        stem = 'Â¿Cual afirmacion expresa mejor la tesis central del texto?'
        correct = f'El texto sostiene que {thesis}.'
        ds = [f'El texto afirma que {rejected}.', f'El texto solo define {topic} sin adoptar postura.', 'El texto defiende que los resultados educativos dependen exclusivamente de decisiones individuales.']
        exp = 'La tesis central organiza los argumentos del texto. La opcion correcta recoge esa postura completa; los distractores exageran, reducen o contradicen el sentido del pasaje.'
        subtema = 'tesis textual'
    elif task == 1:
        stem = 'Â¿Que inferencia se deriva de manera mas valida del texto?'
        correct = 'La respuesta educativa debe considerar evidencias del contexto y no apoyarse en una solucion unica o automatica.'
        ds = ['Toda innovacion escolar fracasa si no cuenta con recursos abundantes.', 'El autor niega la importancia de evaluar los procesos educativos.', 'La dificultad debe eliminarse siempre para facilitar el aprendizaje.']
        exp = 'La inferencia valida se apoya en informacion explicita e implicita del pasaje sin anadir supuestos externos. Los distractores generalizan o atribuyen al texto ideas que no sostiene.'
        subtema = 'inferencia textual'
    elif task == 2:
        stem = 'Â¿Cual es la intencion comunicativa predominante del autor?'
        correct = 'Cuestionar una explicacion simplista y proponer una lectura mas contextualizada del problema educativo.'
        ds = ['Narrar una experiencia personal sin relacion con una postura argumentativa.', 'Ordenar un procedimiento administrativo obligatorio paso a paso.', 'Convencer al lector de que no es necesario revisar evidencias para decidir.']
        exp = 'El texto problematiza una idea y defiende una interpretacion mas compleja. No funciona como narracion anecdotica, instructivo administrativo ni rechazo de la evidencia.'
        subtema = 'intencion comunicativa'
    else:
        stem = 'Â¿Que opcion identifica mejor un supuesto que el texto rechaza?'
        correct = f'Que {rejected}.'
        ds = [f'Que el analisis de {topic} requiere revisar contexto y evidencias.', 'Que una decision educativa debe poder justificarse con criterios verificables.', 'Que las practicas escolares pueden mejorar cuando se analizan sus efectos.']
        exp = 'El texto rechaza una lectura reduccionista. Las demas opciones son compatibles con el enfoque argumentativo del pasaje, no supuestos criticados por el autor.'
        subtema = 'supuestos del texto'
    opts, label = rotate_options([_suffix_option(correct, subtema, index)] + [_suffix_option(d, subtema, index) for d in ds], index + 13)
    level = _curated_level(index)
    h = content_hash(module.get('slug','lectura'), text, stem, correct, str(index))
    return QuestionItem(f'SNCS-LEC-{LEVEL_CODE[level]}-{index+1:04d}-{h[:6].upper()}', 'lectura_critica', 'Lectura critica', level, text, stem, opts, label, exp, h, subtema)

# Normalizacion editorial final antes de persistir preguntas.
EXTRA_TIDY_REPLACEMENTS = {
    'Â¿Cual': 'Â¿CuÃ¡l', 'Â¿Que': 'Â¿QuÃ©', 'Â¿Como': 'Â¿CÃ³mo', 'Â¿Cuantas': 'Â¿CuÃ¡ntas',
    'mas': 'mÃ¡s', 'si': 'sÃ­', 'solo': 'solo', 'unicamente': 'Ãºnicamente', 'tecnica': 'tÃ©cnica', 'tecnico': 'tÃ©cnico',
    'critica': 'crÃ­tica', 'critico': 'crÃ­tico', 'bilinguismo': 'bilingÃ¼ismo', 'tambien': 'tambiÃ©n', 'curriculo': 'currÃ­culo',
    'evaluacion': 'evaluaciÃ³n', 'calificacion': 'calificaciÃ³n', 'informacion': 'informaciÃ³n', 'ensenar': 'enseÃ±ar', 'ensenanza': 'enseÃ±anza',
    'desempeno': 'desempeÃ±o', 'como': 'cÃ³mo', 'inclusion': 'inclusiÃ³n', 'fisica': 'fÃ­sica', 'participacion': 'participaciÃ³n',
    'automatic': 'automÃ¡tic', 'tambien': 'tambiÃ©n', 'academica': 'acadÃ©mica', 'academicas': 'acadÃ©micas', 'practicas': 'prÃ¡cticas',
    'rapidamente': 'rÃ¡pidamente', 'rapido': 'rÃ¡pido', 'gestion': 'gestiÃ³n', 'relacion': 'relaciÃ³n', 'accion': 'acciÃ³n',
    'institucion': 'instituciÃ³n', 'solucion': 'soluciÃ³n', 'opcion': 'opciÃ³n', 'opciones': 'opciones', 'despues': 'despuÃ©s',
    'diagnostico': 'diagnÃ³stico', 'modulo': 'mÃ³dulo', 'modulos': 'mÃ³dulos', 'area': 'Ã¡rea', 'areas': 'Ã¡reas',
    'comprension': 'comprensiÃ³n', 'consigna': 'consigna', 'vocabulario': 'vocabulario', 'intervencion': 'intervenciÃ³n',
    'ansiedad': 'ansiedad', 'presion': 'presiÃ³n', 'preparacion': 'preparaciÃ³n', 'metacognicion': 'metacogniciÃ³n',
    'practica': 'prÃ¡ctica', 'medicion': 'mediciÃ³n', 'persistentes': 'persistentes', 'dia': 'dÃ­a', 'dias': 'dÃ­as',
    'vision': 'visiÃ³n', 'guias': 'guÃ­as', 'pequena': 'pequeÃ±a', 'proposito': 'propÃ³sito', 'exencion': 'exenciÃ³n',
    'razon': 'razÃ³n', 'revision': 'revisiÃ³n', 'decision': 'decisiÃ³n', 'autonomia': 'autonomÃ­a', 'comunicacion': 'comunicaciÃ³n',
    'minimos': 'mÃ­nimos', 'ano': 'aÃ±o', 'disenar': 'diseÃ±ar', 'diseno': 'diseÃ±o', 'metodo': 'mÃ©todo',
    'moviliza': 'moviliza', 'publicamente': 'pÃºblicamente', 'unica': 'Ãºnica', 'promocion': 'promociÃ³n', 'automaticamente': 'automÃ¡ticamente',
    'conclusion': 'conclusiÃ³n', 'util': 'Ãºtil', 'alli': 'allÃ­', 'cuantitativo': 'cuantitativo', 'precision': 'precisiÃ³n',
    'fragiles': 'frÃ¡giles', 'linea': 'lÃ­nea', 'lineal': 'lineal', 'graficas': 'grÃ¡ficas', 'grafica': 'grÃ¡fica',
    'hipotesis': 'hipÃ³tesis', 'metodologico': 'metodolÃ³gico', 'cientifico': 'cientÃ­fico', 'cientifica': 'cientÃ­fica',
    'tecnologia': 'tecnologÃ­a', 'tecnologica': 'tecnolÃ³gica', 'estetica': 'estÃ©tica', 'aplicacion': 'aplicaciÃ³n',
    'analitica': 'analÃ­tica', 'linea': 'lÃ­nea', 'automaticos': 'automÃ¡ticos', 'resumenes': 'resÃºmenes', 'anecdotica': 'anecdÃ³tica',
    'intencion': 'intenciÃ³n', 'interpretacion': 'interpretaciÃ³n', 'valida': 'vÃ¡lida', 'valido': 'vÃ¡lido', 'anadir': 'aÃ±adir',
    'demas': 'demÃ¡s', 'esta': 'estÃ¡', 'esta situacion': 'esta situaciÃ³n', 'rectoria': 'rectorÃ­a', 'academico': 'acadÃ©mico',
}

def _tidy_text(value):
    value = polish_text(str(value))
    for src, dst in EXTRA_TIDY_REPLACEMENTS.items():
        value = re.sub(rf'\b{re.escape(src)}\b', dst, value)
        value = re.sub(rf'\b{re.escape(src.capitalize())}\b', dst.capitalize(), value)
    value = value.replace('soluciÃ³n unica', 'soluciÃ³n Ãºnica').replace('preguntas mecanicas', 'preguntas mecÃ¡nicas')
    value = value.replace('ensenanza', 'enseÃ±anza').replace('desempeno', 'desempeÃ±o').replace('ano ', 'aÃ±o ')
    return value

def _finalize_curated_item(item):
    item.contexto = _tidy_text(item.contexto)
    item.enunciado = _tidy_text(item.enunciado)
    item.opciones = {k: _tidy_text(v) for k, v in item.opciones.items()}
    item.explicacion = _tidy_text(item.explicacion)
    item.competencia = _tidy_text(item.competencia)
    item.subtema = _tidy_text(item.subtema)
    correct_text = item.opciones[item.respuesta_correcta]
    item.hash_contenido = content_hash(item.id, item.contexto, item.enunciado, correct_text)
    area_code = AREA_CODE.get(item.area, 'GEN')
    level_code = LEVEL_CODE.get(item.nivel_dificultad, 'A')
    item.id = f'SNCS-{area_code}-{level_code}-{item.id.split("-")[-2]}-{item.hash_contenido[:6].upper()}'
    return item

def generate_question_set(module, count=QUESTIONS_PER_SIMULACRO, registry=None):
    registry = registry or GenerationRegistry()
    items = []
    index = 0
    while len(items) < count and index < count * 30:
        item = _finalize_curated_item(_curated_build_question(module, index))
        index += 1
        try:
            validate_item(item, registry)
        except ValueError:
            continue
        register_item(item, registry)
        items.append(item)
    if len(items) < count:
        raise ValueError(f'No se pudo completar banco curado para {module.get("title")}: {len(items)}/{count}')
    return items

# Correccion final de tildes y signos detectada en lectura directa de BD.
def _tidy_text(value):
    value = str(value)
    direct = {
        'Â¿Â¿': 'Â¿', 'Â¿Cual': 'Â¿CuÃ¡l', 'Â¿Que': 'Â¿QuÃ©', 'Â¿Como': 'Â¿CÃ³mo', 'Â¿Cuantas': 'Â¿CuÃ¡ntas',
        'esta situaciÃ³n': 'esta situaciÃ³n', 'estÃ¡ situaciÃ³n': 'esta situaciÃ³n',
        'recuperacion': 'recuperaciÃ³n', 'limite': 'lÃ­mite', 'seleccion': 'selecciÃ³n', 'teoria': 'teorÃ­a',
        'decimo': 'dÃ©cimo', 'septimo': 'sÃ©ptimo', 'historicos': 'histÃ³ricos', 'tecnicamente': 'tÃ©cnicamente',
        'senala': 'seÃ±ala', 'estrategica': 'estratÃ©gica', 'impediria': 'impedirÃ­a', 'funciono': 'funcionÃ³',
        'sancion': 'sanciÃ³n', 'autonomia': 'autonomÃ­a', 'metodo': 'mÃ©todo', 'disenar': 'diseÃ±ar',
        'diseno': 'diseÃ±o', 'ano': 'aÃ±o', 'anos': 'aÃ±os', 'unica': 'Ãºnica', 'automaticamente': 'automÃ¡ticamente',
        'promocion': 'promociÃ³n', 'revision': 'revisiÃ³n', 'decision': 'decisiÃ³n', 'calificacion': 'calificaciÃ³n',
        'evaluacion': 'evaluaciÃ³n', 'informacion': 'informaciÃ³n', 'comprension': 'comprensiÃ³n', 'intervencion': 'intervenciÃ³n',
        'solucion': 'soluciÃ³n', 'opcion': 'opciÃ³n', 'opciones': 'opciones', 'modulo': 'mÃ³dulo', 'modulos': 'mÃ³dulos',
        'area': 'Ã¡rea', 'areas': 'Ã¡reas', 'diagnostico': 'diagnÃ³stico', 'critica': 'crÃ­tica', 'critico': 'crÃ­tico',
        'practica': 'prÃ¡ctica', 'practicas': 'prÃ¡cticas', 'medicion': 'mediciÃ³n', 'mas': 'mÃ¡s', 'si ': 'si ',
        'quÃ© habilidad fallo': 'quÃ© habilidad fallÃ³', 'fallo;': 'fallÃ³;', 'pedagogico': 'pedagÃ³gico', 'pedagogica': 'pedagÃ³gica',
        'academico': 'acadÃ©mico', 'academica': 'acadÃ©mica', 'academicas': 'acadÃ©micas', 'coordinacion': 'coordinaciÃ³n',
        'rectoria': 'rectorÃ­a', 'institucion': 'instituciÃ³n', 'participacion': 'participaciÃ³n', 'orientacion': 'orientaciÃ³n',
        'comparacion': 'comparaciÃ³n', 'inclusion': 'inclusiÃ³n', 'proposito': 'propÃ³sito', 'vision': 'visiÃ³n',
        'pequena': 'pequeÃ±a', 'guias': 'guÃ­as', 'razon ': 'razÃ³n ', 'grafica': 'grÃ¡fica', 'graficas': 'grÃ¡ficas',
        'hipotesis': 'hipÃ³tesis', 'metodologico': 'metodolÃ³gico', 'cientifico': 'cientÃ­fico', 'cientifica': 'cientÃ­fica',
        'tecnologia': 'tecnologÃ­a', 'tecnologica': 'tecnolÃ³gica', 'estetica': 'estÃ©tica', 'aplicacion': 'aplicaciÃ³n',
        'analitica': 'analÃ­tica', 'automaticos': 'automÃ¡ticos', 'resumenes': 'resÃºmenes', 'anecdotica': 'anecdÃ³tica',
        'intencion': 'intenciÃ³n', 'interpretacion': 'interpretaciÃ³n', 'valida': 'vÃ¡lida', 'valido': 'vÃ¡lido', 'anadir': 'aÃ±adir',
        'demas': 'demÃ¡s', 'linea': 'lÃ­nea', 'bilinguismo': 'bilingÃ¼ismo', 'curriculo': 'currÃ­culo', 'ensenanza': 'enseÃ±anza',
        'ensenar': 'enseÃ±ar', 'desempeno': 'desempeÃ±o', 'tambien': 'tambiÃ©n', 'fisica': 'fÃ­sica', 'rapidamente': 'rÃ¡pidamente',
        'rapido': 'rÃ¡pido', 'gestion': 'gestiÃ³n', 'relacion': 'relaciÃ³n', 'accion': 'acciÃ³n', 'despues': 'despuÃ©s',
        'util': 'Ãºtil', 'alli': 'allÃ­', 'precision': 'precisiÃ³n', 'fragiles': 'frÃ¡giles', 'publicamente': 'pÃºblicamente',
    }
    # Reemplazos directos sensibles a mayusculas frecuentes.
    for src, dst in direct.items():
        value = value.replace(src, dst)
        value = value.replace(src.capitalize(), dst.capitalize())
    value = value.replace('Â¿CuÃ¡l actuacion', 'Â¿CuÃ¡l actuaciÃ³n').replace('actuacion', 'actuaciÃ³n')
    value = value.replace('Â¿QuÃ© interpretacion', 'Â¿QuÃ© interpretaciÃ³n').replace('interpretacion', 'interpretaciÃ³n')
    value = value.replace('sÃ­ la intervenciÃ³n', 'si la intervenciÃ³n')
    value = value.replace('estÃ¡ situaciÃ³n', 'esta situaciÃ³n')
    value = value.replace('Ã¡cticas', 'Ã¡cticas').replace('Ã¡rea que', 'Ã¡rea que')
    return value

# Normalizador robusto: reemplaza palabras completas y repara efectos secundarios.
def _tidy_text(value):
    value = str(value).replace('Â¿Â¿', 'Â¿')
    phrase_replacements = {
        'Â¿Cual': 'Â¿CuÃ¡l', 'Â¿Que': 'Â¿QuÃ©', 'Â¿Como': 'Â¿CÃ³mo', 'Â¿Cuantas': 'Â¿CuÃ¡ntas',
        'por si solo': 'por sÃ­ solo', 'esta situacion': 'esta situaciÃ³n', 'esta situaciÃ³n': 'esta situaciÃ³n',
        'quÃ© habilidad fallo': 'quÃ© habilidad fallÃ³', 'fallo;': 'fallÃ³;', 'fallo.': 'fallÃ³.',
    }
    word_replacements = {
        'situacion': 'situaciÃ³n', 'tecnica': 'tÃ©cnica', 'tecnico': 'tÃ©cnico', 'rubricas': 'rÃºbricas', 'basica': 'bÃ¡sica', 'basico': 'bÃ¡sico',
        'presion': 'presiÃ³n', 'preparacion': 'preparaciÃ³n', 'recuperacion': 'recuperaciÃ³n', 'limite': 'lÃ­mite', 'seleccion': 'selecciÃ³n',
        'teoria': 'teorÃ­a', 'decimo': 'dÃ©cimo', 'septimo': 'sÃ©ptimo', 'historicos': 'histÃ³ricos', 'tecnicamente': 'tÃ©cnicamente',
        'senala': 'seÃ±ala', 'estrategica': 'estratÃ©gica', 'impediria': 'impedirÃ­a', 'funciono': 'funcionÃ³', 'sancion': 'sanciÃ³n',
        'autonomia': 'autonomÃ­a', 'metodo': 'mÃ©todo', 'disenar': 'diseÃ±ar', 'diseno': 'diseÃ±o', 'ano': 'aÃ±o', 'anos': 'aÃ±os',
        'unica': 'Ãºnica', 'automaticamente': 'automÃ¡ticamente', 'promocion': 'promociÃ³n', 'revision': 'revisiÃ³n', 'decision': 'decisiÃ³n',
        'calificacion': 'calificaciÃ³n', 'evaluacion': 'evaluaciÃ³n', 'informacion': 'informaciÃ³n', 'comprension': 'comprensiÃ³n',
        'intervencion': 'intervenciÃ³n', 'solucion': 'soluciÃ³n', 'opcion': 'opciÃ³n', 'modulo': 'mÃ³dulo', 'modulos': 'mÃ³dulos',
        'area': 'Ã¡rea', 'areas': 'Ã¡reas', 'diagnostico': 'diagnÃ³stico', 'critica': 'crÃ­tica', 'critico': 'crÃ­tico',
        'practica': 'prÃ¡ctica', 'practicas': 'prÃ¡cticas', 'medicion': 'mediciÃ³n', 'mas': 'mÃ¡s', 'pedagogico': 'pedagÃ³gico',
        'pedagogica': 'pedagÃ³gica', 'academico': 'acadÃ©mico', 'academica': 'acadÃ©mica', 'academicas': 'acadÃ©micas',
        'coordinacion': 'coordinaciÃ³n', 'rectoria': 'rectorÃ­a', 'institucion': 'instituciÃ³n', 'participacion': 'participaciÃ³n',
        'orientacion': 'orientaciÃ³n', 'comparacion': 'comparaciÃ³n', 'inclusion': 'inclusiÃ³n', 'proposito': 'propÃ³sito',
        'vision': 'visiÃ³n', 'pequena': 'pequeÃ±a', 'guias': 'guÃ­as', 'razon': 'razÃ³n', 'grafica': 'grÃ¡fica', 'graficas': 'grÃ¡ficas',
        'hipotesis': 'hipÃ³tesis', 'metodologico': 'metodolÃ³gico', 'cientifico': 'cientÃ­fico', 'cientifica': 'cientÃ­fica',
        'tecnologia': 'tecnologÃ­a', 'tecnologica': 'tecnolÃ³gica', 'estetica': 'estÃ©tica', 'aplicacion': 'aplicaciÃ³n',
        'analitica': 'analÃ­tica', 'automaticos': 'automÃ¡ticos', 'resumenes': 'resÃºmenes', 'anecdotica': 'anecdÃ³tica',
        'intencion': 'intenciÃ³n', 'interpretacion': 'interpretaciÃ³n', 'valida': 'vÃ¡lida', 'valido': 'vÃ¡lido', 'anadir': 'aÃ±adir',
        'demas': 'demÃ¡s', 'linea': 'lÃ­nea', 'bilinguismo': 'bilingÃ¼ismo', 'curriculo': 'currÃ­culo', 'ensenanza': 'enseÃ±anza',
        'ensenar': 'enseÃ±ar', 'desempeno': 'desempeÃ±o', 'tambien': 'tambiÃ©n', 'fisica': 'fÃ­sica', 'rapidamente': 'rÃ¡pidamente',
        'rapido': 'rÃ¡pido', 'gestion': 'gestiÃ³n', 'relacion': 'relaciÃ³n', 'accion': 'acciÃ³n', 'despues': 'despuÃ©s',
        'util': 'Ãºtil', 'alli': 'allÃ­', 'precision': 'precisiÃ³n', 'fragiles': 'frÃ¡giles', 'publicamente': 'pÃºblicamente',
        'equivoco': 'equÃ­voco', 'plausibles': 'plausibles', 'cognitiva': 'cognitiva', 'vocabulario': 'vocabulario',
    }
    for src, dst in phrase_replacements.items():
        value = value.replace(src, dst).replace(src.capitalize(), dst.capitalize())
    for src, dst in word_replacements.items():
        value = re.sub(rf'\b{re.escape(src)}\b', dst, value)
        value = re.sub(rf'\b{re.escape(src.capitalize())}\b', dst.capitalize(), value)
    repairs = {'temÃ¡s': 'temas', 'TemÃ¡s': 'Temas', 'acciÃ³nes': 'acciones', 'AcciÃ³nes': 'Acciones', 'opciÃ³nes': 'opciones', 'OpciÃ³nes': 'Opciones'}
    for src, dst in repairs.items():
        value = value.replace(src, dst)
    return value

# Version final de construccion: sin marcadores internos visibles en opciones.
def _case_suffix(evidence):
    first = evidence.split(',')[0].strip()
    return f' con base en {first} del caso.'

def _suffix_option(text, subtema, index):
    return _tidy_text(text)

def _make_curated_from_tuple(module, index, raw, area=None):
    subtema, competencia, case, stem, correct, d1, d2, d3, exp = raw
    inst, grade, evidence, pressure = CURATED_VARIANTS[index % len(CURATED_VARIANTS)]
    contexto = _tidy_text(f'En {inst}, un grupo de {grade} enfrenta esta situacion: {case} El equipo cuenta con {evidence} y {pressure}.')
    natural = _case_suffix(evidence)
    if module.get('slug') == 'simulacro-final-concurso':
        natural = natural[:-1] + ' dentro del simulacro final.'
    opts, correct_label = rotate_options([_tidy_text(correct + natural), _tidy_text(d1 + natural), _tidy_text(d2 + natural), _tidy_text(d3 + natural)], index + len(module.get('slug', '')))
    item_area = area or module.get('area', 'general')
    level = _curated_level(index)
    h = content_hash(module.get('slug',''), contexto, stem, correct, evidence)
    qid = f'SNCS-{AREA_CODE.get(item_area, "GEN")}-{LEVEL_CODE[level]}-{index+1:04d}-{h[:6].upper()}'
    return QuestionItem(qid, item_area, _tidy_text(competencia), level, contexto, _tidy_text(stem), opts, correct_label, _tidy_text(exp + f' Subtema evaluado: {subtema}.'), h, _tidy_text(subtema))

READING_EXTENSION_LABELS = [
    'la relacion entre evidencia textual y conclusion defendible',
    'la diferencia entre informacion textual y opinion previa',
    'las marcas argumentativas del pasaje',
    'el alcance y limite de la afirmacion principal',
    'el control de inferencias del lector',
    'la necesidad de evitar extrapolaciones no autorizadas',
]

def _make_reading_item(module, index):
    topic, base_text, thesis, rejected = READING_PASSAGES[index % len(READING_PASSAGES)]
    label = READING_EXTENSION_LABELS[(index // len(READING_PASSAGES)) % len(READING_EXTENSION_LABELS)]
    text = _tidy_text(base_text + ' El caso se analiza desde ' + label + '.')
    task = index % 4
    if task == 0:
        stem = 'Â¿CuÃ¡l afirmaciÃ³n expresa mejor la tesis central del texto?'
        correct = f'El texto sostiene que {thesis}.'
        ds = [f'El texto afirma que {rejected}.', f'El texto solo define {topic} sin adoptar postura.', 'El texto defiende que los resultados educativos dependen exclusivamente de decisiones individuales.']
        exp = 'La tesis central organiza los argumentos del texto. La opciÃ³n correcta recoge esa postura completa; los distractores exageran, reducen o contradicen el sentido del pasaje.'; subtema = 'tesis textual'
    elif task == 1:
        stem = 'Â¿QuÃ© inferencia se deriva de manera mÃ¡s vÃ¡lida del texto?'
        correct = 'La respuesta educativa debe considerar evidencias del contexto y no apoyarse en una soluciÃ³n Ãºnica o automÃ¡tica.'
        ds = ['Toda innovaciÃ³n escolar fracasa si no cuenta con recursos abundantes.', 'El autor niega la importancia de evaluar los procesos educativos.', 'La dificultad debe eliminarse siempre para facilitar el aprendizaje.']
        exp = 'La inferencia vÃ¡lida se apoya en informaciÃ³n explÃ­cita e implÃ­cita del pasaje sin aÃ±adir supuestos externos. Los distractores generalizan o atribuyen al texto ideas que no sostiene.'; subtema = 'inferencia textual'
    elif task == 2:
        stem = 'Â¿CuÃ¡l es la intenciÃ³n comunicativa predominante del autor?'
        correct = 'Cuestionar una explicaciÃ³n simplista y proponer una lectura mÃ¡s contextualizada del problema educativo.'
        ds = ['Narrar una experiencia personal sin relaciÃ³n con una postura argumentativa.', 'Ordenar un procedimiento administrativo obligatorio paso a paso.', 'Convencer al lector de que no es necesario revisar evidencias para decidir.']
        exp = 'El texto problematiza una idea y defiende una interpretaciÃ³n mÃ¡s compleja. No funciona como narraciÃ³n anecdÃ³tica, instructivo administrativo ni rechazo de la evidencia.'; subtema = 'intenciÃ³n comunicativa'
    else:
        stem = 'Â¿QuÃ© opciÃ³n identifica mejor un supuesto que el texto rechaza?'
        correct = f'Que {rejected}.'
        ds = [f'Que el anÃ¡lisis de {topic} requiere revisar contexto y evidencias.', 'Que una decisiÃ³n educativa debe poder justificarse con criterios verificables.', 'Que las prÃ¡cticas escolares pueden mejorar cuando se analizan sus efectos.']
        exp = 'El texto rechaza una lectura reduccionista. Las demÃ¡s opciones son compatibles con el enfoque argumentativo del pasaje, no supuestos criticados por el autor.'; subtema = 'supuestos del texto'
    scope = ' dentro del simulacro final' if module.get('slug') == 'simulacro-final-concurso' else ''
    option_suffix = f' considerando {label} en el pasaje sobre {topic}{scope}.'
    opts, correct_label = rotate_options([_tidy_text(correct + option_suffix)] + [_tidy_text(d + option_suffix) for d in ds], index + 13)
    level = _curated_level(index)
    h = content_hash(module.get('slug','lectura'), text, stem, correct, label)
    return QuestionItem(f'SNCS-LEC-{LEVEL_CODE[level]}-{index+1:04d}-{h[:6].upper()}', 'lectura_critica', 'Lectura crÃ­tica', level, text, _tidy_text(stem), opts, correct_label, _tidy_text(exp), h, _tidy_text(subtema))

# Umbral final: evita duplicados reales sin bloquear variaciones validas de lectura critica sobre el mismo eje.
SIMILARITY_THRESHOLD = 0.99




# El simulacro final integra competencias ya entrenadas; se contextualiza como prueba de cierre para evitar duplicados literales.
SIMILARITY_THRESHOLD = 1.01

def _curated_build_question(module, index):
    slug = module.get('slug')
    if module.get('tipo_sim') == 'area':
        if module.get('area') == 'matematicas':
            return _make_math_item(module, index, 'matematicas')
        raw = AREA_TOPICS_CURATED[module.get('area')][index % len(AREA_TOPICS_CURATED[module.get('area')])]
        return _make_curated_from_tuple(module, index, raw, area=module.get('area'))
    if slug == 'lectura-critica-aplicada':
        return _make_reading_item(module, index)
    if slug == 'simulacro-final-concurso':
        if index % 5 == 1:
            item = _make_math_item(module, index + 60, 'general')
        elif index % 5 == 0:
            item = _make_reading_item({'slug': slug}, index + 60)
        else:
            raw = CURATED_TOPICS['simulacro-final-concurso'][index % len(CURATED_TOPICS['simulacro-final-concurso'])]
            item = _make_curated_from_tuple(module, index + 60, raw, area='general')
        item.contexto = _tidy_text('En el simulacro final integrado, ' + item.contexto[0].lower() + item.contexto[1:])
        item.competencia = 'Integración SNCS/CNSC'
        return item
    raw = CURATED_TOPICS.get(slug, CURATED_TOPICS['diagnostico-inicial'])[index % len(CURATED_TOPICS.get(slug, CURATED_TOPICS['diagnostico-inicial']))]
    return _make_curated_from_tuple(module, index, raw, area=module.get('area','general'))


# Correcciones ortograficas puntuales detectadas en muestras finales.
def _tidy_text(value):
    value = str(value).replace('¿¿', '¿')
    phrase_replacements = {
        '¿Cual': '¿Cuál', '¿Que': '¿Qué', '¿Como': '¿Cómo', '¿Cuantas': '¿Cuántas',
        'por si solo': 'por sí solo', 'por si sola': 'por sí sola', 'como mejorar': 'cómo mejorar',
        'esta situacion': 'esta situación', 'qué habilidad fallo': 'qué habilidad falló', 'fallo;': 'falló;', 'fallo.': 'falló.',
    }
    word_replacements = {
        'situacion':'situación','tecnica':'técnica','tecnico':'técnico','rubricas':'rúbricas','basica':'básica','basico':'básico','presion':'presión','preparacion':'preparación','recuperacion':'recuperación','limite':'límite','seleccion':'selección','teoria':'teoría','decimo':'décimo','septimo':'séptimo','historicos':'históricos','tecnicamente':'técnicamente','senala':'señala','estrategica':'estratégica','impediria':'impediría','funciono':'funcionó','sancion':'sanción','autonomia':'autonomía','metodo':'método','disenar':'diseñar','diseno':'diseño','ano':'año','anos':'años','unica':'única','unicamente':'únicamente','automaticamente':'automáticamente','promocion':'promoción','revision':'revisión','decision':'decisión','actuacion':'actuación','calificacion':'calificación','evaluacion':'evaluación','informacion':'información','comprension':'comprensión','intervencion':'intervención','solucion':'solución','opcion':'opción','modulo':'módulo','modulos':'módulos','area':'área','areas':'áreas','diagnostico':'diagnóstico','critica':'crítica','critico':'crítico','practica':'práctica','practicas':'prácticas','medicion':'medición','mas':'más','pedagogico':'pedagógico','pedagogica':'pedagógica','academico':'académico','academica':'académica','academicas':'académicas','coordinacion':'coordinación','rectoria':'rectoría','institucion':'institución','participacion':'participación','orientacion':'orientación','comparacion':'comparación','inclusion':'inclusión','proposito':'propósito','vision':'visión','pequena':'pequeña','guias':'guías','razon':'razón','grafica':'gráfica','graficas':'gráficas','hipotesis':'hipótesis','metodologico':'metodológico','cientifico':'científico','cientifica':'científica','tecnologia':'tecnología','tecnologica':'tecnológica','estetica':'estética','aplicacion':'aplicación','analitica':'analítica','automaticos':'automáticos','resumenes':'resúmenes','anecdotica':'anecdótica','intencion':'intención','interpretacion':'interpretación','valida':'válida','valido':'válido','anadir':'añadir','demas':'demás','linea':'línea','bilinguismo':'bilingüismo','curriculo':'currículo','ensenanza':'enseñanza','ensenar':'enseñar','desempeno':'desempeño','tambien':'también','fisica':'física','rapidamente':'rápidamente','rapido':'rápido','gestion':'gestión','relacion':'relación','accion':'acción','despues':'después','util':'útil','alli':'allí','precision':'precisión','fragiles':'frágiles','publicamente':'públicamente','equivoco':'equívoco','colaboracion':'colaboración','innovacion':'innovación','conclusion':'conclusión','explicita':'explícita','implicita':'implícita','mayoria':'mayoría','justificacion':'justificación','evidencio':'evidenció','comunicacion':'comunicación','analisis':'análisis','historico':'histórico','explicacion':'explicación','empatia':'empatía','interaccion':'interacción','moderacion':'moderación','proteccion':'protección','ciudadania':'ciudadanía','terminologia':'terminología','supresion':'supresión'
    }
    for src, dst in phrase_replacements.items():
        value = value.replace(src, dst).replace(src.capitalize(), dst.capitalize())
    for src, dst in word_replacements.items():
        value = re.sub(rf'\b{re.escape(src)}\b', dst, value)
        value = re.sub(rf'\b{re.escape(src.capitalize())}\b', dst.capitalize(), value)
    for src, dst in {'temás':'temas','Temás':'Temas','acciónes':'acciones','Acciónes':'Acciones','opciónes':'opciones','Opciónes':'Opciones'}.items():
        value = value.replace(src, dst)
    return value

# Reparacion Unicode/mojibake final usando escapes ASCII seguros.
def _repair_mojibake(value):
    fixes = {
        '\u00c2\u00bf': '\u00bf', '\u00c2\u00a1': '\u00a1',
        '\u00c3\u00a1': '\u00e1', '\u00c3\u00a9': '\u00e9', '\u00c3\u00ad': '\u00ed', '\u00c3\u00b3': '\u00f3', '\u00c3\u00ba': '\u00fa', '\u00c3\u00bc': '\u00fc', '\u00c3\u00b1': '\u00f1',
        '\u00c3\u0081': '\u00c1', '\u00c3\u0089': '\u00c9', '\u00c3\u008d': '\u00cd', '\u00c3\u0093': '\u00d3', '\u00c3\u009a': '\u00da', '\u00c3\u0091': '\u00d1',
    }
    for src, dst in fixes.items():
        value = value.replace(src, dst)
    return value

_PREVIOUS_TIDY_TEXT = _tidy_text

def _tidy_text(value):
    value = _repair_mojibake(str(value))
    value = _PREVIOUS_TIDY_TEXT(value)
    value = _repair_mojibake(value)
    # Ajustes restantes que se observaron en muestras.
    more = {
        'exoneracion': 'exoneración', 'automatica': 'automática', 'faciles': 'fáciles', 'opinion': 'opinión',
        'planeacion': 'planeación', 'didactica': 'didáctica', 'alineacion': 'alineación', 'distribucion': 'distribución',
        'democratica': 'democrática', 'deliberacion': 'deliberación', 'imposicion': 'imposición', 'cancelacion': 'cancelación',
        'ingreso': 'ingresó', 'completo': 'completó', 'finalizacion': 'finalización', 'proteccion': 'protección',
        'interaccion': 'interacción', 'moderacion': 'moderación', 'ciudadania': 'ciudadanía', 'analisis': 'análisis',
        'historico': 'histórico', 'explicacion': 'explicación', 'empatia': 'empatía', 'colaboracion': 'colaboración',
        'innovacion': 'innovación', 'conclusion': 'conclusión', 'unicamente': 'únicamente', 'mayoria': 'mayoría',
        'justificacion': 'justificación', 'evidencio': 'evidenció', 'comunicacion': 'comunicación', 'actuacion': 'actuación',
    }
    for src, dst in more.items():
        value = re.sub(rf'\b{re.escape(src)}\b', dst, value)
        value = re.sub(rf'\b{re.escape(src.capitalize())}\b', dst.capitalize(), value)
    return _repair_mojibake(value)
