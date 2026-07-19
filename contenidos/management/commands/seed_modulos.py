from django.core.management.base import BaseCommand

from contenidos.models import Modulo, Tema

MODULOS_DATA = [
    {
        'titulo': 'Diagnóstico Inicial',
        'tipo': 'diagnostico_inicial',
        'descripcion': 'Línea base para identificar brechas reales antes de iniciar la preparación.',
        'temas': [
            ('Mapa de fortalezas y brechas', 'Lectura inicial del nivel por competencia.'),
            ('Lectura de consignas', 'Identificacion precisa de lo que pregunta cada item.'),
            ('Toma de decisiones inicial', 'Priorizacion de acciones segun evidencia.'),
            ('Plan de entrada', 'Ruta de estudio sugerida a partir del desempeno.'),
        ],
    },
    {
        'titulo': 'Lectura Crítica',
        'tipo': 'lectura_critica_aplicada',
        'descripcion': 'Inferencia, tesis, intención comunicativa y evaluación de argumentos en textos complejos.',
        'temas': [
            ('Inferencia y supuestos', 'Reconocimiento de informacion implicita sustentada.'),
            ('Tesis y argumentos', 'Analisis de estructura argumentativa y evidencias.'),
            ('Intencion del autor', 'Interpretacion del proposito comunicativo.'),
            ('Evaluacion de evidencia', 'Valoracion de suficiencia, pertinencia y coherencia.'),
        ],
    },
    {
        'titulo': 'Normatividad Educativa',
        'tipo': 'normativa_contexto',
        'descripcion': 'Aplicación contextual de la Ley 115, el Decreto 1278, el Decreto 1290 y la Ley 1620 a casos reales.',
        'temas': [
            ('Estatuto docente', 'Uso aplicado del marco de profesionalizacion docente.'),
            ('Ley General de Educacion', 'Fines, responsabilidades y sentido pedagogico.'),
            ('Convivencia escolar', 'Prevencion, corresponsabilidad y rutas de actuacion.'),
            ('Decreto 1290 y SIEE', 'Evaluacion institucional y debido proceso.'),
        ],
    },
    {
        'titulo': 'Inclusión Educativa',
        'tipo': 'inclusion_educativa',
        'descripcion': 'Barreras de aprendizaje, ajustes razonables, PIAR y Diseño Universal para el Aprendizaje.',
        'temas': [
            ('DUA aplicado', 'Multiples formas de representacion, accion y motivacion.'),
            ('PIAR y ajustes razonables', 'Planeacion individual con apoyos verificables.'),
            ('Barreras de participacion', 'Identificacion y remocion de barreras reales.'),
            ('Decreto 1421', 'Marco de educacion inclusiva aplicado a casos.'),
        ],
    },
    {
        'titulo': 'Competencias Pedagógicas',
        'tipo': 'competencias_pedagogicas',
        'descripcion': 'Casos de planeación curricular, evaluación formativa y didáctica situada en el aula.',
        'temas': [
            ('Planeacion curricular', 'Coherencia entre objetivos, desempenos, actividades y evaluacion.'),
            ('Evaluacion formativa', 'Uso de evidencias y retroalimentacion para mejorar aprendizajes.'),
            ('Didactica situada', 'Estrategias pertinentes segun contexto y necesidad.'),
            ('Gestion del aula', 'Clima, participacion y manejo de conflictos en clase.'),
        ],
    },
    {
        'titulo': 'Análisis de Casos',
        'tipo': 'competencias_tjs',
        'descripcion': 'Dilemas auténticos del ejercicio docente: convivencia, liderazgo, comunicación y trabajo colaborativo.',
        'temas': [
            ('Comunicacion asertiva', 'Respuesta profesional ante tension y desacuerdo.'),
            ('Liderazgo', 'Actuacion orientada a acuerdos, cuidado y mejora institucional.'),
            ('Trabajo en equipo', 'Coordinacion con pares, familias y directivos.'),
            ('Orientacion al logro', 'Decisiones con seguimiento y evidencia.'),
        ],
    },
    {
        'titulo': 'Gestión Escolar',
        'tipo': 'gestion_escolar',
        'descripcion': 'Gobierno escolar, Proyecto Educativo Institucional y gestiones institucionales del MEN.',
        'temas': [
            ('Gobierno escolar', 'Consejo academico, consejo directivo y personero.'),
            ('PEI y SIEE institucional', 'Coherencia entre horizonte institucional y evaluacion.'),
            ('Gestion academica y directiva', 'Decisiones de aula articuladas con la institucion.'),
            ('Gestion comunitaria', 'Relacion con familias y contexto local.'),
        ],
    },
    {
        'titulo': 'Competencias Disciplinares',
        'tipo': 'simulacros_area',
        'descripcion': 'Entrenamiento por disciplina con lectura crítica, datos y situaciones contextualizadas.',
        'temas': [
            ('Comprension disciplinar', 'Uso de conceptos del area para interpretar situaciones.'),
            ('Problemas contextualizados', 'Resolucion de casos aplicados al aula.'),
            ('Interpretacion de datos', 'Lectura de tablas, graficas e indicadores.'),
            ('Decision pedagogica por area', 'Intervenciones coherentes con el saber disciplinar.'),
        ],
    },
    {
        'titulo': 'Simulacro Integral',
        'tipo': 'simulacro_final',
        'descripcion': 'Prueba integral con lectura crítica, pedagogía, normativa, análisis de casos y razonamiento disciplinar.',
        'temas': [
            ('Gestion del tiempo', 'Estrategia para responder bajo limite real.'),
            ('Integracion de competencias', 'Cruce de lectura, criterio pedagogico y analisis de casos.'),
            ('Analisis de resultados', 'Lectura tecnica de aciertos, errores y tendencias.'),
            ('Estrategia de cierre', 'Plan final de preparacion antes de la prueba.'),
        ],
    },
    {
        'titulo': 'Análisis del Desempeño',
        'tipo': 'analisis_desempeno',
        'descripcion': 'Lectura técnica de resultados por competencia e identificación de patrones de error.',
        'temas': [
            ('Lectura de resultados', 'Interpretacion de desempeno por competencia.'),
            ('Patrones de error', 'Identificacion de errores recurrentes y su causa.'),
            ('Priorizacion de brechas', 'Seleccion de focos segun impacto y urgencia.'),
            ('Comparacion con diagnostico inicial', 'Medicion real del avance logrado.'),
        ],
    },
    {
        'titulo': 'Plan de Fortalecimiento',
        'tipo': 'plan_fortalecimiento',
        'descripcion': 'Traduce el análisis de desempeño en un plan de estudio semanal con seguimiento verificable.',
        'temas': [
            ('Plan semanal', 'Organizacion de sesiones de estudio por evidencia.'),
            ('Practica deliberada', 'Ejercicios enfocados en la brecha identificada.'),
            ('Seguimiento de avance', 'Revision periodica de progreso real.'),
            ('Estrategia de cierre', 'Ajuste final antes de la prueba.'),
        ],
    },
]


