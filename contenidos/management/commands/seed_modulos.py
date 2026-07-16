from django.core.management.base import BaseCommand

from contenidos.models import Modulo, Tema

MODULOS_DATA = [
    {
        'titulo': 'Diagnostico inicial',
        'tipo': 'diagnostico_inicial',
        'descripcion': 'Mapa de entrada para identificar brechas reales antes de iniciar la preparacion.',
        'temas': [
            ('Mapa de fortalezas y brechas', 'Lectura inicial del nivel por competencia.'),
            ('Lectura de consignas', 'Identificacion precisa de lo que pregunta cada item.'),
            ('Toma de decisiones inicial', 'Priorizacion de acciones segun evidencia.'),
            ('Plan de entrada', 'Ruta de estudio sugerida a partir del desempeno.'),
        ],
    },
    {
        'titulo': 'Lectura critica aplicada',
        'tipo': 'lectura_critica_aplicada',
        'descripcion': 'Inferencia, tesis, intencion comunicativa y evaluacion de argumentos en textos complejos.',
        'temas': [
            ('Inferencia y supuestos', 'Reconocimiento de informacion implicita sustentada.'),
            ('Tesis y argumentos', 'Analisis de estructura argumentativa y evidencias.'),
            ('Intencion del autor', 'Interpretacion del proposito comunicativo.'),
            ('Evaluacion de evidencia', 'Valoracion de suficiencia, pertinencia y coherencia.'),
        ],
    },
    {
        'titulo': 'Competencias pedagogicas',
        'tipo': 'competencias_pedagogicas',
        'descripcion': 'Casos de planeacion, evaluacion formativa, inclusion, didactica y gestion del aula.',
        'temas': [
            ('Planeacion curricular', 'Coherencia entre objetivos, desempenos, actividades y evaluacion.'),
            ('Evaluacion formativa', 'Uso de evidencias y retroalimentacion para mejorar aprendizajes.'),
            ('Inclusion y DUA', 'Barreras, ajustes razonables y participacion efectiva.'),
            ('Didactica situada', 'Estrategias pertinentes segun contexto y necesidad.'),
        ],
    },
    {
        'titulo': 'Competencias comportamentales / TJS',
        'tipo': 'competencias_tjs',
        'descripcion': 'Juicio situacional docente para convivencia, liderazgo, comunicacion y trabajo colaborativo.',
        'temas': [
            ('Comunicacion asertiva', 'Respuesta profesional ante tension y desacuerdo.'),
            ('Liderazgo', 'Actuacion orientada a acuerdos, cuidado y mejora institucional.'),
            ('Trabajo en equipo', 'Coordinacion con pares, familias y directivos.'),
            ('Orientacion al logro', 'Decisiones con seguimiento y evidencia.'),
        ],
    },
    {
        'titulo': 'Normativa y contexto docente',
        'tipo': 'normativa_contexto',
        'descripcion': 'Aplicacion contextual de normativa educativa, inclusion, convivencia y funciones docentes.',
        'temas': [
            ('Estatuto docente', 'Uso aplicado del marco de profesionalizacion docente.'),
            ('Ley General de Educacion', 'Fines, responsabilidades y sentido pedagogico.'),
            ('Convivencia escolar', 'Prevencion, corresponsabilidad y rutas de actuacion.'),
            ('Inclusion y ajustes razonables', 'Garantia del derecho a aprender con trazabilidad.'),
        ],
    },
    {
        'titulo': 'Simulacros por area',
        'tipo': 'simulacros_area',
        'descripcion': 'Entrenamiento por disciplina con lectura critica, datos y situaciones contextualizadas.',
        'temas': [
            ('Comprension disciplinar', 'Uso de conceptos del area para interpretar situaciones.'),
            ('Problemas contextualizados', 'Resolucion de casos aplicados al aula.'),
            ('Interpretacion de datos', 'Lectura de tablas, graficas e indicadores.'),
            ('Decision pedagogica por area', 'Intervenciones coherentes con el saber disciplinar.'),
        ],
    },
    {
        'titulo': 'Simulacro final tipo concurso',
        'tipo': 'simulacro_final',
        'descripcion': 'Prueba integral con lectura critica, pedagogia, normativa, TJS y razonamiento aplicado.',
        'temas': [
            ('Gestion del tiempo', 'Estrategia para responder bajo limite real.'),
            ('Integracion de competencias', 'Cruce de lectura, criterio pedagogico y juicio situacional.'),
            ('Analisis de resultados', 'Lectura tecnica de aciertos, errores y tendencias.'),
            ('Estrategia de cierre', 'Plan final de preparacion antes de la prueba.'),
        ],
    },
    {
        'titulo': 'Reporte de progreso y plan de mejora',
        'tipo': 'reporte_mejora',
        'descripcion': 'Conversion de resultados en una ruta concreta de refuerzo, seguimiento y mejora.',
        'temas': [
            ('Lectura de resultados', 'Interpretacion de desempeno por competencia.'),
            ('Priorizacion de brechas', 'Seleccion de focos segun impacto y urgencia.'),
            ('Plan semanal', 'Organizacion de sesiones de estudio por evidencia.'),
            ('Seguimiento de mejora', 'Revision de avances y ajuste de estrategia.'),
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
