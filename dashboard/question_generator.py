"""Catalogo de modulos y utilidades de similitud de texto.

Historicamente este archivo tambien contenia un generador mecanico de
preguntas curadas (build_question/generate_question_set/CURATED_TOPICS y
~500 lineas de datos asociados). Ese generador nunca se invocaba desde
ningun otro punto del codigo (fue reemplazado por el proceso real de
construccion de items) y se elimino en la limpieza de codigo muerto
aprobada junto con la auditoria tecnica de la plataforma. Lo que queda
aqui es exactamente lo que si esta en uso: el catalogo de los 11 modulos
(fuente de verdad para apply_market_ready_upgrade) y las utilidades de
normalizacion/similitud que usa check_premium_ready.
"""

import re

ELITE_SLUG = 'elite-cnsc-2026'
AREA_MODULE_SLUG = 'simulacros-por-area'
QUESTION_CATEGORY = 'Banco Curado SNCS/CNSC 2026'
SIMILARITY_THRESHOLD = 0.92

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


def normalize(value: str) -> str:
    value = value.lower()
    value = re.sub(r'[^a-záéíóúüñ0-9\s]', ' ', value)
    return re.sub(r'\s+', ' ', value).strip()


def token_set(value: str) -> set:
    stop = {'que', 'para', 'con', 'una', 'del', 'los', 'las', 'por', 'como', 'debe', 'de', 'la', 'el', 'en', 'al', 'se'}
    return {t for t in normalize(value).split() if len(t) > 3 and t not in stop}


def jaccard(a: set, b: set) -> float:
    return len(a & b) / len(a | b) if a and b else 0.0
