from django.core.management.base import BaseCommand
from contenidos.models import Sesion
from evaluaciones.models import Pregunta


class Command(BaseCommand):
    help = 'Carga 10 preguntas tipo CNSC para Sesion 3: Estrategias Didacticas Activas'

    def handle(self, *args, **kwargs):
        try:
            sesion = Sesion.objects.get(numero=3)
        except Sesion.DoesNotExist:
            self.stdout.write(self.style.ERROR('Primero ejecuta: python manage.py cargar_sesiones'))
            return

        if Pregunta.objects.filter(sesion=sesion).exists():
            self.stdout.write(self.style.WARNING('Las preguntas de Sesion 3 ya existen. Omitiendo.'))
            return

        preguntas_data = [
            {
                'componente': 'pedagogico',
                'dificultad': 'media',
                'enunciado': 'Un docente divide su clase en grupos, plantea un problema real del entorno escolar y pide a los estudiantes que investiguen, propongan soluciones y las presenten. Esta estrategia corresponde a:',
                'opcion_a': 'Aprendizaje memoristico, porque los estudiantes repiten informacion.',
                'opcion_b': 'Aprendizaje Basado en Problemas (ABP), porque parte de una situacion real que demanda investigacion y solucion.',
                'opcion_c': 'Ensenanza directa, porque el docente controla el proceso.',
                'opcion_d': 'Evaluacion sumativa, porque los estudiantes presentan resultados.',
                'respuesta_correcta': 'B',
                'justificacion': 'El ABP es una estrategia didactica activa donde el estudiante aprende a traves de la resolucion de problemas reales o simulados. El docente es facilitador y el estudiante protagonista. Es coherente con el constructivismo y el enfoque por competencias del MEN.',
                'fuente_normativa': 'ABP - Barrows - MEN Colombia',
            },
            {
                'componente': 'pedagogico',
                'dificultad': 'media',
                'enunciado': 'En el modelo de aula invertida (flipped classroom), el rol del tiempo en clase cambia porque:',
                'opcion_a': 'El docente explica la teoria en casa y los estudiantes practican en clase.',
                'opcion_b': 'Los estudiantes estudian los contenidos teoricos en casa (videos, lecturas) y el tiempo de clase se usa para resolver dudas, aplicar y profundizar.',
                'opcion_c': 'Los estudiantes hacen las tareas en clase y el docente las revisa en casa.',
                'opcion_d': 'El docente elimina la teoria y solo trabaja actividades practicas en el aula.',
                'respuesta_correcta': 'B',
                'justificacion': 'El aula invertida invierte el uso tradicional del tiempo: la transmision de informacion ocurre fuera del aula (videos, podcasts, lecturas) y el tiempo presencial se dedica a actividades de mayor nivel cognitivo: aplicacion, analisis, creacion y debate.',
                'fuente_normativa': 'Bergmann y Sams - Flipped Classroom',
            },
            {
                'componente': 'pedagogico',
                'dificultad': 'alta',
                'enunciado': 'Una docente organiza su clase en grupos heterogeneos donde cada estudiante tiene un rol especifico (lider, secretario, relator, controlador de tiempo) y todos son responsables del aprendizaje colectivo. Esta estrategia se denomina:',
                'opcion_a': 'Trabajo en grupo tradicional, porque los estudiantes trabajan juntos.',
                'opcion_b': 'Aprendizaje cooperativo, porque hay interdependencia positiva, responsabilidad individual y roles definidos.',
                'opcion_c': 'Aprendizaje por proyectos, porque tienen un objetivo comun.',
                'opcion_d': 'Ensenanza entre pares, porque los estudiantes se explican entre si.',
                'respuesta_correcta': 'B',
                'justificacion': 'El aprendizaje cooperativo (Johnson & Johnson) se distingue del trabajo en grupo por cinco elementos: interdependencia positiva, responsabilidad individual, interaccion cara a cara, habilidades sociales y procesamiento grupal. Los roles definidos son caracteristica esencial.',
                'fuente_normativa': 'Johnson y Johnson - Aprendizaje Cooperativo',
            },
            {
                'componente': 'pedagogico',
                'dificultad': 'media',
                'enunciado': 'La diferencia fundamental entre el Aprendizaje Basado en Proyectos (ABPr) y el Aprendizaje Basado en Problemas (ABP) radica en:',
                'opcion_a': 'El ABPr usa tecnologia y el ABP no.',
                'opcion_b': 'El ABP parte de un problema abierto para construir conocimiento; el ABPr culmina en un producto o artefacto concreto que da respuesta a una necesidad real.',
                'opcion_c': 'El ABP es para primaria y el ABPr para secundaria.',
                'opcion_d': 'El ABPr es individual y el ABP es grupal.',
                'respuesta_correcta': 'B',
                'justificacion': 'Aunque ambos son estrategias activas, el ABP se centra en resolver un problema como motor de aprendizaje, mientras que el ABPr tiene como meta la creacion de un producto final tangible (maqueta, video, campana, app) que responde a una necesidad del contexto.',
                'fuente_normativa': 'Buck Institute for Education - PBL',
            },
            {
                'componente': 'pedagogico',
                'dificultad': 'alta',
                'enunciado': 'Desde la Guia 31 del MEN, la competencia pedagogica y didactica del docente implica "usar diferentes escenarios y ambientes para potenciar los procesos de ensenanza-aprendizaje". Esto es coherente con:',
                'opcion_a': 'La ensenanza exclusivamente dentro del aula con tablero y libro de texto.',
                'opcion_b': 'El uso de estrategias didacticas activas que diversifican espacios y metodologias segun las necesidades del grupo.',
                'opcion_c': 'La evaluacion permanente mediante pruebas escritas estandarizadas.',
                'opcion_d': 'El uso exclusivo de tecnologia digital en todas las clases.',
                'respuesta_correcta': 'B',
                'justificacion': 'La Guia 31 establece que la competencia pedagogica del docente 1278 se manifiesta en el uso de variadas estrategias y escenarios. Esto implica salir del modelo transmisionista y usar estrategias activas, ambientes diversos y metodologias adaptadas al contexto.',
                'fuente_normativa': 'Guia 31 MEN - Competencia pedagogica y didactica',
            },
            {
                'componente': 'pedagogico',
                'dificultad': 'media',
                'enunciado': 'La gamificacion en el aula consiste en:',
                'opcion_a': 'Reemplazar todas las clases por videojuegos educativos.',
                'opcion_b': 'Aplicar elementos y mecanicas de juego (puntos, niveles, retos, insignias) en contextos de aprendizaje para aumentar la motivacion y el compromiso.',
                'opcion_c': 'Llevar juegos de mesa al aula como actividad de descanso.',
                'opcion_d': 'Evaluar a los estudiantes mediante competencias deportivas.',
                'respuesta_correcta': 'B',
                'justificacion': 'La gamificacion no es jugar en clase sino aplicar la logica del juego al aprendizaje: sistemas de puntos, niveles de progreso, retos, recompensas e insignias que aumentan la motivacion intrinseca. Se diferencia del juego educativo en que el contenido no cambia, cambia la experiencia.',
                'fuente_normativa': 'Kapp - Gamificacion del aprendizaje',
            },
            {
                'componente': 'pedagogico',
                'dificultad': 'alta',
                'enunciado': 'Un docente de ciencias sociales en una IE de Medellin usa el metodo de estudio de caso: presenta una situacion real sobre conflicto urbano, los estudiantes la analizan desde multiples perspectivas y proponen alternativas. Segun el enfoque por competencias del MEN, esta estrategia favorece principalmente:',
                'opcion_a': 'La memorizacion de datos historicos sobre conflictos colombianos.',
                'opcion_b': 'El desarrollo de competencias ciudadanas y pensamiento critico al aplicar conocimientos a situaciones reales del contexto.',
                'opcion_c': 'La evaluacion sumativa de contenidos del area.',
                'opcion_d': 'El aprendizaje de procedimientos administrativos institucionales.',
                'respuesta_correcta': 'B',
                'justificacion': 'El estudio de caso desarrolla pensamiento critico, analisis de perspectivas multiples y toma de decisiones contextualizadas. Es coherente con el enfoque por competencias del MEN que busca el saber hacer en contexto, especialmente en competencias ciudadanas.',
                'fuente_normativa': 'MEN - Competencias ciudadanas - Estandares Basicos',
            },
            {
                'componente': 'pedagogico',
                'dificultad': 'media',
                'enunciado': 'El pensamiento de diseno (Design Thinking) como estrategia didactica en el aula se caracteriza por:',
                'opcion_a': 'Ensenara los estudiantes a dibujar y disenar graficamente.',
                'opcion_b': 'Un proceso centrado en el ser humano que sigue fases de empatia, definicion, ideacion, prototipado y prueba para resolver problemas creativamente.',
                'opcion_c': 'Evaluar el pensamiento logico-matematico de los estudiantes.',
                'opcion_d': 'Una metodologia exclusiva para clases de tecnologia e informatica.',
                'respuesta_correcta': 'B',
                'justificacion': 'El Design Thinking (IDEO, Stanford d.school) es una metodologia de innovacion centrada en las personas. Sus cinco fases (empatizar, definir, idear, prototipar, testear) desarrollan pensamiento creativo, trabajo colaborativo y solucion de problemas reales.',
                'fuente_normativa': 'Design Thinking - IDEO - Stanford d.school',
            },
            {
                'componente': 'pedagogico',
                'dificultad': 'alta',
                'enunciado': 'En el marco del Decreto 1278 de 2002, un docente que usa estrategias didacticas activas variadas y las ajusta segun las caracteristicas de sus estudiantes esta demostrando:',
                'opcion_a': 'Competencia comportamental de liderazgo.',
                'opcion_b': 'Competencia funcional pedagogica y didactica en su area de gestion academica.',
                'opcion_c': 'Competencia administrativa de uso de recursos institucionales.',
                'opcion_d': 'Competencia comunitaria de comunicacion institucional.',
                'respuesta_correcta': 'B',
                'justificacion': 'Segun el Decreto 1278 y la Guia 31, la competencia funcional "pedagogica y didactica" incluye usar variadas estrategias de ensenanza y ajustarlas segun las caracteristicas y ritmos de aprendizaje de los estudiantes. Es parte del area de gestion academica.',
                'fuente_normativa': 'Decreto 1278 de 2002 - Guia 31 MEN',
            },
            {
                'componente': 'pedagogico',
                'dificultad': 'media',
                'enunciado': 'La tecnica del rompecabezas (Jigsaw) de Aronson es una estrategia de aprendizaje cooperativo donde:',
                'opcion_a': 'Los estudiantes arman rompecabezas fisicos como actividad ludica.',
                'opcion_b': 'Cada estudiante aprende una parte del contenido y luego la ensena a sus companeors, siendo experto en esa parte y aprendiendo de los demas.',
                'opcion_c': 'El docente divide el tablero en secciones y asigna una a cada grupo.',
                'opcion_d': 'Los estudiantes compiten para ver quien aprende mas rapidamente.',
                'respuesta_correcta': 'B',
                'justificacion': 'La tecnica Jigsaw divide el contenido en partes. Cada estudiante se convierte en experto de una parte en un grupo de expertos, luego regresa a su grupo original y ensena lo que aprendio. Desarrolla interdependencia positiva y responsabilidad individual.',
                'fuente_normativa': 'Aronson - Tecnica Jigsaw - Aprendizaje Cooperativo',
            },
        ]

        self.stdout.write(self.style.WARNING('Cargando 10 preguntas de Sesion 3...'))
        creadas = 0
        for data in preguntas_data:
            data['sesion'] = sesion
            Pregunta.objects.create(**data)
            creadas += 1
            self.stdout.write(self.style.SUCCESS(f'  Pregunta {creadas} creada'))
        self.stdout.write(self.style.SUCCESS(f'\n{creadas} preguntas cargadas para Sesion 3'))
