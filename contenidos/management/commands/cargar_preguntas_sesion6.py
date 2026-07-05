from django.core.management.base import BaseCommand
from contenidos.models import Sesion
from evaluaciones.models import Pregunta


class Command(BaseCommand):
    help = 'Carga 10 preguntas tipo CNSC para Sesion 6: Inclusion Educativa y Decreto 1421 de 2017'

    def handle(self, *args, **kwargs):
        try:
            sesion = Sesion.objects.get(numero=6)
        except Sesion.DoesNotExist:
            self.stdout.write(self.style.ERROR('Primero ejecuta: python manage.py cargar_sesiones'))
            return

        if Pregunta.objects.filter(sesion=sesion).exists():
            self.stdout.write(self.style.WARNING('Las preguntas de Sesion 6 ya existen. Omitiendo.'))
            return

        preguntas_data = [
            {
                'componente': 'normativo',
                'dificultad': 'media',
                'enunciado': 'El Decreto 1421 de 2017 reglamenta en Colombia:',
                'opcion_a': 'La evaluacion de desempeno de los docentes del Decreto 1278.',
                'opcion_b': 'La atencion educativa a la poblacion con discapacidad en el marco de la educacion inclusiva.',
                'opcion_c': 'El concurso de meritos para ingreso a la carrera docente.',
                'opcion_d': 'La convivencia escolar y las rutas de atencion integral.',
                'respuesta_correcta': 'B',
                'justificacion': 'El Decreto 1421 de 2017 reglamenta la prestacion del servicio educativo para la poblacion con discapacidad en el marco de la educacion inclusiva. Establece el PIAR, el DUA y las responsabilidades de docentes, directivos y secretarias de educacion.',
                'fuente_normativa': 'Decreto 1421 de 2017',
            },
            {
                'componente': 'normativo',
                'dificultad': 'alta',
                'enunciado': 'Segun el Decreto 1421 de 2017, el Plan Individual de Ajustes Razonables (PIAR) es:',
                'opcion_a': 'Un diagnostico medico que determina la discapacidad del estudiante.',
                'opcion_b': 'Una herramienta pedagogica que garantiza los procesos de ensenanza y aprendizaje de estudiantes con discapacidad, basada en la valoracion pedagogica y no en el diagnostico medico.',
                'opcion_c': 'Un documento que autoriza al estudiante con discapacidad a no cumplir con los requisitos academicos.',
                'opcion_d': 'El plan de tratamiento terapeutico que elabora el medico especialista.',
                'respuesta_correcta': 'B',
                'justificacion': 'El PIAR es una herramienta pedagogica (no medica) que define los ajustes razonables para garantizar el aprendizaje del estudiante con discapacidad. Se construye con la familia, el estudiante y el docente de aula, liderado por el docente, basado en valoracion pedagogica.',
                'fuente_normativa': 'Decreto 1421 de 2017 - Art. 2.3.3.5.2.3.5',
            },
            {
                'componente': 'normativo',
                'dificultad': 'media',
                'enunciado': 'El Diseno Universal para el Aprendizaje (DUA) en el marco del Decreto 1421 implica:',
                'opcion_a': 'Disenar adaptaciones especiales unicamente para estudiantes con discapacidad.',
                'opcion_b': 'Planear desde el inicio clases flexibles con multiples formas de representacion, accion y expresion que benefician a todos los estudiantes.',
                'opcion_c': 'Construir rampas y barreras fisicas en la infraestructura escolar.',
                'opcion_d': 'Separar a los estudiantes con discapacidad en grupos especiales.',
                'respuesta_correcta': 'B',
                'justificacion': 'El DUA es un enfoque de diseno curricular que parte de la diversidad como norma, no como excepcion. Propone tres principios: multiples formas de representacion (como se presenta la informacion), multiples formas de accion y expresion (como demuestran lo aprendido) y multiples formas de motivacion.',
                'fuente_normativa': 'Decreto 1421 de 2017 - DUA - CAST',
            },
            {
                'componente': 'normativo',
                'dificultad': 'alta',
                'enunciado': 'Segun el Decreto 1421 de 2017, quien lidera la construccion del PIAR?',
                'opcion_a': 'El medico especialista de la EPS del estudiante.',
                'opcion_b': 'El orientador escolar de forma exclusiva.',
                'opcion_c': 'El docente de aula en colaboracion con la familia, el estudiante y el docente de apoyo pedagogico.',
                'opcion_d': 'El rector de la IE sin participacion de los docentes de aula.',
                'respuesta_correcta': 'C',
                'justificacion': 'El Decreto 1421 Art. 2.3.3.5.2.3.5 establece que el PIAR es liderado por el docente de aula con la participacion activa de la familia y el estudiante. El docente de apoyo pedagogico acompana el proceso. Los directivos y orientadores participan segun la organizacion institucional.',
                'fuente_normativa': 'Decreto 1421 de 2017 - Art. 2.3.3.5.2.3.5',
            },
            {
                'componente': 'normativo',
                'dificultad': 'media',
                'enunciado': 'La educacion inclusiva en Colombia, segun el Decreto 1421 de 2017, se diferencia de la integracion educativa en que:',
                'opcion_a': 'La inclusion exige aulas especiales separadas para estudiantes con discapacidad.',
                'opcion_b': 'La integracion exige al estudiante adaptarse al sistema; la inclusion exige al sistema transformarse para atender la diversidad.',
                'opcion_c': 'La inclusion solo aplica para estudiantes con discapacidad fisica.',
                'opcion_d': 'La integracion es mas avanzada que la inclusion pedagogicamente.',
                'respuesta_correcta': 'B',
                'justificacion': 'La distincion fundamental es filosofica: la integracion pone la responsabilidad de adaptacion en el estudiante (que debe adaptarse al sistema existente). La inclusion reconoce que es el sistema el que debe transformarse para responder a la diversidad de todos los estudiantes.',
                'fuente_normativa': 'Decreto 1421 de 2017 - Educacion inclusiva',
            },
            {
                'componente': 'pedagogico',
                'dificultad': 'alta',
                'enunciado': 'Un docente recibe en su aula a un estudiante con discapacidad auditiva. Desde el enfoque del DUA, la primera accion pedagogica adecuada es:',
                'opcion_a': 'Solicitar que el estudiante sea trasladado a una institucion especializada.',
                'opcion_b': 'Redisenar su planeacion incorporando multiples formas de representacion visual y gestual que beneficien a todos los estudiantes.',
                'opcion_c': 'Asignar un companero para que le traduzca todo lo que el docente dice.',
                'opcion_d': 'Bajar el nivel de exigencia academica para ese estudiante.',
                'respuesta_correcta': 'B',
                'justificacion': 'El DUA propone que el docente diseñe clases accesibles desde el inicio para todos. Para un estudiante con discapacidad auditiva, esto implica recursos visuales, lenguaje de senas, subtitulos, organizadores graficos, etc. Estas estrategias benefician a todo el grupo.',
                'fuente_normativa': 'Decreto 1421 - DUA - Principio de representacion multiple',
            },
            {
                'componente': 'normativo',
                'dificultad': 'media',
                'enunciado': 'Los ajustes razonables en educacion, segun el Decreto 1421 de 2017, son:',
                'opcion_a': 'Modificaciones que implican una carga desproporcionada para la IE.',
                'opcion_b': 'Modificaciones y adaptaciones necesarias y adecuadas para garantizar el acceso y participacion del estudiante con discapacidad, sin imponer carga desproporcionada.',
                'opcion_c': 'Cambios en la infraestructura fisica de la IE para facilitar la movilidad.',
                'opcion_d': 'Reduccion de los contenidos academicos para los estudiantes con discapacidad.',
                'respuesta_correcta': 'B',
                'justificacion': 'Los ajustes razonables son las modificaciones necesarias para garantizar que el estudiante con discapacidad acceda, participe y aprenda en igualdad de condiciones. El criterio de razonabilidad implica que no deben imponer una carga desproporcionada o indebida sobre la IE.',
                'fuente_normativa': 'Decreto 1421 de 2017 - Ajustes razonables',
            },
            {
                'componente': 'pedagogico',
                'dificultad': 'alta',
                'enunciado': 'Un rector afirma que no puede matricular a un estudiante con discapacidad cognitiva porque la IE no tiene la infraestructura adecuada. Segun el Decreto 1421 de 2017, esta afirmacion es:',
                'opcion_a': 'Correcta, porque la IE puede negar el acceso si no tiene condiciones especiales.',
                'opcion_b': 'Incorrecta, porque el Decreto 1421 prohibe negar la matricula a estudiantes con discapacidad y obliga a todas las IE a garantizar su inclusion.',
                'opcion_c': 'Parcialmente correcta, si el rector demuestra ante la secretaria de educacion la falta de infraestructura.',
                'opcion_d': 'Correcta, porque solo las IE especializadas deben atender estudiantes con discapacidad.',
                'respuesta_correcta': 'B',
                'justificacion': 'El Decreto 1421 es enfatico: ninguna IE puede negar la matricula a un estudiante con discapacidad. La falta de condiciones no es justificacion para negar el acceso sino una obligacion que la IE debe gestionar con la secretaria de educacion para recibir apoyo.',
                'fuente_normativa': 'Decreto 1421 de 2017 - Prohibicion de negacion de matricula',
            },
            {
                'componente': 'normativo',
                'dificultad': 'media',
                'enunciado': 'El docente de apoyo pedagogico en el marco del Decreto 1421 cumple la funcion de:',
                'opcion_a': 'Reemplazar al docente de aula cuando hay estudiantes con discapacidad.',
                'opcion_b': 'Acompanar y orientar a los docentes de aula, familias e IE en la implementacion de estrategias de educacion inclusiva.',
                'opcion_c': 'Aplicar terapias especializadas a los estudiantes con discapacidad.',
                'opcion_d': 'Elaborar el PIAR de forma exclusiva sin participacion del docente de aula.',
                'respuesta_correcta': 'B',
                'justificacion': 'El docente de apoyo pedagogico no sustituye al docente de aula. Su rol es de acompanamiento, orientacion y formacion: apoya al docente de aula en el diseno de estrategias inclusivas, orienta a las familias y contribuye a la construccion del PIAR.',
                'fuente_normativa': 'Decreto 1421 de 2017 - Docente de apoyo pedagogico',
            },
            {
                'componente': 'pedagogico',
                'dificultad': 'alta',
                'enunciado': 'Desde el enfoque de educacion inclusiva del Decreto 1421, la evaluacion de los estudiantes con discapacidad debe:',
                'opcion_a': 'Ser igual a la del resto del grupo sin ningun tipo de ajuste.',
                'opcion_b': 'Incluir los ajustes razonables definidos en el PIAR, valorando el progreso individual del estudiante segun sus posibilidades.',
                'opcion_c': 'Eximir al estudiante de la evaluacion para no generarle estres.',
                'opcion_d': 'Ser realizada exclusivamente por el docente de apoyo pedagogico.',
                'respuesta_correcta': 'B',
                'justificacion': 'La evaluacion inclusiva aplica los ajustes razonables del PIAR (mas tiempo, diferentes formatos, uso de apoyos) y valora el progreso del estudiante en relacion con sus propias metas de aprendizaje definidas en el PIAR, no en comparacion con el grupo.',
                'fuente_normativa': 'Decreto 1421 de 2017 - PIAR - Evaluacion inclusiva',
            },
        ]

        self.stdout.write(self.style.WARNING('Cargando 10 preguntas de Sesion 6...'))
        creadas = 0
        for data in preguntas_data:
            data['sesion'] = sesion
            Pregunta.objects.create(**data)
            creadas += 1
            self.stdout.write(self.style.SUCCESS(f'  Pregunta {creadas} creada'))
        self.stdout.write(self.style.SUCCESS(f'\n{creadas} preguntas cargadas para Sesion 6'))
