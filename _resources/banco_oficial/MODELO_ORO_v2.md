# Modelo Oro — Banco Oficial de Ítems (v2, validado)

**Estado:** v2 — corrige v1 tras auditoría contra 8 criterios explícitos de nivel CNSC. Ningún ítem está insertado en la base de datos.

**Qué cambió respecto a v1:** los ítems MO-LC-001, MO-CP-001 y MO-AC-001 se reconstruyeron por completo (v1 quedó como registro histórico en `MODELO_ORO_v1.md`, no se borra — Constitución Cap. 12, control de versiones). MO-NE-001 y MO-IE-001 se mantienen con ajustes menores de longitud.

---

## Registro de validación (8 criterios, por ítem)

| Criterio | MO-LC-001 | MO-NE-001 | MO-CP-001 | MO-IE-001 | MO-AC-001 |
|---|---|---|---|---|---|
| 1. Nivel CNSC real (no genérico) | ✔ (v2) | ✔ | ✔ (v2) | ✔ | ✔ |
| 2. No estilo ICFES/Saber Pro/universitario | ✔ (v2 — v1 fallaba: pedía leer un dato estadístico, no decidir) | ✔ | ✔ (v2 — v1 era técnica pedagógica genérica) | ✔ | ✔ |
| 3. ≥2 competencias en la decisión | ✔ 3 (lectura + normativa/convivencia + decisión institucional) | ✔ 2 (lectura + normativa) | ✔ 2 (retroalimentación + alineación curricular) | ✔ 3 (lectura + normativa + inclusión) | ✔ 2 (comunicación + liderazgo) |
| 4. Distractores = decisiones plausibles, no negaciones del texto | ✔ | ✔ | ✔ | ✔ | ✔ |
| 5. Correcta = mejor decisión, no obvia | ✔ | ✔ | ✔ | ✔ (B usa literalmente "ajuste razonable" para nombrar una exoneración) | ✔ |
| 6. Complejidad real, exige experiencia | ✔ | ✔ | ✔ (v2 — se agregó tensión curricular institucional) | ✔ | ✔ (v2 — contexto ampliado) |
| 7. Longitud dentro del estándar del módulo | ✔ ~180 palabras (150-300) | ✔ ~155 palabras (150-250) | ✔ ~185 palabras (180-300) | ✔ ~175 palabras (150-250) | ✔ ~165 palabras (150-300) |
| 8. Sirve como plantilla replicable | ✔ | ✔ | ✔ | ✔ | ✔ |

---

## ÍTEM 1 (v2) — Lectura Crítica

| Campo | Valor |
|---|---|
| Código | MO-LC-001 |
| Módulo / Subtema | Lectura Crítica / Inferencia textual + Lectura de datos escolares |
| Competencias integradas | Lectura crítica + interpretación normativa (convivencia escolar) + toma de decisiones institucional |
| Área | `lectura_critica` |
| Dificultad | Alto |
| Proceso cognitivo | Nivel 4 — Evaluación y juicio |
| Tipo de ítem | Estándar (binario) |

**Por qué se reconstruyó:** la v1 pedía identificar un problema de causalidad estadística (tres variables que cambiaron a la vez) — un razonamiento válido pero cercano a comprensión lectora académica, sin una decisión profesional con consecuencias reales. La v2 exige lo mismo en materia de lectura rigurosa (distinguir lo documentado de lo inferido) pero aplicado a una decisión institucional real, con un manual de convivencia de por medio.

**Contexto:**
El coordinador de convivencia de una institución educativa recibió un informe escrito, elaborado por la docente de aula, sobre un incidente ocurrido durante el descanso entre dos estudiantes de grado octavo. El informe describe que uno de los estudiantes empujó al otro contra la pared del patio en medio de un forcejeo por un balón, que ambos se retiraron por su cuenta antes de que algún docente pudiera intervenir directamente, y que ninguno presentó lesión visible ni acudió a la enfermería después del incidente. El informe no menciona antecedentes previos de conflicto entre los dos estudiantes, ni registra que alguno haya expresado temor de volver a coincidir con el otro en el mismo espacio. El Manual de Convivencia Escolar de la institución distingue entre situaciones tipo I, manejables mediante el diálogo y la mediación cotidiana entre pares, y situaciones tipo II, que exigen activar una ruta de mayor seguimiento por su afectación o riesgo. Con esa información, el coordinador debe decidir qué ruta activar antes de que finalice la jornada.

