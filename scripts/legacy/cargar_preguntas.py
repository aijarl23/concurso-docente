from evaluaciones.models import Pregunta

preguntas = [
]

for p in preguntas:
    Pregunta.objects.create(
        componente='normativo',
        dificultad='alta',
        contexto=p["contexto"],
        enunciado=p["enunciado"],
        opcion_a=p["opcion_a"],
        opcion_b=p["opcion_b"],
        opcion_c=p["opcion_c"],
        opcion_d=p["opcion_d"],
        respuesta_correcta=p["respuesta_correcta"],
        justificacion=p["justificacion"],
        fuente_normativa=p["fuente_normativa"],
        activa=True
    )

print("Preguntas cargadas correctamente")