from evaluaciones.models import Pregunta, Simulacro

# LIMPIEZA TOTAL
Pregunta.objects.all().delete()
Simulacro.objects.all().delete()

# CREAR SIMULACRO PREMIUM
simulacro = Simulacro.objects.create(
    nombre="CNSC PREMIUM ELITE — Normatividad Educativa Colombiana",
    descripcion="Simulacro de alta exigencia tipo CNSC con enfoque normativo.",
    tiempo_limite_minutos=120,
    puntaje_minimo_aprobacion=70,
    activo=True
)

preguntas_data = [
    {
        "contexto": "En una institución educativa oficial, una estudiante con diagnóstico formal de trastorno del espectro autista presenta dificultades significativas en interacción social, procesamiento de instrucciones complejas y participación en evaluaciones escritas convencionales. Aunque la familia entregó documentación clínica desde el inicio del año, algunos docentes sostienen que modificar instrumentos evaluativos podría generar inequidad frente al resto del grupo.",
        "enunciado": "¿Cuál actuación institucional es jurídicamente más consistente?",
        "opcion_a": "Mantener instrumentos ordinarios para preservar igualdad formal.",
        "opcion_b": "Implementar ajustes razonables pedagógicos y evaluativos coherentes con sus necesidades.",
        "opcion_c": "Exigir nueva certificación oficial antes de cualquier adaptación.",
        "opcion_d": "Trasladar la responsabilidad exclusivamente al acudiente.",
        "respuesta_correcta": "B",
        "justificacion": "El Decreto 1421 de 2017 exige ajustes razonables y educación inclusiva.",
        "fuente_normativa": "Decreto 1421 de 2017"
    },
    {
        "contexto": "Durante revisión del SIEE, un acudiente reclama porque su hijo no recibió estrategias de apoyo documentadas antes de reprobar el año.",
        "enunciado": "¿Qué decisión es jurídicamente más sólida?",
        "opcion_a": "Confirmar reprobación inmediata.",
        "opcion_b": "Verificar debido proceso, estrategias de apoyo y procedimientos del SIEE.",
        "opcion_c": "Promover automáticamente.",
        "opcion_d": "Delegar decisión a coordinación.",
        "respuesta_correcta": "B",
        "justificacion": "El Decreto 1290 exige debido proceso evaluativo y acompañamiento.",
        "fuente_normativa": "Decreto 1290 de 2009"
    },
    {
        "contexto": "Una institución pretende cancelar matrícula por reiteradas faltas disciplinarias sin trazabilidad formal suficiente.",
        "enunciado": "¿Qué actuación es jurídicamente más defendible?",
        "opcion_a": "Cancelar matrícula inmediatamente.",
        "opcion_b": "Reiniciar proceso garantizando debido proceso y trazabilidad.",
        "opcion_c": "Expulsión automática.",
        "opcion_d": "Remitir exclusivamente a policía.",
        "respuesta_correcta": "B",
        "justificacion": "Ley 1620 exige debido proceso y procedimientos institucionales.",
        "fuente_normativa": "Ley 1620 de 2013"
    },
    {
        "contexto": "Una docente sostiene que la evaluación es exclusivamente su autonomía y no debe sujetarse al SIEE.",
        "enunciado": "¿Cuál interpretación es correcta?",
        "opcion_a": "Autonomía absoluta.",
        "opcion_b": "Autonomía dentro del marco institucional y legal.",
        "opcion_c": "Solo rectoría decide.",
        "opcion_d": "El SIEE no aplica.",
        "respuesta_correcta": "B",
        "justificacion": "La autonomía docente opera dentro del marco institucional.",
        "fuente_normativa": "Decreto 1290"
    },
    {
        "contexto": "Una institución niega matrícula por antecedentes disciplinarios de otro colegio.",
        "enunciado": "¿Qué postura tiene mayor sustento?",
        "opcion_a": "Negar ingreso preventivamente.",
        "opcion_b": "Excluir por autonomía institucional.",
        "opcion_c": "Garantizar acceso y evitar discriminación.",
        "opcion_d": "Solo consejo académico decide.",
        "respuesta_correcta": "C",
        "justificacion": "Derecho a la educación y no discriminación.",
        "fuente_normativa": "Ley 115"
    }
]

for p in preguntas_data:
    pregunta = Pregunta.objects.create(
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
    simulacro.preguntas.add(pregunta)

print("SIMULACRO CNSC PREMIUM CREADO CORRECTAMENTE")
print("TOTAL PREGUNTAS:", simulacro.preguntas.count())