**Enunciado:** ¿Qué decisión es la más coherente exclusivamente con lo que el informe documenta?

- **A. (correcta)** Tratar el incidente como una situación tipo I, dado que el informe describe un forcejeo sin lesión ni antecedentes documentados, y activar la mediación entre pares prevista para ese nivel.
- B. Clasificar el incidente como tipo II de inmediato y citar con carácter urgente a las familias de ambos estudiantes, porque todo contacto físico entre estudiantes exige siempre el protocolo más alto disponible.
- C. Cerrar el caso sin ninguna actuación adicional, dado que ninguno de los dos estudiantes presentó lesión visible ni acudió a la enfermería tras el incidente.
- D. Solicitar a la docente que amplíe el informe con antecedentes previos entre los estudiantes, y suspender cualquier decisión sobre la ruta hasta contar con esa información adicional.

**Justificación:** El informe documenta un forcejeo sin lesión y sin antecedentes registrados — exactamente el perfil de una situación tipo I según el propio manual institucional. A es correcta porque actúa con lo que el texto realmente soporta, ni más ni menos. B sobredimensiona el incidente: trata "todo contacto físico" como automáticamente tipo II, una regla que el manual no establece y que el informe no sustenta. C confunde ausencia de lesión física con ausencia de necesidad de intervención, ignorando que incluso las situaciones tipo I requieren mediación, no cierre sin actuación. D es una forma de inacción disfrazada de prudencia: nada en el manual exige agotar antecedentes antes de dar una respuesta inicial proporcionada, y aplazar la decisión dentro de la misma jornada no está justificado por el caso.

**Validación Cognitiva (Cap. 11.0):** los 8 criterios se cumplen — la respuesta exige distinguir lo documentado de lo que un lector apresurado podría sobreinferir (B) o subestimar (C), y decidir en consecuencia dentro de un marco normativo institucional real.

---

## ÍTEM 2 — Normatividad Educativa

*(Sin cambios de fondo respecto a v1 — ya cumplía los 8 criterios; se ajustó ligeramente la redacción de la justificación.)*

| Campo | Valor |
|---|---|
| Código | MO-NE-001 |
| Módulo / Subtema | Normatividad Educativa / Decreto 1290 y SIEE |
| Competencias integradas | Lectura crítica + interpretación normativa (debido proceso evaluativo) |
| Área | `general` |
| Fuente normativa | Decreto 1290 de 2009, art. 4 (Sistema Institucional de Evaluación de los Estudiantes) |
| Dificultad | Alto |
| Proceso cognitivo | Nivel 3 — Análisis situacional |
| Tipo de ítem | Estándar (binario) |

**Contexto:**
Un estudiante de grado noveno faltó a la entrega de un trabajo final de ciencias sociales porque estuvo hospitalizado durante tres días, situación que la familia notificó a la institución mediante una incapacidad médica radicada en la coordinación de convivencia al día siguiente de su reingreso. El docente del área, sin conocer aún esa notificación, calificó el trabajo con la nota mínima de la escala institucional por no haberse entregado en la fecha establecida, aplicando el mismo criterio que usa para cualquier entrega tardía. Al enterarse de la incapacidad médica, la coordinación remitió el caso al docente y le recordó que el Sistema Institucional de Evaluación de los Estudiantes contempla un procedimiento de evaluación de suficiencia para ausencias justificadas, con un plazo de cinco días hábiles tras el reintegro del estudiante. El docente respondió que, aunque reconoce la situación médica, prefiere mantener la nota asignada para no generar un precedente de excepciones frente al resto del curso.

**Enunciado:** ¿Cuál actuación del docente se ajusta mejor al debido proceso evaluativo?

- **A. (correcta)** Activar el procedimiento de evaluación de suficiencia previsto en el SIEE para la ausencia justificada, dentro del plazo establecido, en lugar de mantener una sanción aplicada antes de conocer la incapacidad médica.
- B. Mantener la nota mínima asignada, dado que el criterio de puntualidad en las entregas se aplicó de manera uniforme a todo el curso sin excepciones.
- C. Otorgar automáticamente la nota máxima de la escala como compensación por la situación médica, sin aplicar ningún procedimiento de evaluación adicional.
- D. Remitir la decisión final al acudiente, para que sea la familia quien determine la nota que debe recibir el estudiante.

