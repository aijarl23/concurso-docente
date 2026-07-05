from django.shortcuts import get_object_or_404, render

from .models import Modulo, Tema


MODULE_DESCRIPTION = (
    'Entrenamiento por competencias para Concurso Docente CNSC, con enfoque '
    'en lectura critica, juicio situacional y resolucion de casos aplicados.'
)


def seed_modulos():
    modulos_data = [
        {
            'titulo': 'Modulo 1 - Lectura Critica y Test de Juicio Situacional (TJS)',
            'tipo': 'lectura_tjs',
            'descripcion': MODULE_DESCRIPTION,
            'temas': [
                ('Lectura literal', 'Reconocimiento de informacion explicita y relaciones internas del texto.'),
                ('Lectura inferencial', 'Deduccion de implicaciones, supuestos y conclusiones no expresas.'),
                ('Lectura critica', 'Analisis de argumentos, intencion comunicativa y validez de posturas.'),
                ('Test de juicio situacional', 'Toma de decisiones frente a dilemas del contexto escolar.'),
                ('Casos institucionales', 'Interpretacion de situaciones reales de aula y convivencia escolar.'),
            ],
        },
        {
            'titulo': 'Modulo 2 - Perfil Docente',
            'tipo': 'perfil_docente',
            'descripcion': MODULE_DESCRIPTION,
            'temas': [
                ('Rol docente', 'Responsabilidades profesionales, liderazgo pedagogico y servicio publico.'),
                ('Etica profesional', 'Criterios de actuacion frente a conflictos, equidad y cuidado institucional.'),
                ('Competencias funcionales', 'Gestion del aula, seguimiento de procesos y trabajo colaborativo.'),
                ('Gestion escolar', 'Articulacion con el PEI, convivencia, inclusion y mejoramiento continuo.'),
                ('Contexto educativo', 'Lectura de necesidades territoriales, familiares e institucionales.'),
            ],
        },
        {
            'titulo': 'Modulo 3 - Componente Pedagogico',
            'tipo': 'pedagogico',
            'descripcion': MODULE_DESCRIPTION,
            'temas': [
                ('Didactica', 'Seleccion de estrategias pertinentes segun objetivos, estudiantes y contexto.'),
                ('Planeacion curricular', 'Coherencia entre estandares, evidencias, actividades y evaluacion.'),
                ('Evaluacion', 'Uso pedagogico de evidencias, retroalimentacion y criterios de desempeno.'),
                ('Inclusion', 'Ajustes razonables, barreras para el aprendizaje y participacion efectiva.'),
                ('Modelos pedagogicos', 'Relacion entre enfoques, practicas de aula y formacion integral.'),
            ],
        },
        {
            'titulo': 'Modulo 4 - Psicotecnico y Autoevaluacion',
            'tipo': 'psicotecnico',
            'descripcion': MODULE_DESCRIPTION,
            'temas': [
                ('Razonamiento verbal', 'Analisis de relaciones semanticas, argumentos y comprension compleja.'),
                ('Series logicas', 'Identificacion de patrones, secuencias y reglas de transformacion.'),
                ('Analogias', 'Comparacion de relaciones conceptuales y transferencia de criterios.'),
                ('Atencion y concentracion', 'Control de detalle, discriminacion de informacion y precision.'),
                ('Autoevaluacion', 'Reconocimiento de fortalezas, brechas y decisiones de mejora.'),
            ],
        },
    ]

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
