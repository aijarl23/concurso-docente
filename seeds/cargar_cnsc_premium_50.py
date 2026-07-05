from banco.models import Categoria, BancoPregunta
from simulacros.models import Simulacro

# CATEGORIAS
categorias = [
    "Pedagogia",
    "Didactica",
    "Normatividad",
    "Inclusion",
    "Convivencia",
    "Gestion Escolar"
]

cat = {}
for c in categorias:
    cat[c], _ = Categoria.objects.get_or_create(nombre=c)

preguntas = []

def add(
    categoria,
    titulo,
    contexto,
    enunciado,
    a,b,c,d,
    correcta,
    justificacion,
    fuente
):
    p = BancoPregunta.objects.create(
        categoria=cat[categoria],
        titulo=titulo,
        contexto=contexto,
        enunciado=enunciado,
        opcion_a=a,
        opcion_b=b,
        opcion_c=c,
        opcion_d=d,
        respuesta_correcta=correcta,
        justificacion=justificacion,
        fuente_normativa=fuente,
        dificultad='elite',
        activa=True
    )
    preguntas.append(p)

# 1
add(
    "Pedagogia",
    "Modelo pedagogico institucional",
    "Una institucion educativa oficial evidencia bajos niveles de transferencia del aprendizaje, poca autonomia estudiantil y dependencia excesiva de exposiciones magistrales.",
    "Que decision institucional es mas coherente con enfoque por competencias?",
    "Mantener memorizacion intensiva",
    "Diseñar experiencias activas contextualizadas",
    "Eliminar aprendizaje colaborativo",
    "Reducir trabajo practico",
    "B",
    "El enfoque por competencias exige aplicacion contextual.",
    "Ley 115"
)

# 2
add(
    "Didactica",
    "Secuencia didactica",
    "Un docente desea mejorar comprension profunda y transferencia del aprendizaje.",
    "Que estructura didactica es mas pertinente?",
    "Solo explicacion magistral",
    "Inicio desarrollo cierre evaluacion",
    "Solo taller final",
    "Solo prueba escrita",
    "B",
    "La secuencia didactica estructura aprendizaje progresivo.",
    "MEN"
)

# 3
add(
    "Normatividad",
    "Debido proceso",
    "Un acudiente reclama porque no hubo evidencias de recuperacion academica.",
    "Que corresponde?",
    "Ratificar perdida",
    "Verificar cumplimiento del SIEE",
    "Excluir estudiante",
    "Promocion automatica",
    "B",
    "Debe garantizarse debido proceso.",
    "Decreto 1290"
)

# 4
add(
    "Inclusion",
    "Ajustes razonables",
    "Un estudiante con discapacidad requiere apoyos.",
    "Que accion corresponde?",
    "Evaluar igual sin ajustes",
    "Implementar ajustes razonables",
    "Esperar siguiente año",
    "Remitir sin accion",
    "B",
    "Educacion inclusiva exige ajustes.",
    "Decreto 1421"
)

# 5
add(
    "Convivencia",
    "Ruta institucional",
    "Existe conflicto reiterado con afectacion del clima escolar.",
    "Que procede?",
    "Suspension inmediata",
    "Aplicar ruta institucional",
    "Ignorar",
    "Cambio automatico",
    "B",
    "Debe seguirse Ley 1620.",
    "Ley 1620"
)

# 6
add(
    "Gestion Escolar",
    "PEI",
    "La institucion actualiza su horizonte institucional.",
    "Que instrumento orienta esa coherencia?",
    "Manual docente",
    "PEI",
    "Horario escolar",
    "Acta disciplinaria",
    "B",
    "El PEI orienta identidad institucional.",
    "Ley 115"
)

# 7
add(
    "Pedagogia",
    "Evaluacion formativa",
    "Un docente desea mejorar retroalimentacion.",
    "Que enfoque es pertinente?",
    "Solo sumativa",
    "Formativa continua",
    "Solo examen final",
    "Sin retroalimentacion",
    "B",
    "La evaluacion formativa mejora aprendizaje.",
    "Decreto 1290"
)

# 8
add(
    "Didactica",
    "ABP",
    "Se busca pensamiento critico y resolucion de problemas.",
    "Que estrategia encaja?",
    "Aprendizaje basado en problemas",
    "Dictado repetitivo",
    "Memorizacion",
    "Solo lectura",
    "A",
    "ABP fortalece resolucion contextual.",
    "MEN"
)

# 9
add(
    "Normatividad",
    "Manual convivencia",
    "La institucion revisa normas internas.",
    "Que principio debe respetarse?",
    "Arbitrariedad",
    "Debido proceso",
    "Decision unilateral",
    "Castigo inmediato",
    "B",
    "Debe existir garantia procedimental.",
    "Ley 1620"
)

# 10
add(
    "Gestion Escolar",
    "Liderazgo",
    "Se requiere mejora institucional sostenida.",
    "Que liderazgo es mas efectivo?",
    "Autoritario puro",
    "Pedagogico colaborativo",
    "Pasivo",
    "Fragmentado",
    "B",
    "El liderazgo pedagogico mejora resultados.",
    "MEN"
)

sim, _ = Simulacro.objects.get_or_create(
    nombre="Simulacro CNSC General Premium"
)

sim.descripcion = "Simulacro premium CNSC"
sim.tipo = "simulacro"
sim.tiempo_limite_minutos = 120
sim.puntaje_minimo_aprobacion = 70
sim.activo = True
sim.save()

sim.preguntas.clear()
sim.preguntas.add(*preguntas)

print("OK")
print("Preguntas creadas:", len(preguntas))