**Justificación:** El Decreto 1290 exige que el SIEE de cada institución defina procedimientos de evaluación extraordinaria ante ausencias justificadas; el caso confirma que la institución ya tiene ese procedimiento y que la ausencia fue notificada dentro del plazo. A es correcta porque aplica ese mecanismo, ya vigente, en lugar de sostener una sanción impuesta antes de conocerse la incapacidad. B confunde uniformidad de criterio con justicia evaluativa: aplicar la misma regla a una ausencia ya justificada que a una entrega simplemente tardía ignora la notificación recibida. C reemplaza una decisión arbitraria por otra igual de arbitraria en sentido contrario, sin evaluar en ningún momento el aprendizaje real del estudiante. D traslada indebidamente a la familia una decisión académica que corresponde a la institución dentro de su propio SIEE.

**Validación Cognitiva (Cap. 11.0):** cumple los 8 criterios — A y B compiten genuinamente por parecer razonables (uniformidad vs. debido proceso), exigiendo comparar antes de decidir cuál respeta mejor la norma.

---

## ÍTEM 3 (v2) — Competencias Pedagógicas

| Campo | Valor |
|---|---|
| Código | MO-CP-001 |
| Módulo / Subtema | Competencias Pedagógicas / Retroalimentación efectiva + Alineación curricular |
| Competencias integradas | Evaluación formativa + alineación curricular institucional |
| Área | `componente_pedagogico` |
| Dificultad | Alto |
| Proceso cognitivo | Nivel 4 — Evaluación y juicio |
| Tipo de ítem | Estándar (binario) |

**Por qué se reconstruyó:** la v1 solo exigía identificar "buena técnica de retroalimentación" frente a una mala — válido, pero sin la tensión institucional (tiempo, plan curricular aprobado, compromisos ya asumidos con el consejo académico) que distingue una decisión de nivel CNSC de una recomendación pedagógica genérica de cualquier certificación docente.

**Contexto:**
En una institución educativa urbana, la docente de matemáticas de grado séptimo revisó las evaluaciones parciales de los tres últimos periodos y encontró que un grupo numeroso de estudiantes repetía el mismo error al resolver problemas con fracciones: aplicaban el algoritmo de suma sin encontrar primero un denominador común. La malla curricular aprobada por el consejo académico establece que, a partir de la semana siguiente, el grupo debe iniciar el tema de proporcionalidad, antes de presentar la prueba institucional de mitad de año, que evalúa ambos temas por igual. Al revisar los cuadernos de los estudiantes con mayor dificultad, la docente confirmó que habían corregido mecánicamente el resultado copiando la respuesta del compañero más cercano, sin ninguna evidencia de haber comprendido en qué paso del procedimiento se originaba el error. La coordinación académica ya había advertido al equipo de matemáticas que el cronograma de la prueba institucional no tiene margen de aplazamiento este año.

**Enunciado:** ¿Qué decisión atiende mejor el error identificado sin desconocer el plan curricular ya aprobado?

- **A. (correcta)** Dedicar una sesión corta y explícita a corregir el paso específico del error antes de iniciar proporcionalidad, y retomarlo brevemente en las primeras clases del nuevo tema con ejercicios que integren ambos contenidos.
- B. Detener por completo el avance del plan curricular y dedicar las próximas dos semanas exclusivamente a repasar fracciones, aunque eso implique no alcanzar a ver proporcionalidad antes de la prueba institucional.
- C. Avanzar a proporcionalidad según lo previsto en la malla curricular, sin dedicar tiempo adicional a fracciones, confiando en que los estudiantes corrijan el error por su cuenta con la práctica del nuevo tema.
- D. Solicitar al consejo académico que retire el tema de fracciones de la prueba institucional de mitad de año, dado que el grupo no alcanzó el nivel esperado en ese contenido.

