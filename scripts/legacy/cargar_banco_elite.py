from banco.models import Categoria, BancoPregunta
from simulacros.models import Simulacro

# LIMPIEZA CONTROLADA
BancoPregunta.objects.all().delete()
Simulacro.objects.all().delete()

# CATEGORÍAS
pedagogia, _ = Categoria.objects.get_or_create(nombre="Pedagogía")
normatividad, _ = Categoria.objects.get_or_create(nombre="Normatividad")

preguntas = [
    {
        "categoria": pedagogia,
        "titulo": "Modelos pedagógicos y decisión institucional",
        "contexto": """En una institución educativa oficial, el consejo académico discute la actualización del enfoque pedagógico institucional debido a resultados inconsistentes en desempeño, baja participación estudiantil y dificultades para transferir aprendizajes a contextos reales. Algunos docentes defienden prácticas centradas en transmisión magistral por eficiencia operativa, mientras otros argumentan la necesidad de enfoques activos que fortalezcan pensamiento crítico, resolución de problemas y aprendizaje contextualizado. La rectoría solicita una decisión técnicamente sustentada que no responda solo a preferencias metodológicas individuales, sino a coherencia pedagógica institucional.""",
        "enunciado": "¿Cuál decisión resulta pedagógicamente más consistente con un enfoque formativo centrado en desarrollo de competencias?",
        "opcion_a": "Mantener exclusivamente transmisión magistral por control del tiempo.",
        "opcion_b": "Adoptar estrategias activas coherentes con construcción significativa del aprendizaje.",
        "opcion_c": "Delegar a cada docente sin lineamiento institucional.",
        "opcion_d": "Eliminar actividades colaborativas por dispersión.",
        "respuesta_correcta": "B",
        "justificacion": "Los enfoques por competencias exigen construcción activa y transferencia contextual.",
        "fuente_normativa": "Ley 115 de 1994",
    },
    {
        "categoria": normatividad,
        "titulo": "Debido proceso evaluativo",
        "contexto": """Un acudiente presenta reclamación formal porque su hijo fue reportado como reprobado sin evidencias documentadas de planes de apoyo, retroalimentación estructurada ni procedimientos de recuperación definidos en el SIEE. El docente sostiene autonomía profesional para valorar desempeño, mientras coordinación académica revisa si la institución respetó integralmente el marco normativo aplicable.""",
        "enunciado": "¿Cuál actuación institucional es jurídicamente más sólida?",
        "opcion_a": "Ratificar la decisión solo por autonomía docente.",
        "opcion_b": "Verificar cumplimiento integral del SIEE y debido proceso evaluativo.",
        "opcion_c": "Promover automáticamente al estudiante.",
        "opcion_d": "Trasladar decisión exclusiva a rectoría.",
        "respuesta_correcta": "B",
        "justificacion": "El proceso evaluativo debe ajustarse al SIEE y garantizar debido proceso.",
        "fuente_normativa": "Decreto 1290 de 2009",
    },
]

objetos = []

for p in preguntas:
    pregunta = BancoPregunta.objects.create(
        categoria=p["categoria"],
        titulo=p["titulo"],
        contexto=p["contexto"],
        enunciado=p["enunciado"],
        opcion_a=p["opcion_a"],
        opcion_b=p["opcion_b"],
        opcion_c=p["opcion_c"],
        opcion_d=p["opcion_d"],
        respuesta_correcta=p["respuesta_correcta"],
        justificacion=p["justificacion"],
        fuente_normativa=p["fuente_normativa"],
        dificultad="elite",
        activa=True,
    )
    objetos.append(pregunta)

simulacro = Simulacro.objects.create(
    nombre="Simulacro CNSC Premium Elite",
    descripcion="Piloto premium de alta exigencia.",
    tipo="simulacro",
    tiempo_limite_minutos=90,
    puntaje_minimo_aprobacion=70,
    activo=True,
)

simulacro.preguntas.add(*objetos)

print("BANCO ELITE CARGADO")
print("Preguntas:", BancoPregunta.objects.count())
print("Simulacros:", Simulacro.objects.count())