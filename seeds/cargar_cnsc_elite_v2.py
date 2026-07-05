from banco.models import Categoria, BancoPregunta
from simulacros.models import Simulacro

# LIMPIEZA CONTROLADA DEL SIMULACRO PREMIUM
BancoPregunta.objects.filter(titulo__startswith='ELITE').delete()

categorias = {}
for nombre in [
    'Pedagogía', 'Didáctica', 'Normatividad', 'Inclusión', 'Convivencia', 'Gestión Escolar'
]:
    categorias[nombre], _ = Categoria.objects.get_or_create(nombre=nombre)

preguntas = []

def crear(categoria, titulo, contexto, enunciado, a, b, c, d, correcta, justificacion, fuente):
    p = BancoPregunta.objects.create(
        categoria=categorias[categoria],
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
        activa=True,
    )
    preguntas.append(p)

crear('Pedagogía','ELITE 1','En una institución educativa oficial, los resultados de aprendizaje muestran que los estudiantes recuerdan contenidos pero fallan al transferir conocimientos a problemas reales. El consejo académico identifica prácticas centradas en transmisión unidireccional, baja participación estudiantil y poca metacognición. La rectoría exige una decisión institucional sustentada en coherencia pedagógica y no en preferencias individuales.','¿Qué decisión institucional resulta más consistente con un enfoque de desarrollo de competencias?','Mantener centralidad exclusiva de exposición magistral por eficiencia administrativa.','Diseñar experiencias activas contextualizadas con resolución de problemas y reflexión metacognitiva.','Incrementar número de pruebas memorísticas para mejorar disciplina académica.','Reducir trabajo colaborativo para evitar dispersión.','B','El enfoque por competencias requiere aplicación contextual, participación activa y construcción significativa.','Ley 115 de 1994')

crear('Normatividad','ELITE 2','Un acudiente presenta reclamación formal porque su hijo fue declarado no promovido sin evidencia clara de planes de apoyo, recuperación, retroalimentación documentada ni trazabilidad de decisiones conforme al sistema institucional de evaluación. El docente invoca autonomía profesional plena para sustentar la decisión.','¿Cuál actuación institucional tiene mayor solidez jurídica?','Ratificar automáticamente la decisión por autonomía docente.','Revisar cumplimiento integral del SIEE y garantías de debido proceso evaluativo.','Promover automáticamente al estudiante para evitar conflicto legal.','Trasladar la responsabilidad exclusiva a coordinación académica.','B','La autonomía docente opera dentro del marco institucional y del debido proceso.','Decreto 1290 de 2009')

crear('Inclusión','ELITE 3','Un estudiante con discapacidad presenta barreras persistentes para acceder a procesos evaluativos diseñados de forma homogénea. Algunos docentes consideran que ajustar condiciones vulnera igualdad frente al grupo.','¿Qué decisión es jurídicamente y pedagógicamente correcta?','Aplicar evaluación idéntica para garantizar trato igual formal.','Implementar ajustes razonables y apoyos acordes con necesidades identificadas.','Suspender temporalmente evaluaciones hasta nuevo concepto externo.','Delegar completamente la responsabilidad a la familia.','B','La igualdad material exige ajustes razonables para garantizar acceso efectivo.','Decreto 1421 de 2017')

crear('Convivencia','ELITE 4','En una institución se presenta un conflicto reiterado entre estudiantes con escalamiento progresivo, afectación del clima escolar y denuncias cruzadas. Un directivo propone sanción inmediata sin agotamiento de protocolos por presión comunitaria.','¿Cuál respuesta institucional es correcta?','Aplicar sanción ejemplar inmediata sin procedimiento.','Activar la ruta institucional garantizando debido proceso y enfoque restaurativo según el caso.','Excluir preventivamente a todos los involucrados.','Esperar nuevos incidentes para evitar sobreintervención.','B','La gestión de convivencia exige procedimientos institucionales y garantías.','Ley 1620 de 2013')

crear('Didáctica','ELITE 5','Un docente busca mejorar comprensión profunda en un grupo que responde adecuadamente a pruebas de memoria pero fracasa al analizar situaciones nuevas.','¿Qué estrategia didáctica es más pertinente?','Incrementar talleres repetitivos de memorización.','Diseñar secuencias didácticas con activación, construcción, aplicación y retroalimentación.','Reducir complejidad conceptual del currículo.','Limitar evaluación a preguntas cerradas.','B','La secuencia didáctica favorece aprendizaje progresivo y transferencia.','Lineamientos MEN')

crear('Gestión Escolar','ELITE 6','La institución adelanta revisión estratégica de su identidad, prioridades curriculares y mecanismos de articulación comunitaria. Algunos actores confunden instrumentos operativos con orientadores institucionales.','¿Qué instrumento articula el horizonte institucional?','Cronograma académico.','Proyecto Educativo Institucional.','Manual de asistencia.','Registro disciplinario.','B','El PEI orienta identidad, fines y organización institucional.','Ley 115 de 1994')

crear('Pedagogía','ELITE 7','Un colectivo docente debate si evaluar debe limitarse a certificar resultados finales o acompañar el aprendizaje durante el proceso con información útil para mejorar desempeño.','¿Qué enfoque responde mejor a una evaluación orientada al aprendizaje?','Evaluación exclusivamente sumativa.','Evaluación formativa continua con retroalimentación pertinente.','Eliminación de criterios explícitos.','Promedio automático de actividades sin análisis.','B','La evaluación formativa fortalece regulación del aprendizaje.','Decreto 1290 de 2009')

crear('Normatividad','ELITE 8','Durante revisión del manual de convivencia se propone incorporar sanciones discrecionales inmediatas frente a faltas ambiguas para acelerar decisiones institucionales.','¿Qué principio limita esta propuesta?','Conveniencia administrativa.','Debido proceso y tipicidad procedimental institucional.','Autonomía absoluta directiva.','Respuesta ejemplarizante inmediata.','B','La regulación institucional debe respetar garantías procedimentales.','Ley 1620 de 2013')

crear('Gestión Escolar','ELITE 9','La rectoría busca mejorar resultados académicos sostenibles mediante transformación cultural, acompañamiento docente y decisiones basadas en evidencia.','¿Qué tipo de liderazgo es más pertinente?','Autoritario centrado solo en control.','Liderazgo pedagógico colaborativo orientado a mejora continua.','Gestión reactiva sin seguimiento.','Delegación fragmentada sin visión compartida.','B','El liderazgo pedagógico impulsa mejora institucional sostenible.','Orientaciones MEN')

crear('Didáctica','ELITE 10','En un proceso de aprendizaje interdisciplinar se pretende fortalecer pensamiento crítico, formulación de hipótesis y resolución contextualizada de problemas auténticos.','¿Qué estrategia se alinea mejor?','Dictado repetitivo centrado en reproducción textual.','Aprendizaje basado en problemas con acompañamiento estructurado.','Memorización de respuestas modelo.','Evaluación única final sin proceso.','B','El ABP favorece razonamiento aplicado y construcción activa.','Orientaciones MEN')

sim, _ = Simulacro.objects.get_or_create(nombre='Simulacro CNSC General Premium')
sim.descripcion = 'Simulacro premium CNSC elite'
sim.tipo = 'simulacro'
sim.tiempo_limite_minutos = 120
sim.puntaje_minimo_aprobacion = 70
sim.activo = True
sim.save()
sim.preguntas.clear()
sim.preguntas.add(*preguntas)

print('CARGA ELITE OK')
print('Preguntas elite:', len(preguntas))