**Justificación:** A es correcta porque resuelve la causa raíz del error (el paso preciso del procedimiento) sin romper el compromiso curricular ya aprobado, integrando el refuerzo dentro del avance en lugar de tratarlos como bloques excluyentes. B corrige el problema pedagógico, pero al costo de desconocer unilateralmente un plan aprobado por el consejo académico y comprometer el cronograma institucional sin haber agotado alternativas menos disruptivas. C prioriza el cumplimiento del cronograma ignorando una causa ya diagnosticada, apostando a una corrección espontánea que el propio caso desmiente (los estudiantes copian, no comprenden). D traslada la responsabilidad pedagógica a una decisión institucional ajena a su alcance como docente, en lugar de resolver desde la práctica de aula lo que sí está en su margen de acción.

**Validación Cognitiva (Cap. 11.0):** cumple los 8 criterios — B es un distractor fuerte porque *sí* resuelve el problema pedagógico, exigiendo que el aspirante pondere ese acierto parcial contra el costo institucional que ignora.

---

## ÍTEM 4 — Inclusión Educativa

*(Sin cambios de fondo respecto a v1 — ya cumplía los 8 criterios; se amplió ligeramente el contexto para reforzar la trazabilidad del proceso previo del PIAR.)*

| Campo | Valor |
|---|---|
| Código | MO-IE-001 |
| Módulo / Subtema | Inclusión Educativa / PIAR y ajustes razonables |
| Competencias integradas | Lectura crítica + interpretación normativa + inclusión (ajuste vs. exoneración) |
| Área | `general` |
| Fuente normativa | Decreto 1421 de 2017 |
| Dificultad | Muy Alto |
| Proceso cognitivo | Nivel 4 — Evaluación y juicio |
| Tipo de ítem | Estándar (binario) |

**Contexto:**
Un estudiante de grado quinto con diagnóstico de dislexia cuenta con un Plan Individual de Ajustes Razonables construido al inicio del año escolar por el equipo de apoyo pedagógico junto con la familia, tras una valoración formal, y socializado con todos los docentes que atienden al estudiante. El plan establece tiempo adicional para las pruebas escritas y materiales de lectura con tipografía y espaciado adaptados. Durante el segundo periodo, el docente de lenguaje decidió, por iniciativa propia y sin consultar al equipo de apoyo, que el estudiante quedaría exonerado de todas las actividades de producción escrita del área, calificándolo únicamente con base en su participación oral en clase. El docente argumentó ante la coordinación que esa decisión era, en sus palabras, "el ajuste razonable más adecuado" para no generar frustración en el estudiante frente a una habilidad que le resulta más difícil.

**Enunciado:** ¿Qué actuación es la más coherente con el Decreto 1421 de 2017 ante esta situación?

- **A. (correcta)** Revisar la decisión con el equipo de apoyo pedagógico y ajustar la actividad escrita a lo ya definido en el Plan Individual de Ajustes Razonables, en lugar de eliminar por completo la producción escrita del área.
- B. Mantener la exoneración total de actividades escritas decidida por el docente, dado que evita la frustración que el estudiante podría sentir frente a una tarea más exigente para él.
- C. Solicitar a la familia que asuma en casa el refuerzo de la producción escrita, ya que es un aspecto que la institución considera fuera de su alcance actual.
- D. Suspender temporalmente la calificación del área de lenguaje hasta que el equipo de apoyo pedagógico determine si el estudiante debe continuar en el grado quinto.

**Justificación:** El Decreto 1421 exige que los ajustes surjan del proceso ya definido con el equipo de apoyo y remuevan barreras sin eliminar el objeto de aprendizaje; el estudiante ya contaba con un ajuste vigente que el docente reemplazó unilateralmente por una exoneración total. A es correcta porque restituye el proceso y el ajuste ya acordados. B confunde exoneración con ajuste razonable — el error central que el Decreto 1421 busca prevenir, y repite textualmente el argumento erróneo del docente del caso. C traslada indebidamente a la familia una responsabilidad institucional, contrario al principio de corresponsabilidad con liderazgo de la institución. D es desproporcionada: nada en el caso cuestiona la promoción de grado del estudiante.

**Validación Cognitiva (Cap. 11.0):** cumple los 8 criterios — B es el distractor de mayor exigencia de todo el Modelo Oro porque usa el propio lenguaje técnico correcto ("ajuste razonable") para justificar la decisión incorrecta.

---

## ÍTEM 5 (v2) — Análisis de Casos (idoneidad graduada)

