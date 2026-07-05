from django.core.management.base import BaseCommand
from contenidos.models import Sesion
from evaluaciones.models import Pregunta


class Command(BaseCommand):
    help = 'Carga 10 preguntas tipo CNSC para Sesion 5: Planeacion de Clase y DBA'

    def handle(self, *args, **kwargs):
        try:
            sesion = Sesion.objects.get(numero=5)
        except Sesion.DoesNotExist:
            self.stdout.write(self.style.ERROR('Primero ejecuta: python manage.py cargar_sesiones'))
            return

        if Pregunta.objects.filter(sesion=sesion).exists():
            self.stdout.write(self.style.WARNING('Las preguntas de Sesion 5 ya existen. Omitiendo.'))
            return

        preguntas_data = [
            {
                'componente': 'pedagogico',
                'dificultad': 'media',
                'enunciado': 'Los Derechos Basicos de Aprendizaje (DBA) en Colombia se definen como:',
                'opcion_a': 'Pruebas estandarizadas que el MEN aplica al final de cada grado.',
                'opcion_b': 'Aprendizajes estructurantes que todo estudiante debe alcanzar en cada grado, expresados como enunciados de lo que el estudiante sabe y sabe hacer.',
                'opcion_c': 'Los contenidos minimos obligatorios que cada docente debe cubrir por periodo.',
                'opcion_d': 'Los derechos fundamentales de los estudiantes segun la Constitucion.',
                'respuesta_correcta': 'B',
                'justificacion': 'Los DBA son aprendizajes estructurantes por grado que el MEN define como referente para la planeacion. Cada DBA tiene tres componentes: el enunciado del aprendizaje, las evidencias de aprendizaje y los ejemplos de actividades. Complementan los Estandares Basicos de Competencias.',
                'fuente_normativa': 'MEN - Derechos Basicos de Aprendizaje',
            },
            {
                'componente': 'pedagogico',
                'dificultad': 'media',
                'enunciado': 'La diferencia entre los Estandares Basicos de Competencias (EBC) y los Derechos Basicos de Aprendizaje (DBA) es que:',
                'opcion_a': 'Los EBC aplican solo a matematicas y los DBA a todas las areas.',
                'opcion_b': 'Los EBC definen lo que el estudiante debe saber y saber hacer al finalizar un ciclo de grados; los DBA especifican aprendizajes concretos por cada grado.',
                'opcion_c': 'Los DBA reemplazaron definitivamente a los EBC desde 2016.',
                'opcion_d': 'Los EBC son nacionales y los DBA son definidos por cada IE.',
                'respuesta_correcta': 'B',
                'justificacion': 'Los EBC definen metas por grupos de grados (1-3, 4-5, 6-7, 8-9, 10-11) de forma amplia. Los DBA son mas especificos: definen aprendizajes grado a grado con evidencias observables. Son complementarios, no excluyentes.',
                'fuente_normativa': 'MEN - EBC y DBA - Decreto 1075 de 2015',
            },
            {
                'componente': 'pedagogico',
                'dificultad': 'alta',
                'enunciado': 'Una docente de lenguaje de grado 5 planea su clase partiendo del DBA: "Comprende textos literarios para propiciar el desarrollo de su capacidad creativa y lludica". Para operacionalizar este DBA, lo primero que debe hacer es:',
                'opcion_a': 'Seleccionar el libro de texto que usara durante el periodo.',
                'opcion_b': 'Identificar las evidencias de aprendizaje del DBA y disenarestategias que permitan verificarlas en el contexto de sus estudiantes.',
                'opcion_c': 'Aplicar una prueba escrita para medir la comprension lectora.',
                'opcion_d': 'Pedir a los estudiantes que lean el texto en casa como tarea.',
                'respuesta_correcta': 'B',
                'justificacion': 'Los DBA tienen evidencias de aprendizaje que orientan la planeacion. El docente debe identificar esas evidencias y disenar actividades que permitan verificarlas. Partir del DBA significa que el diseño de la clase va de la meta de aprendizaje hacia las actividades, no al reves.',
                'fuente_normativa': 'MEN - DBA - Orientaciones para la planeacion',
            },
            {
                'componente': 'pedagogico',
                'dificultad': 'media',
                'enunciado': 'En una planeacion de clase bien estructurada, los objetivos de aprendizaje deben ser:',
                'opcion_a': 'Amplios y generales para dar flexibilidad al docente.',
                'opcion_b': 'Especificos, medibles, alcanzables, relevantes y con limite de tiempo (criterios SMART).',
                'opcion_c': 'Definidos por el libro de texto, no por el docente.',
                'opcion_d': 'Iguales para todos los estudiantes sin importar su nivel de desarrollo.',
                'respuesta_correcta': 'B',
                'justificacion': 'Los objetivos de aprendizaje deben expresar claramente que sabra, entendera o podra hacer el estudiante al finalizar la clase. Los criterios SMART (especifico, medible, alcanzable, relevante, temporal) garantizan que sean operacionalizables y evaluables.',
                'fuente_normativa': 'Planeacion didactica - MEN - Guia 31',
            },
            {
                'componente': 'pedagogico',
                'dificultad': 'alta',
                'enunciado': 'El diseno curricular por competencias implica que la planeacion parte de:',
                'opcion_a': 'Los contenidos tematicos del libro de texto del grado.',
                'opcion_b': 'Las competencias y desempenos esperados, para luego definir actividades y evaluacion alineadas con esas metas.',
                'opcion_c': 'Las actividades ludicas disponibles en la IE.',
                'opcion_d': 'El tiempo disponible en el horario escolar.',
                'respuesta_correcta': 'B',
                'justificacion': 'El diseno curricular por competencias sigue la logica del backward design (diseno hacia atras): primero se define la competencia meta, luego la evidencia de que se logro (evaluacion) y finalmente las actividades de aprendizaje. Esto es lo opuesto a planear desde los contenidos.',
                'fuente_normativa': 'Wiggins y McTighe - Backward Design - MEN',
            },
            {
                'componente': 'normativo',
                'dificultad': 'media',
                'enunciado': 'Segun la Ley 115 de 1994, el curriculo escolar debe incluir obligatoriamente:',
                'opcion_a': 'Solo las areas fundamentales definidas por el MEN.',
                'opcion_b': 'Areas obligatorias y fundamentales, areas optativas y proyectos pedagogicos transversales.',
                'opcion_c': 'Unicamente los contenidos de las pruebas Saber.',
                'opcion_d': 'Los temas definidos por los docentes sin restriccion alguna.',
                'respuesta_correcta': 'B',
                'justificacion': 'La Ley 115 Art. 23 establece las areas obligatorias y fundamentales. El Art. 31 define las areas optativas. Ademas establece proyectos pedagogicos transversales (aprovechamiento del tiempo libre, educacion para la sexualidad, educacion ambiental, etc.).',
                'fuente_normativa': 'Ley 115 de 1994 - Art. 23 y 31',
            },
            {
                'componente': 'pedagogico',
                'dificultad': 'alta',
                'enunciado': 'La malla curricular de una IE es un instrumento de planeacion que articula:',
                'opcion_a': 'Solo los contenidos tematicos por periodo y grado.',
                'opcion_b': 'Competencias, DBA, contenidos, estrategias didacticas, recursos y criterios de evaluacion de forma articulada por grado y area.',
                'opcion_c': 'Exclusivamente el horario de clases y la distribucion de docentes.',
                'opcion_d': 'Los proyectos de aula de cada docente de forma independiente.',
                'respuesta_correcta': 'B',
                'justificacion': 'La malla curricular es la herramienta de planeacion macro que articula todos los elementos del proceso: competencias, DBA, estandares, contenidos, estrategias, recursos y evaluacion. Garantiza la coherencia vertical (entre grados) y horizontal (entre areas) del curriculo.',
                'fuente_normativa': 'MEN - Malla curricular - Decreto 1075 de 2015',
            },
            {
                'componente': 'pedagogico',
                'dificultad': 'media',
                'enunciado': 'Los proyectos pedagogicos transversales en la IE colombiana tienen como caracteristica principal:',
                'opcion_a': 'Reemplazar las areas fundamentales durante ciertos periodos del ano.',
                'opcion_b': 'Integrar diferentes areas del conocimiento en torno a tematicas que atraviesan todo el curriculo y responden a necesidades del contexto.',
                'opcion_c': 'Ser actividades extracurriculares opcionales sin calificacion.',
                'opcion_d': 'Ser implementados exclusivamente por el docente de ciencias sociales.',
                'respuesta_correcta': 'B',
                'justificacion': 'Los proyectos transversales (educacion sexual, educacion ambiental, uso del tiempo libre, etc.) se caracterizan por cruzar todas las areas del curriculo, integrando saberes diversos en torno a problematicas del contexto. Son obligatorios segun la Ley 115.',
                'fuente_normativa': 'Ley 115 de 1994 - Proyectos transversales',
            },
            {
                'componente': 'pedagogico',
                'dificultad': 'alta',
                'enunciado': 'Cuando un docente del Decreto 1278 realiza su planeacion de aula, segun la Guia 31 del MEN, debe evidenciar:',
                'opcion_a': 'Unicamente los contenidos tematicos del periodo.',
                'opcion_b': 'Las metas de aprendizaje, los contenidos, las estrategias pedagogicas seleccionadas y los procedimientos de evaluacion.',
                'opcion_c': 'El registro de asistencia y la distribucion del tiempo de clase.',
                'opcion_d': 'El libro de texto que usara y las actividades del cuaderno.',
                'respuesta_correcta': 'B',
                'justificacion': 'La Guia 31 (Modelo de pauta de observacion de clase - Anexo 4) establece que la planeacion del docente debe incluir: metas de aprendizaje, contenidos, estrategias pedagogicas seleccionadas segun el grupo y procedimientos de evaluacion. Esto es lo que el evaluador verifica.',
                'fuente_normativa': 'Guia 31 MEN - Anexo 4 - Pauta de observacion de clase',
            },
            {
                'componente': 'normativo',
                'dificultad': 'media',
                'enunciado': 'Segun el Decreto 1075 de 2015, el Proyecto Educativo Institucional (PEI) debe incluir la propuesta curricular que responde a la pregunta:',
                'opcion_a': 'Cuantos docentes necesita la IE para funcionar.',
                'opcion_b': 'Como se ensenara, que se ensenara, cuando se ensenara y como se evaluara en la IE.',
                'opcion_c': 'Cual es el presupuesto anual de la institucion educativa.',
                'opcion_d': 'Quienes son los directivos docentes y sus funciones administrativas.',
                'respuesta_correcta': 'B',
                'justificacion': 'El componente curricular del PEI responde a las preguntas fundamentales del curriculo: que ensenar (contenidos y competencias), como ensenar (estrategias didacticas), cuando ensenar (secuenciacion) y como evaluar (SIEE). Es la guia pedagogica de la IE.',
                'fuente_normativa': 'Decreto 1075 de 2015 - PEI - Ley 115 Art. 73',
            },
        ]

        self.stdout.write(self.style.WARNING('Cargando 10 preguntas de Sesion 5...'))
        creadas = 0
        for data in preguntas_data:
            data['sesion'] = sesion
            Pregunta.objects.create(**data)
            creadas += 1
            self.stdout.write(self.style.SUCCESS(f'  Pregunta {creadas} creada'))
        self.stdout.write(self.style.SUCCESS(f'\n{creadas} preguntas cargadas para Sesion 5'))