class Command(BaseCommand):
    help = (
        'Crea o actualiza los modulos y temas base de contenidos. '
        'Debe correr como parte del deploy (build.sh), nunca dentro de una vista.'
    )

    def handle(self, *args, **options):
        tipos_vigentes = [module_data['tipo'] for module_data in MODULOS_DATA]
        Modulo.objects.exclude(tipo__in=tipos_vigentes).update(activo=False)
        for order, module_data in enumerate(MODULOS_DATA, 1):
            temas = module_data['temas']
            modulo, _ = Modulo.objects.update_or_create(
                tipo=module_data['tipo'],
                defaults={
                    'titulo': module_data['titulo'],
                    'descripcion': module_data['descripcion'],
                    'orden': order,
                    'activo': True,
                },
            )
            Tema.objects.filter(modulo=modulo).exclude(orden__in=range(1, len(temas) + 1)).update(activo=False)
            for topic_order, (titulo, descripcion) in enumerate(temas, 1):
                Tema.objects.update_or_create(
                    modulo=modulo,
                    orden=topic_order,
                    defaults={'titulo': titulo, 'descripcion': descripcion, 'activo': True},
                )

        self.stdout.write(self.style.SUCCESS(f'Modulos sincronizados: {len(MODULOS_DATA)}'))
