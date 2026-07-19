from banco.models import Categoria, BancoPregunta
from simulacros.models import Simulacro


def crear_categoria(nombre):
    categoria, _ = Categoria.objects.get_or_create(nombre=nombre)
    return categoria


def crear_pregunta(
    categoria,
    titulo,
    contexto,
    enunciado,
    opcion_a,
    opcion_b,
    opcion_c,
    opcion_d,
    respuesta_correcta,
    justificacion,
    fuente
):
    return BancoPregunta.objects.create(
        categoria=categoria,
        titulo=titulo,
        contexto=contexto,
        enunciado=enunciado,
        opcion_a=opcion_a,
        opcion_b=opcion_b,
        opcion_c=opcion_c,
        opcion_d=opcion_d,
        respuesta_correcta=respuesta_correcta,
        justificacion=justificacion,
        fuente_normativa=fuente,
        dificultad='elite',
        activa=True
    )


def crear_simulacro(nombre, descripcion, preguntas):
    simulacro, _ = Simulacro.objects.get_or_create(
        nombre=nombre,
        defaults={
            "descripcion": descripcion,
            "tipo": "simulacro",
            "tiempo_limite_minutos": 120,
            "puntaje_minimo_aprobacion": 70,
            "activo": True
        }
    )
    simulacro.preguntas.add(*preguntas)
    return simulacro


def generar_base():
    pedagogia = crear_categoria("Pedagogía")
    normatividad = crear_categoria("Normatividad")

    preguntas = []

    preguntas.append(
        crear_pregunta(
            pedagogia,
            "Constructivismo aplicado",
            """En una institución educativa oficial, los resultados de aprendizaje muestran baja transferencia del conocimiento a situaciones reales. El equipo docente identifica que gran parte de las prácticas de aula siguen centradas en repetición mecánica y exposición unidireccional. La rectoría solicita una propuesta pedagógica coherente con el desarrollo de competencias, aprendizaje significativo y participación activa del estudiante.""",
            "¿Cuál decisión pedagógica resulta más consistente con un enfoque constructivista?",
            "Mantener evaluación memorística por facilidad operativa.",
            "Diseñar experiencias activas de construcción del conocimiento contextualizado.",
            "Reducir interacción entre estudiantes para mejorar disciplina.",
            "Sustituir análisis por repetición de contenidos.",
            "B",
            "El constructivismo privilegia construcción activa, contextualización y aprendizaje significativo.",
            "Ley 115 de 1994"
        )
    )

    preguntas.append(
        crear_pregunta(
            normatividad,
            "Debido proceso académico",
            """Un acudiente presenta reclamación formal porque su hijo fue reportado con pérdida académica sin evidencias claras de acompañamiento, recuperación o procedimientos institucionales documentados conforme al sistema de evaluación institucional.""",
            "¿Cuál actuación institucional tiene mayor sustento jurídico?",
            "Ratificar decisión únicamente con criterio docente.",
            "Revisar cumplimiento integral del SIEE y debido proceso evaluativo.",
            "Promover automáticamente para evitar conflicto.",
            "Delegar decisión exclusivamente a coordinación.",
            "B",
            "El proceso evaluativo debe garantizar debido proceso y coherencia institucional.",
            "Decreto 1290 de 2009"
        )
    )

    simulacro = crear_simulacro(
        "Simulacro CNSC Premium Elite",
        "Simulacro profesional de alta exigencia.",
        preguntas
    )

    print("GENERACIÓN OK")
    print("Preguntas creadas:", len(preguntas))
    print("Simulacro:", simulacro.nombre)


generar_base()