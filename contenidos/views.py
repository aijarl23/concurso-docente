from django.shortcuts import get_object_or_404, render

from .models import Modulo, Tema


MODULE_DESCRIPTION = (
    'Entrenamiento por competencias para Concurso Docente CNSC, con enfoque '
    'en lectura crítica, juicio situacional y resolución de casos aplicados.'
)


def seed_modulos():
    modulos_data = [
        {
            'titulo': 'Diagnóstico inicial',
            'tipo': 'diagnostico_inicial',
            'descripcion': 'Mapa de entrada para identificar brechas reales antes de iniciar la preparación.',
            'temas': [
                ('Mapa de fortalezas y brechas', 'Lectura inicial del nivel por competencia.'),
                ('Lectura de consignas', 'Identificación precisa de lo que pregunta cada ítem.'),
                ('Toma de decisiones inicial', 'Priorización de acciones según evidencia.'),
                ('Plan de entrada', 'Ruta de estudio sugerida a partir del desempeño.'),
            ],
        },
        {
            'titulo': 'Lectura crítica aplicada',
            'tipo': 'lectura_critica_aplicada',
            'descripcion': 'Inferencia, tesis, intención comunicativa y evaluación de argumentos en textos complejos.',
            'temas': [
                ('Inferencia y supuestos', 'Reconocimiento de información implícita sustentada.'),
                ('Tesis y argumentos', 'Análisis de estructura argumentativa y evidencias.'),
                ('Intención del autor', 'Interpretación del propósito comunicativo.'),
                ('Evaluación de evidencia', 'Valoración de suficiencia, pertinencia y coherencia.'),
            ],
        },
        {
            'titulo': 'Competencias pedagógicas',
            'tipo': 'competencias_pedagogicas',
            'descripcion': 'Casos de planeación, evaluación formativa, inclusión, didáctica y gestión del aula.',
            'temas': [
                ('Planeación curricular', 'Coherencia entre objetivos, desempeños, actividades y evaluación.'),
                ('Evaluación formativa', 'Uso de evidencias y retroalimentación para mejorar aprendizajes.'),
                ('Inclusión y DUA', 'Barreras, ajustes razonables y participación efectiva.'),
                ('Didáctica situada', 'Estrategias pertinentes según contexto y necesidad.'),
            ],
        },
        {
            'titulo': 'Competencias comportamentales / TJS',
            'tipo': 'competencias_tjs',
            'descripcion': 'Juicio situacional docente para convivencia, liderazgo, comunicación y trabajo colaborativo.',
            'temas': [
                ('Comunicación asertiva', 'Respuesta profesional ante tensión y desacuerdo.'),
                ('Liderazgo', 'Actuación orientada a acuerdos, cuidado y mejora institucional.'),
                ('Trabajo en equipo', 'Coordinación con pares, familias y directivos.'),
                ('Orientación al logro', 'Decisiones con seguimiento y evidencia.'),
            ],
        },
        {
            'titulo': 'Normativa y contexto docente',
            'tipo': 'normativa_contexto',
            'descripcion': 'Aplicación contextual de normativa educativa, inclusión, convivencia y funciones docentes.',
            'temas': [
                ('Estatuto docente', 'Uso aplicado del marco de profesionalización docente.'),
                ('Ley General de Educación', 'Fines, responsabilidades y sentido pedagógico.'),
                ('Convivencia escolar', 'Prevención, corresponsabilidad y rutas de actuación.'),
                ('Inclusión y ajustes razonables', 'Garantía del derecho a aprender con trazabilidad.'),
            ],
        },
        {
            'titulo': 'Simulacros por área',
            'tipo': 'simulacros_area',
            'descripcion': 'Entrenamiento por disciplina con razonamiento cuantitativo, datos y situaciones contextualizadas.',
            'temas': [
                ('Razonamiento cuantitativo', 'Interpretación de datos, proporciones y tendencias.'),
                ('Matemáticas aplicadas', 'Resolución de problemas en contexto escolar.'),
                ('Interpretación de datos', 'Lectura de tablas, gráficas e indicadores.'),
                ('Problemas contextualizados', 'Transferencia de procedimientos a situaciones nuevas.'),
            ],
        },
        {
            'titulo': 'Simulacro final tipo concurso',
            'tipo': 'simulacro_final',
            'descripcion': 'Prueba integral con mezcla de lectura crítica, pedagogía, normativa, TJS y razonamiento aplicado.',
            'temas': [
                ('Gestión del tiempo', 'Estrategia para responder bajo límite real.'),
                ('Integración de competencias', 'Cruce de lectura, criterio pedagógico y juicio situacional.'),
                ('Análisis de resultados', 'Lectura técnica de aciertos, errores y tendencias.'),
                ('Estrategia de cierre', 'Plan final de preparación antes de la prueba.'),
            ],
        },
        {
            'titulo': 'Reporte de progreso y plan de mejora',
            'tipo': 'reporte_mejora',
            'descripcion': 'Conversión de resultados en una ruta concreta de refuerzo, seguimiento y mejora.',
            'temas': [
                ('Lectura de resultados', 'Interpretación de desempeño por competencia.'),
                ('Priorización de brechas', 'Selección de focos según impacto y urgencia.'),
                ('Plan semanal', 'Organización de sesiones de estudio por evidencia.'),
                ('Seguimiento de mejora', 'Revisión de avances y ajuste de estrategia.'),
            ],
        },
    ]

    tipos_vigentes = [module_data['tipo'] for module_data in modulos_data]
    Modulo.objects.exclude(tipo__in=tipos_vigentes).update(activo=False)

    for order, module_data in enumerate(modulos_data, 1):
        temas = module_data.pop('temas')
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
                defaults={
                    'titulo': titulo,
                    'descripcion': descripcion,
                    'activo': True,
                },
            )


def dashboard(request):
    seed_modulos()
    modulos = Modulo.objects.filter(activo=True).prefetch_related('temas')

    return render(request, 'contenidos/dashboard.html', {'modulos': modulos})


def detalle_modulo(request, modulo_id):
    seed_modulos()
    modulo = get_object_or_404(Modulo.objects.prefetch_related('temas'), id=modulo_id, activo=True)

    return render(request, 'contenidos/detalle_modulo.html', {'modulo': modulo})
