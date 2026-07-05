from django.core.management.base import BaseCommand
from contenidos.models import Sesion
from evaluaciones.models import Pregunta


class Command(BaseCommand):
    help = 'Carga 10 preguntas tipo CNSC para Sesion 4: Evaluacion Educativa y Decreto 1290'

    def handle(self, *args, **kwargs):
        try:
            sesion = Sesion.objects.get(numero=4)
        except Sesion.DoesNotExist:
            self.stdout.write(self.style.ERROR('Primero ejecuta: python manage.py cargar_sesiones'))
            return

        if Pregunta.objects.filter(sesion=sesion).exists():
            self.stdout.write(self.style.WARNING('Las preguntas de Sesion 4 ya existen. Omitiendo.'))
            return

        preguntas_data = [
            {
                'componente': 'normativo',
                'dificultad': 'media',
                'enunciado': 'Segun el Decreto 1290 de 2009, la evaluacion del aprendizaje en Colombia es responsabilidad de:',
                'opcion_a': 'Exclusivamente el MEN, que define los criterios nacionales obligatorios.',
                'opcion_b': 'Los establecimientos educativos, que deben definir su propio Sistema Institucional de Evaluacion de Estudiantes (SIEE).',
                'opcion_c': 'El ICFES, que aplica pruebas estandarizadas en todos los grados.',
                'opcion_d': 'Los docentes de forma individual, sin necesidad de un sistema institucional.',
                'respuesta_correcta': 'B',
                'justificacion': 'El Decreto 1290 de 2009 otorga autonomia a cada IE para definir su SIEE. Es el cambio fundamental respecto al Decreto 230: el Estado fija criterios generales pero cada institucion define escalas, criterios de promocion y estrategias de recuperacion propias.',
                'fuente_normativa': 'Decreto 1290 de 2009 - Art. 1 y 4',
            },
            {
                'componente': 'pedagogico',
                'dificultad': 'media',
                'enunciado': 'La evaluacion diagnostica se realiza principalmente para:',
                'opcion_a': 'Asignar una calificacion al inicio del periodo academico.',
                'opcion_b': 'Identificar los conocimientos previos, intereses y dificultades de los estudiantes antes de iniciar un proceso de ensenanza.',
                'opcion_c': 'Determinar si el estudiante aprueba o reprueba el ano escolar.',
                'opcion_d': 'Comparar el desempeno de los estudiantes entre diferentes instituciones.',
                'respuesta_correcta': 'B',
                'justificacion': 'La evaluacion diagnostica cumple la funcion de identificar el punto de partida del estudiante: saberes previos, vacios conceptuales, estilos de aprendizaje e intereses. No tiene proposito calificatorio sino informativo para orientar la planeacion pedagogica.',
                'fuente_normativa': 'Decreto 1290 - Tipos de evaluacion - MEN',
            },
            {
                'componente': 'pedagogico',
                'dificultad': 'alta',
                'enunciado': 'Un docente aplica evaluaciones frecuentes durante la clase, retroalimenta los errores inmediatamente y ajusta su ensenanza segun los resultados. Este tipo de evaluacion se denomina:',
                'opcion_a': 'Evaluacion sumativa, porque acumula notas a lo largo del periodo.',
                'opcion_b': 'Evaluacion formativa, porque su proposito es mejorar el aprendizaje durante el proceso.',
                'opcion_c': 'Evaluacion diagnostica, porque identifica saberes previos.',
                'opcion_d': 'Evaluacion estandarizada, porque aplica los mismos criterios a todos.',
                'respuesta_correcta': 'B',
                'justificacion': 'La evaluacion formativa (Black y Wiliam) ocurre durante el proceso de aprendizaje, tiene proposito de mejora y retroalimentacion continua. Se distingue de la sumativa (que certifica al final) y de la diagnostica (que identifica el punto de partida).',
                'fuente_normativa': 'Decreto 1290 - Evaluacion formativa - Black y Wiliam',
            },
            {
                'componente': 'normativo',
                'dificultad': 'alta',
                'enunciado': 'El Decreto 1290 de 2009 establece que la promocion de los estudiantes es decision de:',
                'opcion_a': 'El MEN mediante criterios nacionales uniformes para todas las IE.',
                'opcion_b': 'El Consejo Academico de cada IE, segun los criterios del SIEE.',
                'opcion_c': 'El docente de forma autonoma sin consultar instancias institucionales.',
                'opcion_d': 'El ICFES segun los resultados de las pruebas Saber.',
                'respuesta_correcta': 'B',
                'justificacion': 'El Decreto 1290 Art. 6 establece que es el Consejo Academico quien define los criterios de promocion dentro del SIEE. Cada IE tiene autonomia para fijar el porcentaje de areas a reprobar, los criterios de promocion anticipada y las comisiones de evaluacion.',
                'fuente_normativa': 'Decreto 1290 de 2009 - Art. 6',
            },
            {
                'componente': 'pedagogico',
                'dificultad': 'media',
                'enunciado': 'Una rubrica de evaluacion es un instrumento que:',
                'opcion_a': 'Contiene una lista de los temas que el estudiante debe memorizar.',
                'opcion_b': 'Describe criterios de desempeno con niveles de calidad claramente definidos para valorar productos o procesos.',
                'opcion_c': 'Registra la asistencia y comportamiento del estudiante.',
                'opcion_d': 'Establece el horario de evaluaciones del periodo academico.',
                'respuesta_correcta': 'B',
                'justificacion': 'La rubrica es un instrumento de evaluacion que establece criterios explicitos y niveles de desempeno (ej: excelente, satisfactorio, en proceso, insuficiente). Favorece la evaluacion transparente, la autoevaluacion y la coevaluacion. Es coherente con el enfoque formativo del Decreto 1290.',
                'fuente_normativa': 'Decreto 1290 - Instrumentos de evaluacion',
            },
            {
                'componente': 'normativo',
                'dificultad': 'alta',
                'enunciado': 'Segun el Decreto 1290, los estudiantes tienen derecho a conocer los criterios de evaluacion. Esto implica que el docente debe:',
                'opcion_a': 'Sorprender a los estudiantes con evaluaciones sin previo aviso para medir el aprendizaje real.',
                'opcion_b': 'Dar a conocer al inicio del periodo los criterios, instrumentos y momentos de evaluacion del SIEE.',
                'opcion_c': 'Publicar las notas de todos los estudiantes en carteleras publicas.',
                'opcion_d': 'Aplicar unicamente pruebas escritas como instrumento de evaluacion.',
                'respuesta_correcta': 'B',
                'justificacion': 'El Decreto 1290 Art. 3 establece el derecho de los estudiantes a conocer el SIEE y los criterios de evaluacion. El docente tiene la obligacion de comunicar oportunamente los criterios, indicadores y momentos de evaluacion al inicio del proceso.',
                'fuente_normativa': 'Decreto 1290 de 2009 - Art. 3',
            },
            {
                'componente': 'pedagogico',
                'dificultad': 'media',
                'enunciado': 'La autoevaluacion en el proceso educativo colombiano es importante porque:',
                'opcion_a': 'Permite al estudiante asignarse la nota que considere merezca.',
                'opcion_b': 'Desarrolla la metacognicion y la autorregulacion del aprendizaje, siendo el estudiante critico de su propio proceso.',
                'opcion_c': 'Reduce la carga de trabajo del docente en el proceso evaluativo.',
                'opcion_d': 'Garantiza que todos los estudiantes obtengan buenas calificaciones.',
                'respuesta_correcta': 'B',
                'justificacion': 'La autoevaluacion no es un mecanismo para subir notas sino para desarrollar metacognicion: la capacidad del estudiante de reflexionar sobre su propio aprendizaje, identificar fortalezas y debilidades, y regular sus estrategias de estudio. El Decreto 1290 la incluye como modalidad evaluativa.',
                'fuente_normativa': 'Decreto 1290 - Autoevaluacion, coevaluacion, heteroevaluacion',
            },
            {
                'componente': 'pedagogico',
                'dificultad': 'alta',
                'enunciado': 'Un docente nota que el 70% de sus estudiantes reprobaron una evaluacion sobre el mismo concepto. Desde el enfoque formativo del Decreto 1290, la accion mas pertinente es:',
                'opcion_a': 'Aplicar la misma prueba nuevamente para que los estudiantes practiquen.',
                'opcion_b': 'Reflexionar sobre su practica, reensenar con estrategias diferentes y recoger nuevas evidencias antes de emitir valoracion definitiva.',
                'opcion_c': 'Promediar la nota con otras actividades para que el resultado no afecte tanto.',
                'opcion_d': 'Reportar a los padres de familia para que contraten tutores externos.',
                'respuesta_correcta': 'B',
                'justificacion': 'El Decreto 1290 fundamenta la evaluacion formativa: cuando los resultados son bajos de forma generalizada, la senal es que el proceso de ensenanza necesita ajustarse. El docente debe reflexionar sobre su practica, reensenar con estrategias diferentes y buscar nuevas evidencias.',
                'fuente_normativa': 'Decreto 1290 - Evaluacion formativa - Guia 31',
            },
            {
                'componente': 'normativo',
                'dificultad': 'media',
                'enunciado': 'Cual es la diferencia principal entre el Decreto 230 de 2002 (derogado) y el Decreto 1290 de 2009 en materia de promocion escolar?',
                'opcion_a': 'El Decreto 230 era mas exigente academicamente porque no permitia reprobar.',
                'opcion_b': 'El Decreto 230 obligaba a aprobar el 95% de estudiantes; el Decreto 1290 da autonomia a cada IE para definir sus propios criterios de promocion.',
                'opcion_c': 'El Decreto 1290 elimino la posibilidad de que los estudiantes reprobaran el ano.',
                'opcion_d': 'Ambos decretos son equivalentes, solo cambiaron en la escala de valoracion.',
                'respuesta_correcta': 'B',
                'justificacion': 'El Decreto 230 de 2002 obligaba a promover al menos el 95% de los estudiantes, lo que genero criticas por facilismo. El Decreto 1290 de 2009 lo derogo y devolvio la autonomia evaluativa a las IE, permitiendo que cada una defina sus criterios de promocion en el SIEE.',
                'fuente_normativa': 'Decreto 1290 de 2009 vs Decreto 230 de 2002',
            },
            {
                'componente': 'pedagogico',
                'dificultad': 'alta',
                'enunciado': 'Una lista de chequeo como instrumento de evaluacion se diferencia de una rubrica en que:',
                'opcion_a': 'La lista de chequeo es mas compleja y detallada que la rubrica.',
                'opcion_b': 'La lista de chequeo verifica la presencia o ausencia de criterios (si/no); la rubrica describe niveles de calidad para cada criterio.',
                'opcion_c': 'La rubrica se usa solo en educacion superior y la lista de chequeo en basica.',
                'opcion_d': 'Ambos instrumentos son identicos, solo difieren en el nombre.',
                'respuesta_correcta': 'B',
                'justificacion': 'La lista de chequeo es dicotomica: verifica si un elemento esta presente o ausente (si/no, cumple/no cumple). La rubrica va mas alla: describe niveles de calidad (excelente, satisfactorio, en proceso) para cada criterio, permitiendo una valoracion mas matizada del desempeno.',
                'fuente_normativa': 'Instrumentos de evaluacion - MEN - Decreto 1290',
            },
        ]

        self.stdout.write(self.style.WARNING('Cargando 10 preguntas de Sesion 4...'))
        creadas = 0
        for data in preguntas_data:
            data['sesion'] = sesion
            Pregunta.objects.create(**data)
            creadas += 1
            self.stdout.write(self.style.SUCCESS(f'  Pregunta {creadas} creada'))
        self.stdout.write(self.style.SUCCESS(f'\n{creadas} preguntas cargadas para Sesion 4'))
