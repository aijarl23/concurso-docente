from django.core.management.base import BaseCommand
from contenidos.models import Sesion
from evaluaciones.models import Pregunta


class Command(BaseCommand):
    help = 'Carga 10 preguntas tipo CNSC para Sesión 2: Enfoques de Enseñanza-Aprendizaje'

    def handle(self, *args, **kwargs):
        try:
            sesion = Sesion.objects.get(numero=2)
        except Sesion.DoesNotExist:
            self.stdout.write(self.style.ERROR('❌ Primero ejecuta: python manage.py cargar_sesiones'))
            return

        preguntas_data = [
            {
                'componente': 'pedagogico',
                'dificultad': 'media',
                'enunciado': 'Un docente de básica secundaria diseña sus clases partiendo de que el estudiante aprende por asociación entre estímulos y respuestas, refuerza los comportamientos correctos con notas positivas e ignora los incorrectos. ¿Desde qué enfoque teórico fundamenta su práctica?',
                'opcion_a': 'Cognitivismo, porque se centra en los procesos mentales del estudiante.',
                'opcion_b': 'Constructivismo social, porque el aprendizaje ocurre en interacción con otros.',
                'opcion_c': 'Conductismo, porque el aprendizaje se explica por condicionamiento y refuerzos.',
                'opcion_d': 'Humanismo, porque prioriza el desarrollo integral de la persona.',
                'respuesta_correcta': 'C',
                'justificacion': 'El conductismo (Skinner, Pavlov, Watson) explica el aprendizaje como un cambio observable en la conducta producido por estímulo-respuesta y refuerzo. Las notas positivas como reforzadores y la repetición de conductas deseadas son características propias de este enfoque.',
                'fuente_normativa': 'Teoría conductista - Skinner, Pavlov',
            },
            {
                'componente': 'pedagogico',
                'dificultad': 'media',
                'enunciado': 'Según el enfoque cognitivista, ¿cuál es el principal objeto de estudio del aprendizaje?',
                'opcion_a': 'Los cambios observables en la conducta del estudiante ante estímulos externos.',
                'opcion_b': 'Los procesos internos del pensamiento: percepción, memoria, razonamiento y resolución de problemas.',
                'opcion_c': 'La influencia del entorno sociocultural en la construcción del conocimiento.',
                'opcion_d': 'La motivación intrínseca y el autoconcepto del estudiante.',
                'respuesta_correcta': 'B',
                'justificacion': 'El cognitivismo (Piaget, Ausubel, Bruner) se centra en los procesos mentales internos: cómo el individuo percibe, organiza, almacena y recupera información. A diferencia del conductismo, no se limita a lo observable sino que estudia la "caja negra" del pensamiento.',
                'fuente_normativa': 'Psicología cognitiva - Piaget, Ausubel, Bruner',
            },
            {
                'componente': 'pedagogico',
                'dificultad': 'alta',
                'enunciado': 'Una docente de preescolar organiza actividades donde los niños construyen torres con bloques, comentan cómo las hicieron y ayudan a compañeros que tienen dificultades. La docente acompaña sin dar respuestas directas. Este enfoque es coherente con:',
                'opcion_a': 'El conductismo, porque hay refuerzo positivo cuando los niños logran construir bien.',
                'opcion_b': 'El cognitivismo, porque los niños desarrollan esquemas mentales al manipular objetos.',
                'opcion_c': 'El socioconstructivismo de Vygotsky, porque el aprendizaje ocurre en interacción social con mediación.',
                'opcion_d': 'El humanismo, porque se respeta el ritmo natural de cada niño.',
                'respuesta_correcta': 'C',
                'justificacion': 'El socioconstructivismo vygotskiano plantea que el conocimiento se construye en interacción social. El rol mediador del docente, el trabajo colaborativo entre pares y la ZDP (Zona de Desarrollo Próximo) son sus elementos centrales, todos presentes en la situación descrita.',
                'fuente_normativa': 'Vygotsky - Socioconstructivismo',
            },
            {
                'componente': 'pedagogico',
                'dificultad': 'media',
                'enunciado': 'Abraham Maslow y Carl Rogers son representantes del enfoque humanista en educación. Su aporte fundamental a la pedagogía consiste en:',
                'opcion_a': 'Demostrar que el aprendizaje depende exclusivamente del nivel de desarrollo cognitivo.',
                'opcion_b': 'Proponer que la educación debe centrarse en el desarrollo integral de la persona, su motivación y autorrealización.',
                'opcion_c': 'Afirmar que el conocimiento se construye únicamente a través de la interacción con el entorno físico.',
                'opcion_d': 'Establecer que el docente debe controlar las condiciones ambientales para modificar la conducta del estudiante.',
                'respuesta_correcta': 'B',
                'justificacion': 'El humanismo educativo (Maslow, Rogers) propone una educación centrada en el estudiante como ser total, con énfasis en su motivación intrínseca, autoconcepto, dignidad y autorrealización. Rogers planteó el aprendizaje significativo como proceso personal de cambio.',
                'fuente_normativa': 'Humanismo pedagógico - Maslow, Rogers',
            },
            {
                'componente': 'pedagogico',
                'dificultad': 'alta',
                'enunciado': 'En el marco del enfoque por competencias del MEN colombiano, un docente evalúa si sus estudiantes pueden "usar los conocimientos sobre fracciones para resolver situaciones de la vida cotidiana". Esta evaluación valora principalmente:',
                'opcion_a': 'La memorización y reproducción de procedimientos matemáticos.',
                'opcion_b': 'La capacidad de saber hacer en contexto integrando conocimientos, habilidades y actitudes.',
                'opcion_c': 'El nivel de desarrollo cognitivo según las etapas de Piaget.',
                'opcion_d': 'La conducta observable del estudiante ante estímulos matemáticos específicos.',
                'respuesta_correcta': 'B',
                'justificacion': 'El enfoque por competencias del MEN define competencia como "saber hacer en contexto". Integra el saber (conocimiento conceptual), el saber hacer (procedimientos) y el saber ser (actitudes). Supera la memorización y evalúa la transferencia del conocimiento a situaciones reales.',
                'fuente_normativa': 'MEN - Estándares Básicos de Competencias - Decreto 1075 de 2015',
            },
            {
                'componente': 'pedagogico',
                'dificultad': 'media',
                'enunciado': 'La teoría del aprendizaje significativo de Ausubel plantea que para que un aprendizaje sea verdaderamente significativo se requiere:',
                'opcion_a': 'Que el estudiante memorice el contenido y lo repita correctamente.',
                'opcion_b': 'Que el nuevo conocimiento se relacione de manera sustancial con lo que el estudiante ya sabe.',
                'opcion_c': 'Que el docente use materiales audiovisuales novedosos durante la clase.',
                'opcion_d': 'Que la tarea sea lo suficientemente difícil para generar esfuerzo cognitivo.',
                'respuesta_correcta': 'B',
                'justificacion': 'Ausubel distingue el aprendizaje significativo del aprendizaje memorístico. Para que sea significativo se necesitan dos condiciones: material potencialmente significativo y disposición del estudiante para relacionarlo con sus conocimientos previos (estructura cognitiva preexistente).',
                'fuente_normativa': 'Ausubel - Teoría del Aprendizaje Significativo',
            },
            {
                'componente': 'pedagogico',
                'dificultad': 'alta',
                'enunciado': 'Desde la Guía 31 del MEN, la competencia pedagógica y didáctica del docente "se manifiesta cuando el docente fundamenta teóricamente sus prácticas pedagógicas y relaciona la teoría con la vida cotidiana". Esto corresponde principalmente al enfoque:',
                'opcion_a': 'Conductista, porque el docente aplica refuerzos positivos basados en teoría.',
                'opcion_b': 'Reflexivo-crítico, porque el docente articula teoría pedagógica con práctica contextualizada.',
                'opcion_c': 'Cognitivista puro, porque el docente desarrolla esquemas mentales en sus estudiantes.',
                'opcion_d': 'Humanista, porque el docente motiva intrínsecamente a sus estudiantes.',
                'respuesta_correcta': 'B',
                'justificacion': 'La Guía 31 del MEN describe la competencia pedagógica del docente del Decreto 1278 como la capacidad de fundamentar teóricamente su práctica y reflexionar sobre ella. Esto responde al enfoque reflexivo-crítico donde el docente es un intelectual que articula teoría y contexto real.',
                'fuente_normativa': 'Guía 31 - MEN - Evaluación de Desempeño Docente',
            },
            {
                'componente': 'pedagogico',
                'dificultad': 'media',
                'enunciado': '¿Cuál de las siguientes situaciones corresponde a un aprendizaje mediado desde el enfoque socioconstructivista en un aula colombiana de primaria?',
                'opcion_a': 'El docente explica en el tablero el proceso de división y los estudiantes practican ejercicios similares.',
                'opcion_b': 'Los estudiantes ven un video sobre multiplicación y responden un cuestionario individual.',
                'opcion_c': 'El docente forma parejas donde un estudiante con mayor dominio apoya a otro con dificultades para resolver problemas.',
                'opcion_d': 'El docente premia con estrellas a los estudiantes que terminan primero la tarea.',
                'respuesta_correcta': 'C',
                'justificacion': 'El aprendizaje entre pares es una estrategia central del socioconstructivismo. Vygotsky planteó que un "otro más competente" (puede ser un par) actúa como mediador en la ZDP, permitiendo que el estudiante alcance niveles que no lograría solo. Las opciones A y D corresponden a conductismo/enseñanza directa.',
                'fuente_normativa': 'Vygotsky - ZDP - Aprendizaje colaborativo',
            },
            {
                'componente': 'pedagogico',
                'dificultad': 'alta',
                'enunciado': 'Un docente del Decreto 1278 diseña su planeación de clase considerando el nivel de desarrollo cognitivo de sus estudiantes de grado tercero, parte de sus conocimientos previos, genera un conflicto cognitivo con una pregunta problematizadora y propone que construyan el concepto en equipos. ¿Qué enfoque teórico integra de manera coherente?',
                'opcion_a': 'Exclusivamente conductismo, porque hay un estímulo (pregunta) y una respuesta (concepto).',
                'opcion_b': 'Constructivismo integrado (Piaget + Vygotsky + Ausubel), articulando desarrollo, conocimientos previos e interacción.',
                'opcion_c': 'Humanismo puro, porque respeta el ritmo de aprendizaje de cada grupo.',
                'opcion_d': 'Cognitivismo piagetiano exclusivamente, porque considera etapas de desarrollo.',
                'respuesta_correcta': 'B',
                'justificacion': 'La planeación descrita integra: etapas de desarrollo (Piaget), conocimientos previos y conflicto cognitivo (Ausubel), y aprendizaje colaborativo en ZDP (Vygotsky). Esta es la perspectiva constructivista integrada, base del enfoque pedagógico que promueve el MEN en Colombia.',
                'fuente_normativa': 'Constructivismo integrado - MEN Colombia',
            },
            {
                'componente': 'pedagogico',
                'dificultad': 'media',
                'enunciado': 'El Decreto 1075 de 2015 establece que el programa de pedagogía para docentes debe incluir "la profundización de nuevas teorías, enfoques, modelos y metodologías en el campo de la educación". Esto implica que el docente colombiano debe:',
                'opcion_a': 'Aplicar un único modelo pedagógico en todas sus clases para mantener coherencia.',
                'opcion_b': 'Conocer y seleccionar críticamente enfoques pedagógicos según el contexto, los estudiantes y los objetivos de aprendizaje.',
                'opcion_c': 'Seguir exclusivamente el modelo tradicional que ha probado su efectividad históricamente.',
                'opcion_d': 'Adoptar el enfoque humanista como el único válido para el contexto colombiano.',
                'respuesta_correcta': 'B',
                'justificacion': 'El Decreto 1075 de 2015 (Art. 2.4.1.3.4) exige que el docente conozca diversas teorías y enfoques pedagógicos para aplicarlos según el contexto. La idoneidad docente implica selección crítica y fundamentada del enfoque más pertinente para cada situación de aprendizaje.',
                'fuente_normativa': 'Decreto 1075 de 2015 - Art. 2.4.1.3.4',
            },
        ]

        self.stdout.write(self.style.WARNING('Cargando 10 preguntas de Sesión 2: Enfoques de Enseñanza-Aprendizaje...'))
        creadas = 0
        for data in preguntas_data:
            data['sesion'] = sesion
            Pregunta.objects.create(**data)
            creadas += 1
            self.stdout.write(self.style.SUCCESS(f'  ✓ Pregunta {creadas} creada'))

        self.stdout.write(self.style.SUCCESS(f'\n✅ {creadas} preguntas cargadas para Sesión 2'))
        self.stdout.write(self.style.WARNING('\nSiguiente paso: crea el Simulacro 2 en el admin y agrega estas preguntas.'))
