# -*- coding: utf-8 -*-
"""Contenido reescrito para los 35 items TJS "generados" que compartian
distractores identicos entre competencias distintas (ver auditoria).
Cada entrada reemplaza contexto/opciones/justificacion del item original
(identificado por codigo) y agrega idoneidad graduada (0-4) por opcion.
Escala: 4=optima, 3=adecuada pero incompleta, 1=poco adecuada (evasiva),
0=inadecuada (autoritaria, antietica o que omite responsabilidad).
"""

ITEMS = {
    "INI-COM-008": {
        "contexto": (
            "Usted es docente provisional en una institucion urbana y lleva tres semanas notando "
            "que los estudiantes que ingresaron a mitad de periodo no recibieron ninguna induccion "
            "sobre horarios, canales de comunicacion ni el SIEE. Como resultado, varios han sido "
            "reportados por llegar tarde a evaluaciones que no sabian que existian, y dos familias ya "
            "reclamaron por escrito. Coordinacion no ha asignado a nadie esa tarea y el periodo "
            "academico cierra en diez dias."
        ),
        "opcion_a": "Elaborar en el dia una guia breve de induccion con la informacion esencial, entregarla a los estudiantes nuevos y a sus acudientes, y proponer a coordinacion que se formalice como protocolo para el proximo ingreso.",
        "opcion_b": "Enviar un correo a coordinacion señalando el vacio y esperar instrucciones antes de actuar directamente con los estudiantes, para no exceder su rol como docente de aula.",
        "opcion_c": "Aplicar las evaluaciones pendientes sin ajustes, argumentando que la induccion es responsabilidad exclusiva de la coordinacion y no del docente de aula.",
        "opcion_d": "Reunir a los estudiantes nuevos y anunciarles que a partir de ahora seran evaluados con mayor severidad para que aprendan a informarse por su cuenta.",
        "idoneidad": {"a": 4, "b": 2, "c": 1, "d": 0},
        "justificacion": "La opcion mas adecuada actua sobre la causa (falta de induccion) con una solucion inmediata y proporcional, y ademas la convierte en mejora institucional duradera. Escalar sin actuar retrasa una solucion urgente; desentenderse del problema ignora el efecto sobre estudiantes que no tuvieron responsabilidad en el vacio; y endurecer la evaluacion como castigo es desproporcionado y ajeno al problema real.",
    },
    "INI-COM-009": {
        "contexto": (
            "Usted trabaja en una escuela rural dispersa donde la conectividad es intermitente. Durante "
            "el ultimo mes, las tareas digitales enviadas por la coordinacion academica no han podido "
            "completarse en la mayoria de los hogares, y el rendimiento del grupo ha bajado de forma "
            "notoria. Al revisar la biblioteca de la sede, encuentra guias impresas y material didactico "
            "en buen estado que casi no se ha usado en los ultimos dos años."
        ),
        "opcion_a": "Reconocer la limitacion de conectividad, adaptar las actividades al material impreso disponible y acordar con el equipo docente un plan de seguimiento que documente el avance de cada estudiante.",
        "opcion_b": "Reducir temporalmente la exigencia academica del grupo hasta que la conectividad mejore, sin definir un plan alternativo de trabajo mientras tanto.",
        "opcion_c": "Insistir en el uso exclusivo de las tareas digitales tal como fueron diseñadas, indicando que cualquier adaptacion debe esperar a que la coordinacion apruebe un cambio formal.",
        "opcion_d": "Culpar públicamente a las familias por no gestionar mejor el acceso a internet, sin revisar si existen alternativas pedagogicas disponibles en la propia institucion.",
        "idoneidad": {"a": 4, "b": 1, "c": 0, "d": 0},
        "justificacion": "La respuesta MENOS adecuada es imponer una via que ya demostro no funcionar mientras se culpa a las familias por una condicion estructural que no controlan; ademas ignora recursos disponibles en la propia sede. Reducir la exigencia sin plan alterno tambien es problematico, pero al menos no traslada la responsabilidad de forma injusta. Insistir en el canal digital sin adaptarlo desconoce la evidencia del propio contexto.",
    },
    "INI-COM-010": {
        "contexto": (
            "Como docente de ciencias sociales, viene observando que varias familias desconocen como "
            "funciona el SIEE de la institucion: no saben cuando se publican notas, como solicitar una "
            "revision ni los plazos para hacerlo. Esto ha generado reclamos tardios, algunos ya fuera "
            "del plazo reglamentario, que generan tension innecesaria entre acudientes y coordinacion "
            "al cierre de cada periodo."
        ),
        "opcion_a": "Diseñar una comunicacion breve y clara sobre el SIEE (fechas, canales y plazos de reclamacion) para socializarla en la proxima reunion de padres y proponerla como practica permanente del area.",
        "opcion_b": "Explicar el SIEE de forma individual solo a las familias que reclamen directamente con usted, sin generalizar la informacion al resto del grupo.",
        "opcion_c": "Indicar a las familias que consulten el SIEE por su cuenta en la pagina institucional, sin verificar si tienen acceso real a ese canal.",
        "opcion_d": "Aceptar reclamos fuera de plazo de manera informal para evitar conflictos, sin remitirlos al procedimiento formal establecido por el SIEE.",
        "idoneidad": {"a": 4, "b": 2, "c": 1, "d": 0},
        "justificacion": "Prevenir el problema con informacion oportuna y de alcance colectivo es la accion mas coherente con la orientacion al logro y la iniciativa docente. Resolver caso por caso no previene la recurrencia; remitir a un canal sin verificar accesibilidad desatiende al usuario real; y aceptar reclamos informales fuera de plazo vulnera el debido proceso institucional que el propio SIEE establece.",
    },
    "INI-COM-011": {
        "contexto": (
            "En su aula inclusiva tiene un estudiante con barreras de aprendizaje que depende de "
            "adaptaciones especificas -tiempo extendido, formato de letra ampliada y apoyos visuales- "
            "que solo usted conoce, porque las acordo informalmente hace dos años y nunca quedaron "
            "registradas en el PIAR. Esta semana se entera de que sera trasladado a otro grado el "
            "proximo periodo."
        ),
        "opcion_a": "Documentar formalmente las adaptaciones en el PIAR del estudiante, articularlas con el equipo de orientacion y entregar la informacion al docente que continuara el proceso antes del traslado.",
        "opcion_b": "Escribir una nota informal para el proximo docente explicando las adaptaciones, sin gestionar su incorporacion formal al PIAR.",
        "opcion_c": "No compartir la informacion, considerando que cada docente debe descubrir por su cuenta las necesidades de sus estudiantes.",
        "opcion_d": "Solicitar que el estudiante permanezca con usted indefinidamente para evitar que el proceso se pierda, sin gestionar la continuidad institucional del caso.",
        "idoneidad": {"a": 4, "b": 2, "c": 0, "d": 1},
        "justificacion": "La continuidad pedagogica real se garantiza formalizando el PIAR, no dependiendo de la memoria de un solo docente. Una nota informal ayuda pero es fragil y no queda protegida institucionalmente. Omitir la informacion pone en riesgo directo el derecho a la educacion del estudiante. Retener al estudiante evita el problema en lugar de resolverlo de fondo.",
    },
    "INI-COM-012": {
        "contexto": (
            "En la jornada de la tarde, un grupo de estudiantes llega tarde de forma recurrente porque "
            "el unico bus que cubre su ruta rural sufre retrasos frecuentes. El equipo docente ha optado "
            "por registrar la tardanza como falta disciplinaria sin excepcion, y ya hay tres estudiantes "
            "en riesgo de perder el periodo por acumulacion de fallas que no dependen de ellos."
        ),
        "opcion_a": "Analizar con el equipo docente las causas reales de las tardanzas, proponer un ajuste razonable para los casos de transporte verificable y mantener el registro sin penalizar injustamente.",
        "opcion_b": "Solicitar que se revise el caso en el comite de convivencia antes de aplicar cualquier sancion adicional a los estudiantes afectados.",
        "opcion_c": "Mantener el registro de faltas sin excepcion, argumentando que flexibilizar la norma para unos estudiantes seria injusto frente al resto del grupo.",
        "opcion_d": "Excusar automaticamente a todos los estudiantes de esa ruta sin verificar caso por caso, para evitar el desgaste de revisar cada situacion.",
        "idoneidad": {"a": 4, "b": 3, "c": 0, "d": 1},
        "justificacion": "La respuesta MENOS adecuada es sostener una norma de forma rigida sin analizar la causa, penalizando a estudiantes por una circunstancia estructural ajena a su voluntad. Excusar sin verificar tambien es problematico porque no distingue casos reales de excusas injustificadas. Elevar el caso a comite es razonable pero mas lento que resolverlo con analisis directo del equipo docente.",
    },
    "INI-COM-013": {
        "contexto": (
            "Como docente de tecnologia, tiene acceso a los reportes de asistencia, desempeño academico "
            "y observador de convivencia de su grado. Al revisarlos por separado nota que ningun area "
            "cruza esta informacion, aunque varios estudiantes muestran señales combinadas -ausentismo "
            "creciente, bajas notas y anotaciones de aislamiento social- que podrian anticipar un riesgo "
            "de desercion si nadie interviene pronto."
        ),
        "opcion_a": "Cruzar los tres tipos de datos para identificar los casos de mayor riesgo, presentar el hallazgo a coordinacion y proponer un protocolo de alerta temprana compartido entre areas.",
        "opcion_b": "Informar el hallazgo solo al director de grupo de cada estudiante, sin proponer un mecanismo que se sostenga en el tiempo.",
        "opcion_c": "Guardar la observacion para si mismo, considerando que no es su funcion revisar informacion de otras areas.",
        "opcion_d": "Publicar la lista de estudiantes en riesgo en la sala de profesores para que cualquier docente la consulte libremente.",
        "idoneidad": {"a": 4, "b": 2, "c": 0, "d": 0},
        "justificacion": "La iniciativa mas valiosa convierte una observacion aislada en un mecanismo institucional replicable. Informar solo puntualmente ayuda a corto plazo pero no previene que el patron se repita. Callar la informacion desaprovecha una alerta temprana real. Exponer los datos sin control vulnera la confidencialidad de los estudiantes, incluso con buena intencion.",
    },
    "INI-COM-014": {
        "contexto": (
            "En educacion artistica, nota que la participacion de su grupo mejora notablemente cuando "
            "conecta las actividades con problemas reales de la comunidad -un mural sobre el rio "
            "contaminado, una obra sobre el reciclaje del barrio-, comparado con las guias estandar del "
            "plan de area. Sin embargo, nunca ha registrado por que funciona ni ha compartido la "
            "estrategia con sus colegas."
        ),
        "opcion_a": "Sistematizar la estrategia (que se hizo, por que funciono, que evidencias de aprendizaje produjo) y compartirla en la proxima reunion de area como una practica replicable.",
        "opcion_b": "Seguir aplicando la estrategia en su propia aula sin documentarla, confiando en que su efecto se mantendra igual con el tiempo.",
        "opcion_c": "Reservarse la estrategia como un metodo personal, sin compartirla con el area para evitar que otros la usen sin reconocerle el merito.",
        "opcion_d": "Presentarla directamente a rectoria como una innovacion institucional sin antes validarla ni compartirla con el equipo de area que la aplicaria.",
        "idoneidad": {"a": 4, "b": 1, "c": 0, "d": 1},
        "justificacion": "La iniciativa docente de mayor valor no se queda en la practica individual: se documenta y se comparte para que otros puedan aprovecharla. No registrar la estrategia arriesga perderla o no poder sostenerla. Guardarla por interes personal contradice el sentido colaborativo de la funcion docente. Saltar directamente a rectoria sin el aval del area que la aplicaria es un atajo que debilita la apropiacion real de la practica.",
    },
    "INI-COM-015": {
        "contexto": (
            "En lengua castellana, ha identificado a varios estudiantes con talento evidente para "
            "concursos de oratoria y olimpiadas academicas, pero ninguno ha participado en los ultimos "
            "dos años porque nadie en la institucion sistematiza las convocatorias externas ni "
            "acompaña el proceso de inscripcion. Se entera de una convocatoria regional con cierre en "
            "cinco dias."
        ),
        "opcion_a": "Gestionar de inmediato la inscripcion de los estudiantes con mayor potencial, informar a sus familias y proponer a coordinacion crear un mecanismo permanente de seguimiento a convocatorias.",
        "opcion_b": "Informar a los estudiantes sobre la convocatoria y dejar que ellos mismos gestionen la inscripcion sin acompañamiento adicional.",
        "opcion_c": "No informar sobre la convocatoria por considerar que, al no haber un canal institucional establecido, no es su responsabilidad gestionarla.",
        "opcion_d": "Inscribir a los estudiantes sin informar a sus familias, para no exponerse a que ellas decidan no autorizar la participacion.",
        "idoneidad": {"a": 4, "b": 2, "c": 0, "d": 0},
        "justificacion": "La respuesta MENOS adecuada es omitir una oportunidad real de desarrollo del estudiante escudandose en la ausencia de un procedimiento formal, cuando el docente si tiene la informacion y el tiempo para actuar. Informar sin acompañar deja la gestion en manos de estudiantes que probablemente no conocen el proceso. Inscribir sin informar a la familia, aunque bien intencionado, vulnera su derecho a decidir sobre la participacion de su hijo o hija.",
    },
    "LID-COM-014": {
        "contexto": (
            "Usted lidera informalmente el area de ciencias, sin cargo directivo. Propuso implementar "
            "ajustes razonables para dos estudiantes con discapacidad -tiempo adicional y formato "
            "accesible en las evaluaciones-, pero el resto del equipo docente los rechaza porque "
            "considera que aumentan su carga de trabajo. Mientras tanto, hay evidencia de que esos "
            "estudiantes no estan accediendo plenamente a las evaluaciones actuales."
        ),
        "opcion_a": "Presentar al equipo la evidencia concreta del impacto en los estudiantes, abrir un espacio de dialogo sobre como distribuir la carga de los ajustes de forma viable, y proponer un acuerdo de seguimiento con compromisos verificables.",
        "opcion_b": "Evitar insistir en el tema para no generar mas tension con el equipo, y esperar a que coordinacion academica decida por su cuenta si corresponde exigir los ajustes.",
        "opcion_c": "Imponer los ajustes razonables en su propia asignatura sin coordinar con el resto del equipo, dejando en evidencia publicamente a quienes se niegan.",
        "opcion_d": "Remitir el caso completo a coordinacion mediante un informe extenso, sin adelantar ninguna gestion pedagogica mientras se resuelve el tramite.",
        "idoneidad": {"a": 4, "b": 1, "c": 0, "d": 1},
        "justificacion": "El liderazgo sin autoridad formal se ejerce con evidencia y construccion de acuerdos, no con imposicion ni con pasividad. Evitar el tema deja sin resolver una vulneracion real de derechos. Imponer unilateralmente y exponer a los colegas deteriora la relacion de equipo sin garantizar sostenibilidad. Trasladar todo a coordinacion sin ninguna accion inmediata retrasa una respuesta que los estudiantes necesitan ya.",
    },
    "LID-COM-015": {
        "contexto": (
            "Usted es docente provisional pero goza de alto reconocimiento entre los estudiantes. En el "
            "consejo academico, ha notado que se evita sistematicamente discutir los resultados "
            "criticos de la ultima encuesta de convivencia, porque varios directivos temen que la "
            "Secretaria de Educacion los interprete como una señal de mala gestion institucional."
        ),
        "opcion_a": "Reconocer la tension entre la imagen institucional y la necesidad de mejora, presentar la evidencia con objetividad y proponer una ruta de mejora basada en los datos de la encuesta.",
        "opcion_b": "Solicitar apoyo de la Secretaria de Educacion para que acompañe el analisis de los resultados, dejando constancia formal de los hallazgos y las acciones propuestas.",
        "opcion_c": "Sumarse a la decision de no discutir los resultados en el consejo, asumiendo que cuestionar la postura institucional podria afectar su continuidad como docente provisional.",
        "opcion_d": "Convocar una reunion breve con los miembros mas receptivos del consejo para revisar los datos de forma extraoficial, sin buscar que quede en el acta formal.",
        "idoneidad": {"a": 4, "b": 3, "c": 0, "d": 2},
        "justificacion": "La respuesta MENOS adecuada es evitar el tema por temor a las consecuencias sobre su propia situacion laboral, priorizando la conveniencia personal sobre la responsabilidad etica de mejorar la convivencia escolar. Buscar acuerdos informales sin registro formal es mejor que el silencio, pero deja el problema sin trazabilidad institucional. Pedir apoyo externo con evidencia documentada es una via solida, aunque menos directa que enfrentar el tema en el propio consejo.",
    },
    "MI-COM-007": {
        "contexto": (
            "Como director de grupo, recibe dos versiones contradictorias sobre una agresion verbal "
            "entre dos estudiantes durante el descanso. Antes de que pueda escuchar a los testigos, la "
            "familia de uno de los involucrados llega exigiendo una sancion inmediata para el otro "
            "estudiante, amenazando con escalar el caso a la Secretaria de Educacion si no se actua hoy "
            "mismo."
        ),
        "opcion_a": "Explicar a la familia que se activara la ruta de convivencia, escuchar a ambos estudiantes y a los testigos disponibles, y comunicar una decision basada en la evidencia recolectada en los plazos establecidos.",
        "opcion_b": "Pedir a la familia un tiempo breve para recolectar informacion de las dos partes antes de dar cualquier respuesta, sin comprometerse aun con un plazo especifico.",
        "opcion_c": "Sancionar de inmediato al estudiante señalado por la familia reclamante, para evitar que el caso escale a la Secretaria de Educacion.",
        "opcion_d": "Decirle a la familia que el caso no es prioritario y que se resolvera cuando el equipo de convivencia tenga disponibilidad, sin dar un marco de tiempo.",
        "idoneidad": {"a": 4, "b": 3, "c": 0, "d": 1},
        "justificacion": "El manejo responsable de la informacion exige verificarla antes de decidir, y comunicarlo con claridad y plazos a la familia. Sancionar bajo presion sin verificar los hechos vulnera el debido proceso y puede ser injusto. Restar prioridad al caso sin explicacion desatiende una situacion de convivencia real. Pedir tiempo sin comprometerse con un plazo es razonable pero deja a la familia sin la claridad que necesita.",
    },
    "MI-COM-008": {
        "contexto": (
            "Un informe institucional reciente concluye, con base en promedios generales, que no existe "
            "rezago academico significativo en el grado noveno. Sin embargo, al revisar los datos "
            "desagregados por grupo de estudiantes, usted observa brechas fuertes: los estudiantes con "
            "necesidades educativas especiales y los de menor nivel socioeconomico tienen resultados muy "
            "por debajo del promedio general que oculta esa diferencia."
        ),
        "opcion_a": "Presentar el analisis desagregado a coordinacion, mostrando que el promedio general oculta brechas relevantes, y proponer acciones diferenciadas para los subgrupos con mayor rezago.",
        "opcion_b": "Solicitar apoyo del equipo de orientacion para verificar los datos desagregados antes de presentarlos formalmente a coordinacion.",
        "opcion_c": "Aceptar la conclusion del informe general sin cuestionarla, asumiendo que los promedios institucionales ya reflejan el panorama completo del grado.",
        "opcion_d": "Compartir el hallazgo de forma extraoficial solo con otros docentes de confianza, sin llevarlo al espacio institucional donde se toman decisiones sobre el grado.",
        "idoneidad": {"a": 4, "b": 3, "c": 0, "d": 1},
        "justificacion": "La respuesta MENOS adecuada es aceptar sin analisis critico una conclusion que un promedio general puede estar ocultando, renunciando a la funcion de lectura critica de datos que le corresponde al docente. Compartir el hallazgo solo informalmente evita el silencio pero no lo convierte en una decision institucional. Verificar con orientacion antes de presentar es una buena practica, aunque implica un paso adicional antes de actuar.",
    },
    "MI-COM-009": {
        "contexto": (
            "La coordinacion academica le solicita publicar en la cartelera del pasillo la lista de "
            "estudiantes con bajo desempeño del grado, con el argumento de que la exposicion publica "
            "aumentara la asistencia a las sesiones de refuerzo. Usted tiene acceso directo a esos "
            "datos porque es quien lleva el registro de notas del grado."
        ),
        "opcion_a": "Explicar a coordinacion que publicar la lista vulnera la proteccion de datos de los estudiantes, y proponer una alternativa como la comunicacion privada a cada familia con invitacion directa al refuerzo.",
        "opcion_b": "Publicar la lista solo con las iniciales de los estudiantes, asumiendo que eso reduce el riesgo de exposicion publica.",
        "opcion_c": "Publicar la lista completa tal como lo pide coordinacion, priorizando cumplir la instruccion recibida sobre la proteccion de los datos de los estudiantes.",
        "opcion_d": "Negarse a publicar la lista sin ofrecer ninguna alternativa a coordinacion para lograr el objetivo de aumentar la asistencia al refuerzo.",
        "idoneidad": {"a": 4, "b": 1, "c": 0, "d": 2},
        "justificacion": "El manejo adecuado de informacion sensible protege los datos de los estudiantes y a la vez resuelve el objetivo legitimo de la coordinacion mediante un canal apropiado. Publicar con iniciales sigue exponiendo a estudiantes identificables en un grupo pequeño. Publicar la lista completa vulnera directamente su derecho a la privacidad. Negarse sin proponer alternativa deja sin resolver el objetivo pedagogico legitimo detras de la solicitud.",
    },
    "MI-COM-010": {
        "contexto": (
            "Un colega le escribe por el chat del area, compartiendo capturas de pantalla con "
            "calificaciones y comentarios sobre el comportamiento de varios estudiantes, pidiendo la "
            "opinion rapida del grupo antes de una reunion con un acudiente. El chat incluye a docentes "
            "de otras areas que no tienen relacion directa con esos estudiantes."
        ),
        "opcion_a": "Responder al colega en privado, sugerir eliminar la informacion del chat grupal y ofrecer revisar el caso en un espacio adecuado con quienes si tienen relacion directa con el estudiante.",
        "opcion_b": "Dar su opinion sobre el caso directamente en el chat grupal, sin comentar el problema de haber compartido la informacion de forma abierta.",
        "opcion_c": "Reenviar las capturas a otro colega para pedir una segunda opinion, ampliando aun mas la circulacion de la informacion del estudiante.",
        "opcion_d": "Ignorar el mensaje sin señalar el problema, dejando que la informacion continue circulando en el chat grupal.",
        "idoneidad": {"a": 4, "b": 1, "c": 0, "d": 1},
        "justificacion": "La respuesta mas adecuada corrige el manejo indebido de la informacion y a la vez ofrece un canal apropiado para resolver la necesidad real del colega. Opinar sin señalar el problema normaliza la practica. Reenviar la informacion la expone aun mas. Ignorar el mensaje permite que la exposicion de datos sensibles continue sin ninguna correccion.",
    },
    "MI-COM-011": {
        "contexto": (
            "La plataforma institucional que usa para el seguimiento academico genera reportes "
            "automaticos de asistencia y desempeño, pero en las ultimas semanas ha notado registros "
            "duplicados, fechas de actualizacion inconsistentes y datos que no coinciden con lo "
            "observado en clase. Coordinacion le pide usar esos reportes para decidir que estudiantes "
            "requieren apoyo adicional esta semana."
        ),
        "opcion_a": "Reportar las inconsistencias al equipo tecnico, contrastar los datos dudosos con su propio registro de clase antes de decidir, y aplazar unos dias las decisiones que dependan de datos no verificados.",
        "opcion_b": "Usar los reportes automaticos tal como estan, considerando que revisarlos manualmente tomaria demasiado tiempo esta semana.",
        "opcion_c": "Decidir el apoyo adicional basandose unicamente en su impresion personal de cada estudiante, sin usar ningun dato del sistema ni reportar el problema tecnico.",
        "opcion_d": "Suspender por completo el proceso de asignacion de apoyos hasta que la plataforma sea corregida, sin usar ninguna fuente alternativa de informacion mientras tanto.",
        "idoneidad": {"a": 4, "b": 1, "c": 0, "d": 1},
        "justificacion": "La respuesta MENOS adecuada descarta toda fuente de datos y decide solo por impresion personal, sin siquiera reportar el problema tecnico que afecta a toda la institucion. Usar datos que ya se saben inconsistentes tambien es riesgoso, aunque menos grave que prescindir de cualquier evidencia. Suspender todo el proceso, aunque cauteloso, deja sin apoyo a estudiantes que si lo necesitan mientras se resuelve el tema tecnico.",
    },
    "MI-COM-012": {
        "contexto": (
            "Debe decidir si un estudiante de su grado requiere apoyo academico adicional. Cuenta con "
            "tres fuentes de informacion que no coinciden del todo entre si: sus propias observaciones "
            "de aula, los registros de asistencia (con varias inasistencias no justificadas) y los "
            "resultados de la ultima evaluacion, que estuvieron dentro del promedio del grupo."
        ),
        "opcion_a": "Triangular las tres fuentes de evidencia, conversar directamente con el estudiante para entender el contexto de las inasistencias, y decidir con base en el conjunto de la informacion, no en una sola fuente.",
        "opcion_b": "Decidir con base unicamente en los resultados de la evaluacion, ya que es el dato mas objetivo y verificable de los tres disponibles.",
        "opcion_c": "Decidir con base unicamente en las inasistencias registradas, sin conversar con el estudiante ni revisar las demas fuentes de informacion.",
        "opcion_d": "Postergar la decision indefinidamente hasta contar con una cuarta fuente de informacion que confirme con certeza total el diagnostico.",
        "idoneidad": {"a": 4, "b": 2, "c": 1, "d": 1},
        "justificacion": "La decision mas solida integra distintas fuentes de evidencia y escucha al estudiante antes de concluir. Basarse solo en la evaluacion ignora señales de riesgo como la inasistencia. Basarse solo en la inasistencia sin dialogo puede llevar a conclusiones injustas. Postergar indefinidamente en busca de certeza total retrasa un apoyo que el estudiante podria necesitar ya.",
    },
    "MI-COM-013": {
        "contexto": (
            "Un directivo le pide una explicacion simple y rapida sobre por que bajaron los resultados "
            "del grado en el ultimo periodo, para presentarla en la reunion de padres de esta semana. Al "
            "revisar los datos, usted encuentra que las causas son multiples y estan entrelazadas: "
            "aumento de inasistencia, bajo desempeño especifico en comprension lectora, y dos cambios "
            "de docente titular durante el periodo."
        ),
        "opcion_a": "Presentar al directivo un resumen breve que reconozca las tres causas identificadas y su interrelacion, evitando reducir el problema a una sola explicacion simple pero incompleta.",
        "opcion_b": "Explicar unicamente el cambio de docentes como causa principal, porque es la mas facil de comunicar a los padres en la reunion.",
        "opcion_c": "Explicar unicamente el aumento de inasistencia como causa principal, porque es la variable que menos compromete la gestion institucional.",
        "opcion_d": "Negarse a dar una explicacion hasta poder hacer un estudio estadistico completo, dejando al directivo sin ninguna informacion para la reunion de esta semana.",
        "idoneidad": {"a": 4, "b": 2, "c": 1, "d": 1},
        "justificacion": "El manejo responsable de datos complejos no los reduce a una sola causa comoda, sino que comunica la interrelacion real de forma clara y breve. Elegir una sola causa -sea cual sea- simplifica indebidamente un fenomeno multicausal. Negarse a dar cualquier informacion, aunque busca rigor, deja al directivo sin insumos para una reunion que ya esta programada.",
    },
    "MI-COM-014": {
        "contexto": (
            "La madre de un estudiante de primaria solicita conocer los resultados comparativos de "
            "otros estudiantes del salon, para demostrar que su hijo fue evaluado de forma injusta "
            "frente al resto del grupo. Insiste en que tiene derecho a esa informacion porque se trata "
            "del rendimiento academico de su propio hijo."
        ),
        "opcion_a": "Explicar a la madre que puede acceder a la informacion completa de su hijo y a los criterios de evaluacion aplicados, pero que los resultados individuales de otros estudiantes son informacion protegida que no puede compartirse.",
        "opcion_b": "Compartir los resultados comparativos sin los nombres de los demas estudiantes, asumiendo que eso protege suficientemente su identidad en un grupo pequeño.",
        "opcion_c": "Entregar la lista completa de resultados del salon con nombres, considerando que la madre tiene derecho a verificar que la evaluacion de su hijo fue justa.",
        "opcion_d": "Negarse a dar cualquier informacion a la madre, incluyendo los criterios de evaluacion de su propio hijo, para evitar cualquier riesgo de reclamo posterior.",
        "idoneidad": {"a": 4, "b": 1, "c": 0, "d": 1},
        "justificacion": "La respuesta MENOS adecuada entrega datos identificables de otros estudiantes sin su consentimiento, vulnerando directamente su derecho a la reserva de informacion. Compartir resultados sin nombres sigue siendo riesgoso en un grupo pequeño donde la identificacion es facil. Negarse a dar cualquier informacion, incluida la que si le corresponde a la madre sobre su propio hijo, tampoco resuelve el reclamo legitimo que esta plantea.",
    },
    "MI-COM-015": {
        "contexto": (
            "Un rumor circula en redes sociales señalando a un estudiante como responsable de un daño "
            "a la infraestructura del colegio. Varios compañeros, influenciados por el rumor, exigen en "
            "el grupo de chat del curso que sea expulsado de inmediato. Usted no cuenta con ninguna "
            "evidencia formal que confirme quien causo el daño."
        ),
        "opcion_a": "Aclarar publicamente que no existe evidencia formal aun, activar el protocolo institucional de verificacion de hechos, y proteger al estudiante señalado de cualquier accion anticipada mientras se investiga.",
        "opcion_b": "Pedir a los estudiantes que dejen de comentar el tema en redes mientras se investiga, sin dar ninguna explicacion sobre el estado del caso.",
        "opcion_c": "Sancionar preventivamente al estudiante señalado por el rumor, para responder a la presion del grupo mientras se recolecta evidencia.",
        "opcion_d": "Ignorar el rumor por completo, sin activar ningun protocolo de verificacion ni proteger al estudiante de la presion social que esta recibiendo.",
        "idoneidad": {"a": 4, "b": 2, "c": 0, "d": 0},
        "justificacion": "La respuesta mas adecuada distingue explicitamente entre rumor y evidencia, protege al estudiante señalado y activa el canal formal de verificacion. Pedir silencio sin explicar el proceso reduce el ruido pero no protege activamente al estudiante. Sancionar sin evidencia bajo presion social es una vulneracion grave del debido proceso. Ignorar el rumor deja al estudiante expuesto a una presion social real sin ninguna intervencion institucional.",
    },
    "OL-COM-008": {
        "contexto": (
            "Los resultados del ultimo simulacro de grado once muestran una mejora notable en preguntas "
            "de memorizacion y datos puntuales, pero un desempeño bajo y estancado en preguntas que "
            "exigen lectura inferencial y uso de evidencia del texto. El simulacro final esta a ocho "
            "semanas y el plan de estudio actual no distingue entre ambos tipos de habilidad."
        ),
        "opcion_a": "Rediseñar el plan de las proximas semanas con metas especificas y medibles para fortalecer la lectura inferencial, manteniendo el repaso de memorizacion en un segundo plano.",
        "opcion_b": "Aumentar la cantidad total de simulacros practicados, sin diferenciar el tipo de habilidad que cada uno esta reforzando.",
        "opcion_c": "Mantener el plan de estudio actual sin cambios, confiando en que la mejora general seguira su curso hasta el simulacro final.",
        "opcion_d": "Concentrar todo el tiempo restante exclusivamente en ejercicios de memorizacion, ya que es donde el grupo ya muestra mejores resultados.",
        "idoneidad": {"a": 4, "b": 1, "c": 0, "d": 0},
        "justificacion": "La orientacion al logro exige ajustar el plan segun la evidencia especifica de donde esta el rezago real. Mantener el plan sin cambios ignora una señal clara de estancamiento. Reforzar solo lo que ya funciona bien desperdicia el tiempo restante en la habilidad que menos lo necesita. Aumentar la cantidad de simulacros sin diferenciar habilidades diluye el esfuerzo sin atacar la brecha identificada.",
    },
    "OL-COM-009": {
        "contexto": (
            "La institucion celebra una mejora leve en el promedio general de resultados del ultimo "
            "periodo. Sin embargo, al revisar el detalle por estudiante, usted nota que ese promedio "
            "esta impulsado por estudiantes que ya tenian buen desempeño, mientras que el grupo con "
            "mayor rezago -cerca de un cuarto del curso- no muestra ningun avance real."
        ),
        "opcion_a": "Presentar el analisis desagregado al equipo, mostrando que el avance no es parejo, y proponer un plan especifico de acompañamiento para el grupo que sigue rezagado.",
        "opcion_b": "Sumarse a la celebracion institucional del promedio general, sin mencionar el estancamiento del grupo con mayor rezago mientras se define una estrategia mas adelante.",
        "opcion_c": "Celebrar publicamente la mejora del promedio general como un logro completo del grupo, sin mencionar que una parte de los estudiantes no avanzo.",
        "opcion_d": "Cuestionar la validez de todos los resultados del periodo sin evidencia especifica, solo porque el promedio no refleja lo que usted observa en el aula.",
        "idoneidad": {"a": 4, "b": 1, "c": 0, "d": 1},
        "justificacion": "La respuesta MENOS adecuada es presentar como logro colectivo una mejora que en realidad oculta que un grupo de estudiantes no avanzo, lo cual retrasa cualquier intervencion real hacia ellos. Sumarse sin corregir el mensaje tambien posterga el problema, aunque sin agravarlo activamente. Cuestionar todos los resultados sin evidencia especifica no aporta una alternativa constructiva a la situacion.",
    },
    "OL-COM-010": {
        "contexto": (
            "El plan de mejoramiento de su area para este año enumera doce actividades distintas, pero "
            "ninguna tiene un indicador de exito definido ni una fecha de revision intermedia. Ya "
            "transcurrio la mitad del año escolar y nadie del equipo puede decir con certeza si el plan "
            "esta funcionando o no."
        ),
        "opcion_a": "Proponer al equipo definir dos o tres indicadores medibles para las actividades prioritarias del plan y establecer una fecha concreta de revision antes de que termine el año.",
        "opcion_b": "Continuar ejecutando las doce actividades tal como estan planteadas, confiando en que la cantidad de acciones por si sola producira mejora.",
        "opcion_c": "Reducir el plan a una sola actividad simbolica para simplificar el seguimiento, sin analizar cual de las doce era realmente prioritaria.",
        "opcion_d": "Esperar al cierre del año escolar para evaluar el plan completo de una sola vez, sin ningun punto de revision intermedio.",
        "idoneidad": {"a": 4, "b": 1, "c": 1, "d": 0},
        "justificacion": "Un plan de mejora solo es verificable si tiene indicadores y momentos de revision definidos con tiempo suficiente para ajustar el rumbo. Esperar al cierre del año para revisar todo de una vez elimina la posibilidad de corregir a tiempo. Continuar sin indicadores mantiene la misma falla de origen. Reducir el plan a una sola actividad sin analisis pierde de vista posibles prioridades reales entre las doce acciones.",
    },
    "OL-COM-011": {
        "contexto": (
            "En lenguaje, su grupo obtiene buenos resultados en preguntas de comprension literal -ubicar "
            "un dato explicito en el texto-, pero falla sistematicamente cuando debe justificar una "
            "respuesta usando evidencia del propio texto para sustentar una interpretacion. Este patron "
            "se repite en los ultimos tres simulacros."
        ),
        "opcion_a": "Diseñar ejercicios especificos donde los estudiantes deban argumentar sus respuestas citando evidencia textual, con retroalimentacion puntual sobre la calidad de esa argumentacion.",
        "opcion_b": "Aumentar la cantidad de textos leidos en clase, sin cambiar el tipo de pregunta que se les exige responder sobre ellos.",
        "opcion_c": "Concluir que el grupo ya domina lectura critica, porque los resultados generales en comprension literal son buenos.",
        "opcion_d": "Dejar de trabajar preguntas de justificacion con evidencia, ya que es el tipo de pregunta donde el grupo obtiene peores resultados.",
        "idoneidad": {"a": 4, "b": 1, "c": 0, "d": 0},
        "justificacion": "El desempeño transferible se construye entrenando especificamente la habilidad que falla, no evitandola ni asumiendo que un buen resultado parcial representa el dominio completo. Concluir que el grupo ya domina lectura critica ignora una señal clara y repetida de estancamiento. Evitar el tipo de pregunta donde el grupo falla renuncia directamente a cerrar la brecha. Leer mas sin cambiar la exigencia de la pregunta no ataca la habilidad especifica que esta fallando.",
    },
    "OL-COM-012": {
        "contexto": (
            "La presion institucional por subir los indicadores en la proxima prueba externa ha llevado "
            "al equipo docente a dedicar casi todo el tiempo de clase a resolver preguntas tipo prueba, "
            "dejando de lado la retroalimentacion formativa y el trabajo de comprension profunda que "
            "se venia haciendo antes."
        ),
        "opcion_a": "Proponer al equipo un balance entre practica tipo prueba y trabajo formativo, sustentando con evidencia que ambos son necesarios para un aprendizaje sostenible y no solo para el indicador inmediato.",
        "opcion_b": "Continuar entrenando exclusivamente preguntas tipo prueba durante el resto del periodo, priorizando el indicador inmediato sobre el proceso formativo.",
        "opcion_c": "Abandonar por completo la practica tipo prueba, ignorando que los estudiantes tambien necesitan familiarizarse con el formato de la evaluacion externa.",
        "opcion_d": "Dejar que cada docente decida por su cuenta si prioriza practica tipo prueba o trabajo formativo, sin ningun acuerdo de area.",
        "idoneidad": {"a": 4, "b": 0, "c": 1, "d": 1},
        "justificacion": "La respuesta MENOS adecuada sacrifica por completo el proceso formativo de fondo por perseguir unicamente el indicador inmediato, lo cual compromete el aprendizaje real del grupo a mediano plazo. Abandonar la practica tipo prueba tambien desatiende una necesidad legitima de los estudiantes, aunque en sentido opuesto. Dejar la decision fragmentada entre docentes, sin acuerdo de area, produce inconsistencia pero no compromete de forma tan directa el aprendizaje como entrenar solo para el examen.",
    },
    "OL-COM-013": {
        "contexto": (
            "Un estudiante de educacion media con alto potencial academico ha bajado notablemente su "
            "rendimiento este periodo. Al revisar sus trabajos, usted nota que las tareas asignadas no "
            "le exigen analisis ni produccion argumentativa propia, y el mismo le ha comentado que "
            "encuentra las actividades poco desafiantes."
        ),
        "opcion_a": "Diseñar para el estudiante retos diferenciados dentro de la misma planeacion de aula, que exijan mayor analisis y produccion argumentativa sin separarlo del resto del grupo.",
        "opcion_b": "Asignarle trabajo adicional de la misma naturaleza que las tareas actuales, solo que en mayor cantidad.",
        "opcion_c": "Concluir que la baja de rendimiento se debe a falta de compromiso personal del estudiante, sin revisar si las actividades son adecuadas para su nivel.",
        "opcion_d": "Recomendar que el estudiante avance de grado de forma anticipada como unica respuesta al problema, sin ajustar primero las actividades de su nivel actual.",
        "idoneidad": {"a": 4, "b": 1, "c": 0, "d": 1},
        "justificacion": "Retar academicamente a un estudiante con alto potencial dentro de su propio grupo suele ser mas sostenible que un cambio estructural inmediato. Concluir que el problema es solo actitudinal ignora una causa pedagogica evidente. Mas cantidad de la misma tarea no resuelve la falta de exigencia cualitativa. Proponer un adelanto de grado sin antes ajustar las actividades actuales es una respuesta desproporcionada frente a una solucion mas simple y disponible.",
    },
    "OL-COM-014": {
        "contexto": (
            "La institucion se ha fijado metas ambiciosas de mejora en matematicas para este año, pero "
            "al revisar la practica de aula usted nota que ningun docente del area consulta los "
            "resultados desagregados por grupo o por habilidad especifica antes de planear sus clases; "
            "todos usan la misma planeacion general del año anterior."
        ),
        "opcion_a": "Proponer al area revisar juntos los resultados por grupo y por habilidad antes de ajustar la planeacion, para que las metas institucionales se traduzcan en decisiones concretas de aula.",
        "opcion_b": "Ajustar unicamente su propia planeacion con base en los datos disponibles, sin proponerlo como practica del area completa.",
        "opcion_c": "Mantener la planeacion general del año anterior sin cambios, confiando en que fijar metas ambiciosas por si solo movilizara la mejora.",
        "opcion_d": "Solicitar a coordinacion que sea ella quien decida los ajustes de planeacion de todo el area, sin involucrar al equipo docente en el analisis de los datos.",
        "idoneidad": {"a": 4, "b": 2, "c": 0, "d": 1},
        "justificacion": "Las metas institucionales solo se cumplen si se traducen en decisiones pedagogicas concretas basadas en datos, y eso requiere que el equipo completo los revise. Mantener la planeacion sin cambios desconecta la meta institucional de la practica real de aula. Ajustar solo su propia planeacion mejora una parte pero no cierra la brecha del area completa. Delegar el analisis a coordinacion sin involucrar al equipo debilita la apropiacion de los datos por quienes enseñan directamente.",
    },
    "OL-COM-015": {
        "contexto": (
            "Una estrategia de lectura que funciono muy bien en un curso de grado sexto se replica "
            "exactamente igual, sin ningun ajuste, en todos los demas cursos de la institucion -desde "
            "primero hasta once-, sin considerar diferencias de edad, ritmo de aprendizaje ni "
            "prerrequisitos de cada grupo."
        ),
        "opcion_a": "Adaptar los elementos centrales de la estrategia exitosa al nivel y ritmo de cada grupo, conservando su logica pedagogica pero ajustando su complejidad segun el grado.",
        "opcion_b": "Aplicar la estrategia con pequeños ajustes de tiempo por grado, sin revisar a fondo si el nivel de complejidad tambien deberia cambiar.",
        "opcion_c": "Replicar la estrategia exactamente igual en todos los grados, confiando en que si funciono en un curso funcionara igual en cualquier otro.",
        "opcion_d": "Descartar por completo la estrategia para el resto de los grados, considerando que una practica exitosa en un solo curso no tiene ningun valor generalizable.",
        "idoneidad": {"a": 4, "b": 3, "c": 0, "d": 1},
        "justificacion": "La respuesta MENOS adecuada es replicar sin ningun ajuste una estrategia pensada para un grupo especifico, ignorando diferencias evidentes de edad y nivel entre grados. Descartarla por completo desperdicia una practica que si demostro funcionar, aunque en un contexto distinto. Ajustar solo el tiempo sin revisar la complejidad es un avance parcial que no resuelve del todo el problema de fondo.",
    },
    "TE-COM-008": {
        "contexto": (
            "En una institucion rural, dos areas deben diseñar juntas una secuencia interdisciplinar "
            "para el proximo periodo. En la primera reunion de planeacion, cada area defiende sus "
            "propios contenidos como prioritarios y se acusan mutuamente de no entender las "
            "necesidades reales del contexto de los estudiantes."
        ),
        "opcion_a": "Proponer identificar juntos un problema real del contexto que ambas areas puedan abordar desde sus contenidos, y construir la secuencia a partir de ese punto comun.",
        "opcion_b": "Sugerir que cada area diseñe su parte de la secuencia por separado y luego se unan los dos documentos sin una revision conjunta previa.",
        "opcion_c": "Insistir en que su propia area asuma el liderazgo total de la secuencia, dado que considera que su enfoque es mas pertinente para el contexto.",
        "opcion_d": "Suspender el intento de trabajo interdisciplinar y proponer que cada area continue trabajando de forma independiente, como se ha hecho en años anteriores.",
        "idoneidad": {"a": 4, "b": 2, "c": 0, "d": 1},
        "justificacion": "El trabajo en equipo efectivo parte de un punto en comun genuino, no de la imposicion de una sola perspectiva ni de la suma mecanica de partes separadas. Insistir en liderar unilateralmente perpetua el conflicto de fondo. Suspender el intento renuncia al valor pedagogico de la interdisciplinariedad. Diseñar por separado y unir despues evita el conflicto inmediato, pero no logra una integracion real entre las areas.",
    },
    "TE-COM-009": {
        "contexto": (
            "Un proyecto transversal en el que participan cuatro areas esta atrasado. Al revisar el "
            "avance, usted nota que los responsables de cada area no han compartido su progreso entre "
            "si, y cada uno esta usando criterios de calidad distintos para lo que se supone es un "
            "producto conjunto."
        ),
        "opcion_a": "Convocar una reunion breve con los responsables, diferenciar hechos de interpretaciones sobre el atraso, y acordar criterios comunes de calidad con un cronograma de seguimiento verificable.",
        "opcion_b": "Pedir apoyo a coordinacion para que medie en el atraso, documentando los hechos observados y las acciones ya intentadas por el equipo.",
        "opcion_c": "Asumir, sin verificar con los demas responsables, que el atraso se debe a la falta de compromiso de un area en particular, y comunicarlo asi al resto del equipo.",
        "opcion_d": "Absorber personalmente el trabajo pendiente de las otras areas para cumplir el plazo, sin abordar la falta de coordinacion de fondo.",
        "idoneidad": {"a": 4, "b": 3, "c": 0, "d": 1},
        "justificacion": "La respuesta MENOS adecuada es señalar responsabilidades sin verificar los hechos con las partes involucradas, lo cual puede ser injusto y deteriorar la confianza del equipo sin resolver el problema real de coordinacion. Absorber el trabajo ajeno evita el conflicto pero no corrige la falta de coordinacion que volvera a repetirse. Pedir mediacion de coordinacion es razonable, aunque implica un paso adicional frente a resolverlo directamente con el equipo.",
    },
    "TE-COM-010": {
        "contexto": (
            "Un colega del semillero academico que usted orienta ha presentado ante directivos los "
            "avances de un producto elaborado colectivamente por todo el equipo, atribuyendose el logro "
            "de forma individual y sin mencionar el trabajo de los demas docentes ni de los "
            "estudiantes involucrados."
        ),
        "opcion_a": "Conversar directamente con el colega sobre lo ocurrido, y en la siguiente presentacion ante directivos asegurarse de que se reconozca explicitamente el trabajo colectivo de todo el equipo.",
        "opcion_b": "Comentar el episodio con otros integrantes del equipo sin abordarlo directamente con el colega que se atribuyo el logro individual.",
        "opcion_c": "Reclamar publicamente ante los directivos en la misma reunion, señalando al colega frente a todos por haberse atribuido el trabajo del equipo.",
        "opcion_d": "No decir nada al respecto, asumiendo que discutir el reconocimiento del trabajo no vale el desgaste de un conflicto con el colega.",
        "idoneidad": {"a": 4, "b": 1, "c": 1, "d": 0},
        "justificacion": "Resolver el desacuerdo de forma directa y despues corregir el reconocimiento publico protege tanto la relacion de equipo como la justicia del credito colectivo. Callar por completo normaliza la apropiacion indebida del trabajo ajeno. Confrontar publicamente en el momento genera un conflicto innecesario frente a directivos que pudo resolverse en privado. Comentarlo solo entre colegas sin hablar con la persona involucrada no resuelve nada y puede generar mas tension indirecta.",
    },
    "TE-COM-011": {
        "contexto": (
            "El equipo de matematicas acordo una estrategia comun para enseñar resolucion de problemas "
            "este periodo. Sin embargo, al recorrer las aulas usted nota que cada docente la esta "
            "aplicando de forma distinta -algunos ni siquiera la estan usando-, y los estudiantes "
            "reciben instrucciones contradictorias segun el docente que les toque."
        ),
        "opcion_a": "Convocar al equipo para revisar juntos como se esta aplicando la estrategia en cada aula, identificar las diferencias y acordar ajustes concretos para lograr consistencia real.",
        "opcion_b": "Enviar un recordatorio escrito al equipo sobre el acuerdo original, sin abrir un espacio de conversacion sobre por que no se esta aplicando de forma uniforme.",
        "opcion_c": "Continuar aplicando la estrategia solo en su propia aula, sin intervenir en lo que hacen sus colegas del area.",
        "opcion_d": "Proponer abandonar la estrategia comun por completo, ya que su aplicacion desigual demuestra que el acuerdo no esta funcionando.",
        "idoneidad": {"a": 4, "b": 2, "c": 1, "d": 0},
        "justificacion": "La consistencia pedagogica que necesitan los estudiantes se logra revisando juntos las diferencias reales de aplicacion, no solo recordando el acuerdo por escrito. Aplicarla solo en su propia aula resuelve su caso individual pero no la inconsistencia del area. Abandonar la estrategia completa por su aplicacion desigual renuncia a un acuerdo que podria funcionar si se aplicara correctamente.",
    },
    "TE-COM-012": {
        "contexto": (
            "Faltan dos dias para la feria institucional y un area informa que no entregara sus "
            "evidencias porque considera que la planeacion inicial del evento fue deficiente y no "
            "reflejo sus necesidades. El resto de areas ya tiene su material listo y el evento no se "
            "puede posponer."
        ),
        "opcion_a": "Reunirse de inmediato con el area faltante para entender sus objeciones especificas, y definir juntos una entrega minima viable que si pueda estar lista a tiempo.",
        "opcion_b": "Pedir a coordinacion que intervenga para exigir la entrega del area faltante, sin explorar antes una solucion conjunta directamente con ellos.",
        "opcion_c": "Excluir al area faltante de la feria sin conversar con ellos, presentando el evento solo con las areas que si cumplieron a tiempo.",
        "opcion_d": "Aplazar la feria completa para todas las areas, aunque la mayoria ya tiene su material listo, solo por la situacion de una de ellas.",
        "idoneidad": {"a": 4, "b": 2, "c": 0, "d": 1},
        "justificacion": "La recuperacion colaborativa del proceso busca una solucion conjunta y minima viable antes de escalar el conflicto o excluir a nadie. Excluir al area sin dialogo desconoce sus objeciones y rompe la logica de trabajo en equipo. Aplazar todo el evento perjudica innecesariamente a las areas que si cumplieron. Escalar directamente a coordinacion sin intentar primero una solucion directa es un paso razonable pero no el mas eficiente dado el poco tiempo disponible.",
    },
    "TE-COM-013": {
        "contexto": (
            "En media tecnica, un conflicto entre docentes de mayor antigüedad y docentes nuevos ha "
            "paralizado la decision sobre los criterios de evaluacion comunes del area. Cada grupo "
            "defiende su propia perspectiva y ya han pasado tres reuniones sin llegar a ningun acuerdo, "
            "mientras el periodo de evaluacion se acerca."
        ),
        "opcion_a": "Facilitar un espacio donde ambos grupos presenten los fundamentos pedagogicos de su postura, identificar los puntos en comun y construir un criterio hibrido que integre lo valioso de cada perspectiva.",
        "opcion_b": "Proponer que se someta la decision a votacion simple entre todos los docentes del area, sin analizar antes los fundamentos de cada postura.",
        "opcion_c": "Alinearse abiertamente con el grupo de docentes de mayor antigüedad, considerando que su experiencia deberia tener mas peso en la decision.",
        "opcion_d": "Postergar la definicion de criterios comunes indefinidamente, dejando que cada docente aplique los suyos propios mientras se resuelve el conflicto.",
        "idoneidad": {"a": 4, "b": 2, "c": 0, "d": 1},
        "justificacion": "Mediar entre perspectivas construyendo un acuerdo basado en fundamentos pedagogicos es mas sostenible que imponer una postura o evadir la decision. Alinearse con un grupo por su antigüedad, sin analizar los argumentos, es una forma de imposicion disfrazada. Postergar indefinidamente deja a los estudiantes sin criterios claros justo antes de la evaluacion. Votar sin analizar los fundamentos puede resolver el impasse pero no necesariamente produce el mejor criterio pedagogico.",
    },
    "TE-COM-014": {
        "contexto": (
            "En una zona rural con aula multigrado, el equipo docente debe distribuir materiales "
            "didacticos escasos entre varias sedes. Cada sede prioriza cubrir sus propias urgencias "
            "inmediatas sin considerar el impacto en las demas, lo que ha dejado a una sede sin ningun "
            "material durante todo el mes."
        ),
        "opcion_a": "Proponer al equipo un criterio compartido de distribucion basado en necesidad real de cada sede, y hacer seguimiento para que ninguna quede sin material de forma prolongada.",
        "opcion_b": "Ceder los materiales de su propia sede a la sede mas necesitada este mes, sin proponer un criterio compartido que evite que la situacion se repita.",
        "opcion_c": "Priorizar unicamente las necesidades de su propia sede en la proxima distribucion, replicando la misma logica que genero el problema.",
        "opcion_d": "Solicitar a la institucion mas materiales sin proponer ningun cambio en el criterio actual de distribucion entre sedes.",
        "idoneidad": {"a": 4, "b": 2, "c": 0, "d": 1},
        "justificacion": "La equidad real en el uso de recursos requiere un criterio compartido y sostenido, no gestos aislados ni la misma logica individualista que causo el problema. Priorizar solo la propia sede repite exactamente el patron que dejo a otra sede sin material. Ceder los recursos este mes ayuda puntualmente pero no evita que la situacion se repita el proximo periodo. Pedir mas materiales sin cambiar el criterio de distribucion no resuelve la causa real del problema.",
    },
    "TE-COM-015": {
        "contexto": (
            "Un proyecto de lectura institucional depende de aportes coordinados de varias areas, pero "
            "solo el area de lenguaje ha cumplido con sus entregas hasta ahora. Al ver que las demas "
            "areas se han retrasado, la coordinadora de lenguaje empieza a tomar decisiones sobre el "
            "proyecto completo sin consultar a las otras areas involucradas."
        ),
        "opcion_a": "Reconocer el esfuerzo del area de lenguaje, y proponer un espacio conjunto para reactivar el compromiso de las demas areas sin que el proyecto quede bajo el control de una sola.",
        "opcion_b": "Apoyar en privado a la coordinadora de lenguaje para que siga tomando decisiones sola, dado que es la unica que ha cumplido con los plazos establecidos.",
        "opcion_c": "Permitir que el area de lenguaje asuma el control total del proyecto de forma permanente, ya que es la que demostro mayor compromiso con los plazos.",
        "opcion_d": "Cancelar el proyecto completo por el incumplimiento de la mayoria de las areas, sin intentar antes reactivar la participacion de quienes se atrasaron.",
        "idoneidad": {"a": 4, "b": 1, "c": 0, "d": 1},
        "justificacion": "La respuesta MENOS adecuada consolida el control de un proyecto colectivo en una sola area de forma permanente, lo cual rompe la corresponsabilidad que el proyecto necesita para sostenerse. Cancelarlo por completo desperdicia el trabajo ya realizado por quienes si cumplieron. Apoyar en privado que una sola area decida, aunque menos definitivo que hacerlo permanente, tambien deja sin corregir el desequilibrio de fondo.",
    },
}
