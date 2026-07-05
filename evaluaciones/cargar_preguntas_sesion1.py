from django.core.management.base import BaseCommand
from contenidos.models import Sesion
from evaluaciones.models import Pregunta


class Command(BaseCommand):
    help = 'Carga 10 preguntas tipo CNSC para la Sesion 1: Modelos Pedagogicos'

    def handle(self, *args, **kwargs):
        try:
            sesion = Sesion.objects.get(numero=1)
        except Sesion.DoesNotExist:
            self.stdout.write(self.style.ERROR('Primero ejecuta: python manage.py cargar_sesiones'))
            return

        if Pregunta.objects.filter(sesion=sesion).exists():
            self.stdout.write(self.style.WARNING('Las preguntas de Sesion 1 ya existen. Omitiendo.'))
            return

        preguntas_data = [
            {
                'componente': 'pedagogico',
                'dificultad': 'media',
                'enunciado': 'Un docente organiza su clase de manera frontal, dicta contenidos, evalua mediante pruebas memoristicas y considera que el estudiante debe recibir pasivamente el conocimiento del maestro. A que modelo pedagogico corresponde esta practica?',
                'opcion_a': 'Modelo constructivista, porque el docente estructura el conocimiento.',
                'opcion_b': 'Modelo tradicional, porque el docente es el centro del proceso y el estudiante es receptor.',
                'opcion_c': 'Modelo critico, porque cuestiona la realidad social.',
                'opcion_d': 'Modelo por competencias, porque evalua resultados medibles.',
                'respuesta_correcta': 'B',
                'justificacion': 'El modelo tradicional se caracteriza por un docente protagonista que transmite conocimiento verbalmente, un estudiante pasivo que memoriza, evaluacion centrada en la repeticion de contenidos y una relacion jerarquica.',
                'fuente_normativa': 'Marco pedagogico - Florez Ochoa',
            },
            {
                'componente': 'pedagogico',
                'dificultad': 'media',
                'enunciado': 'Segun Lev Vygotsky, la Zona de Desarrollo Proximo (ZDP) se refiere a:',
                'opcion_a': 'El nivel maximo de conocimiento que un estudiante puede alcanzar por si solo.',
                'opcion_b': 'La distancia entre el nivel de desarrollo actual del estudiante y el nivel potencial que puede lograr con apoyo de un mediador.',
                'opcion_c': 'La etapa del desarrollo cognitivo en la que el nino adquiere el pensamiento logico-formal.',
                'opcion_d': 'El conjunto de saberes previos que el estudiante trae al aula.',
                'respuesta_correcta': 'B',
                'justificacion': 'La ZDP, concepto central del enfoque sociocultural de Vygotsky, representa el espacio donde el aprendizaje ocurre con mediacion de un otro mas capacitado. Es el puente entre lo que el estudiante puede hacer solo y lo que puede hacer con ayuda.',
                'fuente_normativa': 'Vygotsky - Enfoque Sociocultural',
            },
            {
                'componente': 'pedagogico',
                'dificultad': 'alta',
                'enunciado': 'Una docente de basica primaria plantea a sus estudiantes: Como podemos reducir los residuos solidos en nuestro colegio? Los estudiantes investigan, formulan hipotesis, disenan propuestas y las socializan. Este enfoque corresponde a:',
                'opcion_a': 'Modelo tradicional con proyecto de aula.',
                'opcion_b': 'Ensenanza directa con refuerzos positivos.',
                'opcion_c': 'Modelo constructivista con aprendizaje basado en problemas.',
                'opcion_d': 'Evaluacion sumativa de competencias ciudadanas.',
                'respuesta_correcta': 'C',
                'justificacion': 'El aprendizaje basado en problemas (ABP) es una estrategia propia del constructivismo. El estudiante construye conocimiento mediante investigacion, hipotesis y aplicacion en contextos reales. El docente es mediador, no transmisor.',
                'fuente_normativa': 'Constructivismo - Ausubel, Bruner',
            },
            {
                'componente': 'pedagogico',
                'dificultad': 'media',
                'enunciado': 'El modelo pedagogico por competencias se caracteriza principalmente por:',
                'opcion_a': 'Evaluar unicamente mediante pruebas escritas estandarizadas.',
                'opcion_b': 'Formar para la repeticion de contenidos disciplinares especificos.',
                'opcion_c': 'Integrar conocimientos, habilidades y actitudes para resolver problemas en contextos reales.',
                'opcion_d': 'Reducir el aprendizaje a la adquisicion de destrezas tecnicas.',
                'respuesta_correcta': 'C',
                'justificacion': 'La competencia se define como un saber hacer en contexto que integra conocimientos (saber), habilidades (saber hacer) y actitudes (saber ser). La evaluacion por competencias valora el desempeno en situaciones reales.',
                'fuente_normativa': 'MEN - Estandares Basicos de Competencias',
            },
            {
                'componente': 'pedagogico',
                'dificultad': 'alta',
                'enunciado': 'Paulo Freire, representante de la pedagogia critica, propone que la educacion debe:',
                'opcion_a': 'Transmitir neutralmente los contenidos oficiales establecidos por el Estado.',
                'opcion_b': 'Ser un acto politico que promueva la concientizacion y emancipacion de los oprimidos.',
                'opcion_c': 'Priorizar el desarrollo de competencias laborales para el mercado.',
                'opcion_d': 'Enfocarse exclusivamente en el desarrollo cognitivo individual.',
                'respuesta_correcta': 'B',
                'justificacion': 'Freire sostiene que toda educacion es politica. Su propuesta de pedagogia liberadora busca que los oprimidos tomen conciencia critica de su realidad y actuen para transformarla. Rechaza la educacion bancaria.',
                'fuente_normativa': 'Freire - Pedagogia del Oprimido',
            },
            {
                'componente': 'pedagogico',
                'dificultad': 'media',
                'enunciado': 'Jean Piaget identifica cuatro etapas del desarrollo cognitivo. El pensamiento logico-abstracto y la capacidad de razonar con hipotesis aparece en la etapa:',
                'opcion_a': 'Sensoriomotora (0-2 anos).',
                'opcion_b': 'Preoperacional (2-7 anos).',
                'opcion_c': 'Operaciones concretas (7-11 anos).',
                'opcion_d': 'Operaciones formales (11 anos en adelante).',
                'respuesta_correcta': 'D',
                'justificacion': 'En la etapa de operaciones formales, el adolescente desarrolla pensamiento abstracto, razonamiento hipotetico-deductivo y capacidad de analizar lo posible, no solo lo real. Es clave para didactica en secundaria y media.',
                'fuente_normativa': 'Piaget - Teoria del Desarrollo Cognitivo',
            },
            {
                'componente': 'pedagogico',
                'dificultad': 'alta',
                'enunciado': 'Un docente de matematicas parte de los conocimientos previos del estudiante, genera conflictos cognitivos con situaciones problematicas y promueve la construccion progresiva del concepto de funcion. Esta practica se fundamenta en:',
                'opcion_a': 'Aprendizaje por asociacion estimulo-respuesta.',
                'opcion_b': 'Aprendizaje significativo de David Ausubel.',
                'opcion_c': 'Condicionamiento operante de Skinner.',
                'opcion_d': 'Pedagogia instrumental-tecnicista.',
                'respuesta_correcta': 'B',
                'justificacion': 'Ausubel propone que el aprendizaje significativo ocurre cuando el nuevo conocimiento se relaciona sustancialmente con conceptos previos en la estructura cognitiva del estudiante.',
                'fuente_normativa': 'Ausubel - Aprendizaje Significativo',
            },
            {
                'componente': 'pedagogico',
                'dificultad': 'media',
                'enunciado': 'Cual de las siguientes afirmaciones describe mejor el rol del docente en el modelo constructivista?',
                'opcion_a': 'Transmisor de conocimientos disciplinares establecidos.',
                'opcion_b': 'Evaluador objetivo que mide logros mediante pruebas estandarizadas.',
                'opcion_c': 'Mediador que disena situaciones para que el estudiante construya el conocimiento.',
                'opcion_d': 'Autoridad que mantiene la disciplina y el orden en el aula.',
                'respuesta_correcta': 'C',
                'justificacion': 'En el constructivismo, el docente no entrega conocimiento hecho, sino que disena ambientes, preguntas y problemas que provocan la construccion activa del aprendizaje. Es mediador entre el saber y el estudiante.',
                'fuente_normativa': 'Constructivismo pedagogico',
            },
            {
                'componente': 'pedagogico',
                'dificultad': 'alta',
                'enunciado': 'La escuela tradicional ha sido criticada desde la pedagogia critica porque:',
                'opcion_a': 'Promueve demasiada participacion del estudiante en el aula.',
                'opcion_b': 'Reproduce relaciones de poder y desigualdades sociales mediante el curriculo oculto.',
                'opcion_c': 'Prioriza las competencias sobre los contenidos disciplinares.',
                'opcion_d': 'Fomenta la autonomia critica del estudiante.',
                'respuesta_correcta': 'B',
                'justificacion': 'Autores como Giroux, Apple y Freire sostienen que la escuela tradicional, a traves del curriculo oculto, reproduce las desigualdades sociales y las relaciones de poder de la sociedad dominante.',
                'fuente_normativa': 'Pedagogia Critica - Giroux, Apple',
            },
            {
                'componente': 'pedagogico',
                'dificultad': 'media',
                'enunciado': 'En Colombia, el enfoque por competencias se articula con los Derechos Basicos de Aprendizaje (DBA) porque:',
                'opcion_a': 'Los DBA son pruebas estandarizadas del ICFES.',
                'opcion_b': 'Los DBA establecen los aprendizajes estructurantes que los estudiantes deben alcanzar por grado, expresados como desempenos.',
                'opcion_c': 'Los DBA reemplazan a los Estandares Basicos de Competencias.',
                'opcion_d': 'Los DBA solo aplican para areas como matematicas y lenguaje.',
                'respuesta_correcta': 'B',
                'justificacion': 'Los DBA son un conjunto de aprendizajes estructurantes que el estudiante debe lograr en cada grado. Complementan los Estandares Basicos de Competencias y se expresan como desempenos observables.',
                'fuente_normativa': 'MEN - Derechos Basicos de Aprendizaje',
            },
        ]

        self.stdout.write(self.style.WARNING('Cargando 10 preguntas de Sesion 1: Modelos Pedagogicos...'))
        creadas = 0
        for data in preguntas_data:
            data['sesion'] = sesion
            Pregunta.objects.create(**data)
            creadas += 1
            self.stdout.write(self.style.SUCCESS(f'  Pregunta {creadas} creada'))

        self.stdout.write(self.style.SUCCESS(f'\n{creadas} preguntas cargadas para Sesion 1'))
