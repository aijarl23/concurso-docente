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
        'slug': 'diagnostico-inicial', 'tipo': 'diagnostico_inicial', 'title': 'Diagnóstico inicial',
        'area': 'general', 'competencia': 'Diagnóstico integral', 'tipo_sim': 'diagnostico',
        'description': 'Identifica brechas de lectura, pedagogía, normativa, juicio situacional y razonamiento aplicado antes de iniciar la ruta.',
        'topics': ['Mapa de fortalezas y brechas', 'Lectura de consignas', 'Toma de decisiones inicial', 'Uso de resultados para plan de mejora'],
    },
    {
        'slug': 'lectura-critica-aplicada', 'tipo': 'lectura_critica_aplicada', 'title': 'Lectura crítica aplicada',
        'area': 'lectura_critica', 'competencia': 'Lectura crítica', 'tipo_sim': 'tematico',
        'description': 'Entrena inferencia, intención comunicativa, estructura argumentativa y evaluación de evidencia en textos complejos.',
        'topics': ['Inferencia y supuestos', 'Tesis y argumentos', 'Intención del autor', 'Evaluación de evidencia'],
    },
    {
        'slug': 'competencias-pedagogicas', 'tipo': 'competencias_pedagogicas', 'title': 'Competencias pedagógicas',
        'area': 'componente_pedagogico', 'competencia': 'Pedagogía y didáctica', 'tipo_sim': 'tematico',
        'description': 'Casos de planeación, evaluación formativa, inclusión, didáctica y gestión del aula con criterio profesional docente.',
        'topics': ['Planeación curricular', 'Evaluación formativa', 'Inclusión y DUA', 'Didáctica situada'],
    },
    {
        'slug': 'competencias-comportamentales-tjs', 'tipo': 'competencias_tjs', 'title': 'Competencias comportamentales / TJS',
        'area': 'psicotecnico', 'competencia': 'Juicio situacional docente', 'tipo_sim': 'tjs',
        'description': 'Situaciones de convivencia, liderazgo, comunicación, trabajo en equipo e iniciativa en contexto escolar.',
        'topics': ['Comunicación asertiva', 'Liderazgo', 'Trabajo en equipo', 'Orientación al logro'],
    },
    {
        'slug': 'normativa-contexto-docente', 'tipo': 'normativa_contexto', 'title': 'Normativa y contexto docente',
        'area': 'general', 'competencia': 'Normativa educativa aplicada', 'tipo_sim': 'tematico',
        'description': 'Aplicación contextual de Decreto 1278, Ley 115, inclusión, convivencia escolar y funciones docentes.',
        'topics': ['Estatuto docente', 'Ley General de Educación', 'Convivencia escolar', 'Inclusión y ajustes razonables'],
    },
    {
        'slug': 'simulacros-por-area', 'tipo': 'simulacros_area', 'title': 'Simulacros por área',
        'area': 'matematicas', 'competencia': 'Razonamiento cuantitativo aplicado', 'tipo_sim': 'area',
        'description': 'Entrenamiento disciplinar y razonamiento cuantitativo con gráficas, tablas, proporciones y datos escolares.',
        'topics': ['Razonamiento cuantitativo', 'Matemáticas aplicadas', 'Interpretación de datos', 'Problemas contextualizados'],
    },
    {
        'slug': 'simulacro-final-concurso', 'tipo': 'simulacro_final', 'title': 'Simulacro final tipo concurso',
        'area': 'general', 'competencia': 'Integración CNSC', 'tipo_sim': 'elite',
        'description': 'Prueba integral con mezcla de competencias, lectura crítica, pedagogía, normativa, TJS y razonamiento aplicado.',
        'topics': ['Gestión del tiempo', 'Integración de competencias', 'Análisis de resultados', 'Estrategia de cierre'],
    },
    {
        'slug': 'reporte-progreso-plan-mejora', 'tipo': 'reporte_mejora', 'title': 'Reporte de progreso y plan de mejora',
        'area': 'general', 'competencia': 'Metacognición y mejora', 'tipo_sim': 'tematico',
        'description': 'Analiza desempeño, prioriza brechas y convierte resultados de simulacros en decisiones concretas de estudio.',
        'topics': ['Lectura de resultados', 'Priorización de brechas', 'Plan semanal', 'Seguimiento de mejora'],
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


CASES_BY_MODULE = {
    'diagnostico-inicial': [
        ('En la primera semana de preparación, una docente obtiene resultados altos en normativa, pero bajos en lectura inferencial y análisis de casos.',
         'El reporte muestra que responde rápido las preguntas literales, aunque falla cuando debe justificar una decisión pedagógica a partir de varios datos.',
         'La dificultad no parece estar en desconocer contenidos, sino en integrar información y priorizar evidencias.'),
        ('Un aspirante revisa tres simulacros y descubre que sus errores se concentran en preguntas con enunciados negativos o alternativas parcialmente correctas.',
         'En sus apuntes marca como "tema no aprendido" asuntos que sí domina, porque no distingue entre error conceptual y error de lectura de consigna.',
         'Antes de estudiar más material, necesita interpretar el origen real de sus fallos.'),
        ('Un grupo de estudio decide iniciar por el módulo más popular, aunque sus resultados diagnósticos muestran brechas diferentes entre sus integrantes.',
         'Algunos requieren fortalecer razonamiento cuantitativo; otros necesitan mejorar juicio situacional y lectura crítica.',
         'El reto es construir una ruta común sin invisibilizar necesidades individuales.'),
        ('Una aspirante obtiene 62 % en el diagnóstico, pero al revisar las respuestas nota que varias opciones descartadas contenían pistas relevantes.',
         'El resultado global no permite saber si el problema principal fue tiempo, ansiedad, lectura superficial o falta de dominio conceptual.',
         'La decisión de mejora debe partir de evidencias más finas que el puntaje total.'),
        ('Después de un simulacro inicial, un docente decide repetir preguntas hasta memorizar respuestas.',
         'Su desempeño mejora en los ítems conocidos, pero baja cuando enfrenta casos nuevos con estructura semejante.',
         'La preparación debe diferenciar reconocimiento de patrones y comprensión transferible.'),
    ],
    'lectura-critica-aplicada': [
        ('Un texto editorial sostiene que la calidad educativa depende de más tecnología, pero solo presenta ejemplos de instituciones urbanas con alta conectividad.',
         'El autor usa un tono convincente y cifras aisladas, aunque no explica si la mejora proviene de la tecnología, de la formación docente o de otras condiciones institucionales.',
         'La lectura exige valorar la relación entre tesis, evidencia y alcance de la conclusión.'),
        ('Un informe escolar afirma que el bajo desempeño lector se debe a falta de interés estudiantil.',
         'Sin embargo, el mismo documento muestra cambios frecuentes de docentes, escaso acceso a biblioteca y evaluaciones centradas en copia literal.',
         'El lector debe identificar qué interpretación está mejor sustentada por el conjunto de datos.'),
        ('Una columna defiende reducir tareas para mejorar bienestar, pero omite distinguir entre tareas mecánicas y actividades de profundización.',
         'El texto apela a experiencias familiares y presenta una conclusión general a partir de casos particulares.',
         'La pregunta no busca opinión personal, sino análisis de supuestos y límites argumentativos.'),
        ('Un comunicado institucional invita a "innovar" y asocia innovación con uso permanente de plataformas digitales.',
         'No se mencionan objetivos de aprendizaje, criterios de evaluación ni condiciones de acceso de estudiantes rurales.',
         'El problema central está en inferir qué falta para que la propuesta sea pedagógicamente sólida.'),
        ('Un artículo sobre convivencia escolar plantea que toda sanción deteriora el clima institucional.',
         'El texto no considera prácticas restaurativas ni diferencia castigo arbitrario de consecuencia formativa.',
         'La lectura crítica exige reconocer una generalización que simplifica el problema.'),
    ],
    'competencias-pedagogicas': [
        ('En una planeación de Ciencias Naturales, las actividades son llamativas, pero no se observa relación clara entre desempeño esperado, evidencia de aprendizaje y criterios de evaluación.',
         'Los estudiantes elaboran carteleras y exposiciones, aunque la rúbrica solo califica presentación visual y cumplimiento de entrega.',
         'La revisión pedagógica debe centrarse en la coherencia interna de la secuencia.'),
        ('Una docente detecta que varios estudiantes resuelven ejercicios cuando siguen un ejemplo, pero no explican el procedimiento ni lo aplican a situaciones nuevas.',
         'El plan de refuerzo propone aumentar la cantidad de ejercicios iguales durante dos semanas.',
         'La decisión debe valorar si la estrategia fortalece comprensión o solo repetición.'),
        ('Un estudiante con barreras de participación entrega productos incompletos, pero evidencia avances orales y trabajo colaborativo.',
         'El equipo debate si debe mantener exactamente la misma evidencia escrita para todos o ajustar medios sin reducir el nivel esperado.',
         'La respuesta exige comprender inclusión como acceso al aprendizaje, no como disminución automática de exigencia.'),
        ('En una evaluación de periodo, la mayoría reprueba una pregunta que combinaba lectura de gráfica y explicación causal.',
         'El docente concluye que el grupo "no estudió", aunque durante las clases se trabajaron fórmulas sin interpretación de datos.',
         'El análisis pedagógico debe revisar la alineación entre enseñanza, evaluación y desempeño solicitado.'),
        ('Un área acuerda usar evaluación formativa, pero en la práctica solo entrega notas numéricas al final de cada unidad.',
         'Los estudiantes no reciben criterios previos ni oportunidades de mejora sobre evidencias parciales.',
         'La situación obliga a distinguir evaluación formativa de simple acumulación de calificaciones.'),
    ],
    'competencias-comportamentales-tjs': [
        ('Durante una reunión, una madre acusa públicamente a un docente de favorecer a algunos estudiantes.',
         'El docente tiene registros de retroalimentación, pero la conversación se torna emocional y otros padres empiezan a intervenir.',
         'La respuesta debe proteger la comunicación, la dignidad de las partes y la trazabilidad institucional.'),
        ('Un estudiante difunde en redes un comentario ofensivo contra un compañero.',
         'El grupo pide una sanción inmediata y la familia del agresor minimiza el hecho como una broma.',
         'La actuación esperada debe equilibrar prevención, reparación y corresponsabilidad.'),
        ('Dos docentes discrepan sobre la adaptación de una actividad para un estudiante con discapacidad.',
         'Uno considera que cualquier ajuste es injusto; el otro propone eliminar casi todo el reto académico.',
         'La decisión requiere liderazgo pedagógico y construcción de acuerdos con fundamento.'),
        ('La coordinación solicita resultados rápidos en una estrategia de lectura, pero el equipo docente advierte que no hay línea base ni seguimiento.',
         'Algunos proponen reportar avances generales para evitar cuestionamientos.',
         'El juicio situacional exige actuar con transparencia y orientación al mejoramiento.'),
        ('Un docente nuevo recibe críticas porque sus clases son diferentes a las prácticas tradicionales del área.',
         'Tiene evidencias de participación y aprendizaje, pero aún no las ha socializado con sus colegas.',
         'La respuesta debe fortalecer trabajo en equipo sin renunciar al criterio pedagógico.'),
    ],
    'normativa-contexto-docente': [
        ('Una institución debe responder a la solicitud de ajustes razonables para un estudiante con discapacidad.',
         'La familia aporta recomendaciones médicas y los docentes tienen evidencias de participación, pero no existe un plan formal documentado.',
         'La decisión debe articular derecho a la educación, corresponsabilidad y seguimiento.'),
        ('Un comité analiza un caso de convivencia que afecta a varios cursos.',
         'Algunos miembros quieren resolverlo solo con suspensión; otros proponen una charla general sin registro ni compromisos.',
         'El marco normativo exige una respuesta proporcional, documentada y preventiva.'),
        ('Un docente en periodo de prueba recibe observaciones sobre planeación, seguimiento y relación con la comunidad.',
         'El informe mezcla hechos verificables con apreciaciones generales no sustentadas.',
         'La lectura normativa requiere diferenciar evidencia, función docente y debido proceso.'),
        ('La rectoría solicita ajustar el plan de estudios por bajo desempeño en pruebas externas.',
         'La propuesta inicial reduce áreas artísticas y proyectos transversales sin análisis curricular suficiente.',
         'La decisión debe considerar fines de la educación, formación integral y pertinencia institucional.'),
        ('Una sede rural reporta dificultades de conectividad para cumplir actividades digitales obligatorias.',
         'La institución exige el mismo formato de entrega para todos, aunque conoce barreras de acceso persistentes.',
         'La respuesta normativa debe evitar exclusión y garantizar alternativas equivalentes.'),
    ],
    'simulacros-por-area': [
        ('En un informe de Matemáticas, el grupo A obtuvo 18 aciertos promedio y el grupo B obtuvo 15.',
         'El grupo A tenía 20 estudiantes y el B tenía 9; además, las preguntas con mayor error exigían interpretar una tabla, no solo calcular.',
         'La conclusión debe evitar comparar valores aislados sin considerar proporciones ni tipo de demanda cognitiva.'),
        ('Una gráfica muestra aumento del 40 % en participación de una estrategia científica escolar.',
         'El año anterior participaron 5 estudiantes y este año 7; el informe presenta el resultado como evidencia de impacto masivo.',
         'La interpretación exige reconocer cómo la base de comparación afecta la lectura del porcentaje.'),
        ('En una prueba de Ciencias Naturales, varios estudiantes predicen correctamente un fenómeno, pero no justifican la relación causal.',
         'El docente duda si el problema es conceptual, comunicativo o de lectura de la consigna.',
         'La pregunta evalúa razonamiento disciplinar aplicado al análisis de evidencia.'),
        ('Un texto en inglés describe una situación escolar y pide inferir la intención de un aviso institucional.',
         'La mayoría traduce palabras sueltas, pero falla al reconocer propósito, destinatario y contexto.',
         'La competencia evaluada no es memorización de vocabulario, sino comprensión funcional.'),
        ('Un proyecto de tecnología propone usar una aplicación para reportar asistencia.',
         'La sede con menor asistencia es la que tiene menor conectividad y menor disponibilidad de dispositivos.',
         'La solución debe analizar el problema antes de suponer que la herramienta digital lo resuelve.'),
    ],
    'simulacro-final-concurso': [
        ('En una sola situación institucional confluyen bajo desempeño lector, conflicto de aula y presión por resultados externos.',
         'El equipo cuenta con datos parciales, actas de seguimiento y testimonios de estudiantes, pero no con una explicación única.',
         'La respuesta debe integrar lectura crítica, pedagogía, normativa y juicio situacional.'),
        ('Una institución adopta un plan de mejora con muchas actividades, pero sin responsables, indicadores ni momentos de revisión.',
         'El documento tiene lenguaje técnico y buena presentación, aunque no permite verificar avances reales.',
         'La evaluación del caso exige distinguir formulación aparente de gestión efectiva.'),
        ('Un docente recibe resultados bajos en una competencia y decide estudiar solo resúmenes normativos.',
         'Sus errores, sin embargo, aparecen en casos donde debía priorizar acciones y justificar decisiones.',
         'La situación demanda elegir una estrategia de mejora coherente con la evidencia.'),
        ('Un comité escolar revisa una política institucional que busca mejorar convivencia y aprendizaje.',
         'El texto combina principios amplios con medidas concretas, algunas de las cuales no tienen relación directa con el problema diagnosticado.',
         'La tarea consiste en reconocer pertinencia, coherencia y efectos previsibles.'),
        ('Una prueba final incluye textos extensos, tablas, situaciones de aula y dilemas de actuación docente.',
         'El aspirante responde primero lo que recuerda, pero deja para el final las preguntas que exigían mayor análisis.',
         'La estrategia de prueba debe equilibrar tiempo, dificultad y lectura cuidadosa.'),
    ],
    'reporte-progreso-plan-mejora': [
        ('Tras cuatro simulacros, una aspirante mejora en velocidad, pero mantiene errores en preguntas de inferencia y opciones con matices.',
         'El reporte general muestra avance, aunque las justificaciones evidencian que sigue eligiendo respuestas por palabras clave.',
         'El plan de mejora debe atacar la causa del error, no solo aumentar horas de estudio.'),
        ('Un docente obtiene bajo puntaje en TJS, pero las respuestas muestran que identifica el problema y falla al ordenar la actuación institucional.',
         'El análisis por competencia permite diferenciar sensibilidad ética, comunicación y seguimiento.',
         'La intervención debe ser más precisa que repetir simulacros completos.'),
        ('El registro semanal muestra que un aspirante estudia muchas horas, pero no revisa por qué se equivoca.',
         'Sus notas contienen listas de temas, no patrones de error ni decisiones de ajuste.',
         'El progreso exige convertir resultados en información accionable.'),
        ('Una usuaria compra un módulo individual y obtiene buen resultado inicial.',
         'El sistema detecta que aún no ha practicado normativa aplicada ni razonamiento cuantitativo.',
         'La recomendación debe orientar continuidad sin asumir que un buen puntaje parcial equivale a preparación integral.'),
        ('Después de revisar resultados, un grupo decide cambiar todo su plan cada vez que baja el puntaje.',
         'Las variaciones entre simulacros son pequeñas y algunas se explican por tiempo usado o dificultad del texto.',
         'La lectura del progreso debe evitar conclusiones apresuradas a partir de datos aislados.'),
    ],
}

TASKS = [
    ('inferencia', '¿Cuál inferencia se sustenta mejor en la información del caso?'),
    ('decision', '¿Qué decisión resulta más pertinente desde el criterio profesional docente?'),
    ('riesgo', '¿Qué riesgo metodológico o pedagógico debe evitarse principalmente?'),
    ('evidencia', '¿Qué uso de la evidencia permite una conclusión más válida?'),
    ('prioridad', '¿Cuál debería ser la prioridad de intervención?'),
    ('mejora', '¿Qué acción convertiría el resultado en una mejora verificable?'),
]

GOOD_OPTIONS = {
    'inferencia': 'El problema no puede explicarse por una sola causa; requiere relacionar evidencias, contexto y demanda cognitiva antes de concluir.',
    'decision': 'Tomar una decisión proporcional, documentada y orientada al aprendizaje, con comunicación clara y seguimiento verificable.',
    'riesgo': 'Reducir el caso a una lectura inmediata, ya sea por presión externa, memoria normativa o interpretación aislada de un dato.',
    'evidencia': 'Contrastar datos cuantitativos y cualitativos, revisar su alcance y usarlos para justificar una intervención pertinente.',
    'prioridad': 'Atender primero la causa que afecta el aprendizaje o la participación, sin perder trazabilidad institucional.',
    'mejora': 'Definir una acción específica, responsable, medible y revisable, conectada con el patrón de error detectado.',
}

CORRECT_BY_MODULE = {
    'diagnostico-inicial': {
        'inferencia': 'El desempeño inicial debe leerse por patrones de error y no solo por puntaje global, porque cada competencia exige una estrategia distinta.',
        'decision': 'Priorizar un plan de estudio basado en evidencias del diagnóstico, diferenciando errores de lectura, dominio conceptual y manejo del tiempo.',
        'riesgo': 'Confundir un resultado bajo con falta general de conocimiento, sin identificar si el error proviene de la consigna, del contenido o de la estrategia.',
        'evidencia': 'Cruzar puntaje, tipo de pregunta, justificación del error y tiempo usado para definir una ruta de mejora razonable.',
        'prioridad': 'Intervenir primero la brecha que se repite en varios ítems y afecta el desempeño transversal de la prueba.',
        'mejora': 'Convertir el diagnóstico en metas semanales verificables, con revisión de errores y nuevos intentos comparables.',
    },
    'lectura-critica-aplicada': {
        'inferencia': 'La conclusión válida debe apoyarse en la relación entre tesis, evidencias y límites del texto, no en una coincidencia literal de palabras.',
        'decision': 'Identificar la tesis, evaluar la suficiencia de las evidencias y reconocer los supuestos antes de aceptar la conclusión del autor.',
        'riesgo': 'Tomar como válida una generalización persuasiva aunque el texto no aporte evidencia suficiente o comparable.',
        'evidencia': 'Contrastar ejemplos, datos y alcance de la afirmación para determinar si sostienen la conclusión planteada.',
        'prioridad': 'Reconocer qué afirma el texto, qué prueba realmente y qué queda como supuesto no demostrado.',
        'mejora': 'Releer el texto buscando relaciones lógicas entre ideas, no palabras aisladas que parezcan coincidir con una opción.',
    },
    'competencias-pedagogicas': {
        'inferencia': 'La dificultad pedagógica se ubica en la coherencia entre propósito, actividad, evidencia y criterio de evaluación.',
        'decision': 'Rediseñar la secuencia para alinear desempeños esperados, actividades, evidencias y retroalimentación formativa.',
        'riesgo': 'Valorar la actividad por su atractivo o cumplimiento formal sin comprobar si produce evidencia válida de aprendizaje.',
        'evidencia': 'Usar productos, explicaciones, desempeño observado y criterios explícitos para decidir si el aprendizaje esperado se alcanzó.',
        'prioridad': 'Ajustar primero la alineación curricular y evaluativa antes de aumentar tareas o repetir ejercicios.',
        'mejora': 'Incorporar retroalimentación, oportunidades de revisión y criterios conocidos por los estudiantes desde el inicio.',
    },
    'competencias-comportamentales-tjs': {
        'inferencia': 'La situación exige una respuesta profesional que combine escucha, límites, registro y seguimiento institucional.',
        'decision': 'Escuchar a los actores, verificar información, comunicar límites y acordar acciones restaurativas o pedagógicas con seguimiento.',
        'riesgo': 'Responder solo para calmar la presión inmediata, sin documentar hechos ni proteger la confianza de la comunidad.',
        'evidencia': 'Usar registros, testimonios contrastados y acuerdos institucionales para decidir una actuación proporcional.',
        'prioridad': 'Proteger la dignidad de las personas y restablecer condiciones de convivencia y aprendizaje.',
        'mejora': 'Formalizar acuerdos, responsables y revisión posterior para que la intervención no quede en una reacción aislada.',
    },
    'normativa-contexto-docente': {
        'inferencia': 'La norma debe aplicarse según su finalidad educativa y las evidencias del caso, no como trámite literal aislado.',
        'decision': 'Documentar una decisión proporcional que garantice derechos, responsabilidades institucionales y seguimiento verificable.',
        'riesgo': 'Invocar la norma sin analizar contexto, debido proceso, inclusión o efectos sobre el derecho a aprender.',
        'evidencia': 'Relacionar registros institucionales, marco normativo y necesidades del estudiante o de la comunidad antes de decidir.',
        'prioridad': 'Garantizar el derecho a la educación con medidas proporcionales, comunicadas y trazables.',
        'mejora': 'Convertir la decisión normativa en acciones, responsables y evidencias de cumplimiento institucional.',
    },
    'simulacros-por-area': {
        'inferencia': 'El dato disciplinar debe interpretarse considerando proporciones, contexto, demanda cognitiva y evidencia disponible.',
        'decision': 'Analizar la información cuantitativa o disciplinar antes de elegir una intervención académica o tecnológica.',
        'riesgo': 'Comparar cifras aisladas o porcentajes llamativos sin revisar base de cálculo, condiciones y propósito de la medición.',
        'evidencia': 'Relacionar tablas, gráficas, procedimientos y explicaciones de los estudiantes para sustentar la conclusión.',
        'prioridad': 'Identificar si la dificultad está en el concepto, en la interpretación de datos o en la lectura de la consigna.',
        'mejora': 'Diseñar práctica contextualizada que exija explicar procedimientos y transferirlos a situaciones nuevas.',
    },
    'simulacro-final-concurso': {
        'inferencia': 'El caso requiere integrar lectura crítica, pedagogía, normativa y juicio situacional antes de elegir la actuación.',
        'decision': 'Priorizar una respuesta integral, viable y sustentada que atienda aprendizaje, convivencia y responsabilidad institucional.',
        'riesgo': 'Resolver el caso desde una sola competencia cuando la situación exige articular varias evidencias y criterios.',
        'evidencia': 'Usar datos, testimonios, normas y efectos pedagógicos para justificar una decisión coherente.',
        'prioridad': 'Ordenar la actuación según impacto en aprendizaje, protección de derechos y posibilidad de seguimiento.',
        'mejora': 'Ajustar la estrategia de prueba para dedicar más lectura a ítems integradores y evitar respuestas por memoria.',
    },
    'reporte-progreso-plan-mejora': {
        'inferencia': 'El progreso real depende de patrones de error, no de variaciones aisladas del puntaje total.',
        'decision': 'Convertir los resultados en un plan específico por competencia, con metas, práctica deliberada y revisión de errores.',
        'riesgo': 'Cambiar toda la ruta de estudio por un resultado puntual sin analizar dificultad, tiempo y tipo de error.',
        'evidencia': 'Comparar aciertos, errores, justificaciones y tiempo usado para decidir qué reforzar primero.',
        'prioridad': 'Intervenir la brecha que limita más competencias o se repite en distintos simulacros.',
        'mejora': 'Definir una acción de estudio medible y revisarla con un nuevo simulacro comparable.',
    },
}

DISTRACTORS = [
    'Aplicar la medida más visible para mostrar gestión inmediata, aunque no resuelva la causa del problema.',
    'Elegir la alternativa que repite palabras del caso, sin verificar si explica la relación entre las evidencias.',
    'Esperar a tener información perfecta antes de actuar, aun cuando ya existen indicios suficientes para intervenir.',
    'Trasladar la responsabilidad a otra instancia sin formular una acción pedagógica propia.',
    'Promediar los datos disponibles y tomar el resultado global como explicación definitiva del desempeño.',
    'Priorizar el cumplimiento formal del procedimiento aunque no se conecte con aprendizaje, inclusión o convivencia.',
    'Suponer que aumentar actividades o tiempo de estudio corrige automáticamente el patrón de error.',
    'Generalizar una conclusión a partir de un caso aislado sin revisar condiciones, población ni propósito.',
]


def build_item(module, i):
    cases = CASES_BY_MODULE[module['slug']]
    case = cases[(i - 1) % len(cases)]
    task_key, stem = TASKS[(i - 1) % len(TASKS)]
    contexto = (
        f'{case[0]}\n'
        f'{case[1]}\n'
        f'{case[2]}\n'
        'Para responder no basta recordar una definición: es necesario interpretar la situación, reconocer tensiones y valorar consecuencias.\n'
        'La alternativa correcta debe ser viable en una institución educativa oficial y coherente con el derecho al aprendizaje.\n'
        'También debe evitar decisiones automáticas que confundan rapidez con pertinencia o formalidad con calidad pedagógica.'
    )
    correct = CORRECT_BY_MODULE.get(module['slug'], GOOD_OPTIONS).get(task_key, GOOD_OPTIONS[task_key])
    wrongs = [DISTRACTORS[(i + offset) % len(DISTRACTORS)] for offset in range(3)]
    options = [correct] + wrongs
    shift = (i - 1) % 4
    rotated = options[shift:] + options[:shift]
    answer = 'ABCD'[rotated.index(correct)]
    return {
        'contexto': contexto,
        'enunciado': stem,
        'opciones': rotated,
        'respuesta': answer,
        'justificacion': (
            f'La opción {answer} es la más sólida porque interpreta el caso desde la competencia '
            f'{module["competencia"]}, relaciona evidencias y propone una actuación proporcional. '
            'Las demás alternativas son distractores frecuentes en pruebas CNSC/ICFES: responden por apariencia, '
            'generalizan datos, aplazan sin criterio o privilegian el trámite sobre el aprendizaje.'
        ),
    }


class Command(BaseCommand):
    help = 'Aplica auditoría comercial y académica: precios, ruta de 8 módulos y banco premium V3.'

    @transaction.atomic
    def handle(self, *args, **options):
        category, _ = Category.objects.update_or_create(
            slug='ruta-premium-cnsc-2026',
            defaults={
                'name': 'Ruta Premium Concurso Docente CNSC 2026',
                'category_type': 'simulacros',
                'description': 'Ruta integral de preparación con diagnóstico, competencias, simulacros y plan de mejora.',
                'icon': 'bi-stars',
                'order': 1,
                'active': True,
            }
        )
        banco_cat, _ = Categoria.objects.get_or_create(nombre='Banco Premium CNSC 2026 V3')

        BancoPregunta.objects.exclude(categoria=banco_cat).update(activa=False)
        BancoPregunta.objects.filter(categoria__nombre='Banco Premium CNSC 2026 V2').update(activa=False)

        # Desactiva solo bancos genericos anteriores de plantilla repetitiva.
        BancoPregunta.objects.filter(
            enunciado__startswith='A partir del texto, cual alternativa representa la decision mas pertinente'
        ).update(activa=False)

        Modulo.objects.exclude(tipo__in=[module['tipo'] for module in MODULES]).update(activo=False)
        valid_module_slugs = [module['slug'] for module in MODULES] + ['elite-cnsc-2026']
        Simulacro.objects.exclude(module__slug__in=valid_module_slugs).update(activo=False)
        Product.objects.exclude(module__slug__in=valid_module_slugs).update(active=False)

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
                item = build_item(data, i)
                a, b, c, d = item['opciones']
                fingerprint = hashlib.sha1(f"{data['slug']}|v3|{i}|{item['contexto']}|{item['enunciado']}".encode('utf-8')).hexdigest()[:10]
                pregunta, was_created = BancoPregunta.objects.update_or_create(
                    titulo=f'{data["title"]} V3 {i:02d} {fingerprint}',
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
                        'fuente_normativa': 'CNSC/ICFES: razonamiento crítico, competencias docentes, Ley 115, Decreto 1278, Decreto 1421 y convivencia escolar según pertinencia del caso.',
                        'dificultad': 'elite',
                        'area': data['area'],
                        'competencia': data['competencia'],
                        'tiempo_limite_segundos': 180,
                        'es_premium': True,
                        'activa': True,
                    }
                )
                created_questions += int(was_created)
                questions.append(pregunta)

            simulacro, _ = Simulacro.objects.update_or_create(
                nombre=f'{data["title"]} - Simulacro premium',
                defaults={
                    'descripcion': data['description'],
                    'tipo': data['tipo_sim'],
                    'module': module,
                    'area': data['area'],
                    'tiempo_limite_minutos': 60,
                    'tiempo_por_pregunta_segundos': 180,
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
                'short_description': 'Oferta de lanzamiento: todos los módulos, simulacros premium y reportes por un solo pago.',
                'description': 'Incluye diagnóstico, lectura crítica, competencias pedagógicas, TJS, normativa, áreas, simulacro final y plan de mejora.',
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

        valid_simulacro_names = [f'{module["title"]} - Simulacro premium' for module in MODULES]
        Simulacro.objects.exclude(nombre__in=valid_simulacro_names).update(activo=False)

        # Precios definitivos: paquete completo 35k/25k; módulos individuales vigentes 15k.
        Product.objects.filter(module__slug__in=[module['slug'] for module in MODULES]).update(
            price=Decimal('15000'),
            sale_price=Decimal('15000'),
            active=True,
        )
        Product.objects.exclude(module__slug__in=valid_module_slugs).update(active=False)

        self.stdout.write(self.style.SUCCESS(
            f'Upgrade aplicado: {len(MODULES)} módulos, {created_questions} preguntas nuevas, precios actualizados.'
        ))