| Campo | Valor |
|---|---|
| Código | MO-AC-001 |
| Módulo / Subtema | Análisis de Casos / Comunicación asertiva + Liderazgo sin autoridad formal |
| Competencias integradas | Comunicación asertiva bajo presión + liderazgo sin autoridad formal |
| Área | `psicotecnico` |
| Dificultad | Alto |
| Proceso cognitivo | Nivel 4 — Evaluación y juicio |
| Tipo de ítem | `mas_adecuada` (idoneidad graduada 0-4) |

**Por qué se reconstruyó:** la v1 tenía un contexto de ~110 palabras, por debajo del mínimo de 150 exigido para este módulo — insuficiente para sostener la complejidad que exige el criterio 6. La v2 mantiene el mismo dilema pero añade información real (la muestra pública ya comprometida con las familias, el historial del colega de plantear objeciones válidas por el canal correcto en otras ocasiones) que obliga a un juicio más fino, no a una reacción genérica.

**Contexto:**
Durante una reunión de escuela de padres, un docente que lidera un proyecto transversal entre tres áreas presentó el cronograma de entregas acordado semanas atrás con el resto del equipo docente, pensado para culminar en una muestra pública de los trabajos de los estudiantes antes del cierre del periodo. En medio de la reunión, uno de los colegas del equipo interrumpió públicamente para decir que no estaba de acuerdo con ese cronograma y que, en su opinión, debería cambiarse por completo, sin haber planteado antes esa objeción en ninguna de las reuniones previas de planeación del proyecto. Ese mismo colega había manifestado en otras ocasiones observaciones válidas sobre el proyecto, pero siempre lo había hecho directamente en las reuniones de equipo, nunca frente a las familias. Varios acudientes presentes quedaron visiblemente confundidos sobre cuál era en realidad la fecha de entrega vigente, y algunos empezaron a hacer preguntas dirigidas directamente al colega que había interrumpido, mientras la muestra pública seguía programada para la fecha ya anunciada a las familias.

**Enunciado:** ¿Cuál es la respuesta MÁS adecuada ante esta situación?

| Opción | Idoneidad | Descripción |
|---|---|---|
| **A** | **4 (correcta)** | Sostener con calma el cronograma ya acordado ante los acudientes, confirmando la fecha de la muestra pública, y proponerle al colega revisar su objeción en una reunión de equipo posterior a la jornada. |
| B | 1 | Cambiar en el momento el cronograma según lo que propone el colega, para evitar que la discusión continúe frente a los acudientes, aunque el resto del equipo no esté presente para validar ese cambio. |
| C | 2 | Pedirle al colega, delante de los acudientes, que explique por qué nunca planteó esa objeción antes, en ninguna de las reuniones de planeación del proyecto que ya se realizaron. |
| D | 0 | No responder en el momento y esperar a que la reunión termine, sin aclarar ante los acudientes cuál es la fecha de entrega y de la muestra pública realmente vigente. |

**Justificación:** A obtiene la idoneidad máxima porque protege simultáneamente la claridad ante las familias, la fecha ya comprometida de la muestra pública, y la relación con el colega, atendiendo su objeción sin escalarla públicamente. B (idoneidad 1) cede el cronograma bajo presión, premia la interrupción pública y compromete una fecha ya anunciada sin que el resto del equipo la valide. C (idoneidad 2) es la opción más tentadora: señala algo cierto (el colega debió objetar antes) pero lo hace escalando el conflicto entre colegas frente a las familias, en el peor momento posible. D (idoneidad 0) dejaría a los acudientes sin ninguna claridad sobre una fecha que ya les fue anunciada — el daño más directo e inmediato de las cuatro opciones, aunque comprensible como reacción bajo presión.

**Validación Cognitiva (Cap. 11.0):** cumple los 8 criterios — C es deliberadamente la opción más difícil de descartar, porque tener razón en el fondo del desacuerdo no equivale a haber actuado correctamente en la forma y el momento.

---

## Resumen para aprobación final

Los 5 ítems (v2) cumplen simultáneamente los 8 criterios verificados en la tabla inicial. Ningún ítem está insertado en la base de datos.

Quedo a la espera de tu aprobación final para fijar esta versión (v2) como el estándar obligatorio del Banco Oficial de Preguntas.
