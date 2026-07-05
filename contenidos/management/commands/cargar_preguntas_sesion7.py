from django.core.management.base import BaseCommand
from contenidos.models import Sesion
from evaluaciones.models import Pregunta


class Command(BaseCommand):
    help = 'Carga 10 preguntas tipo CNSC para Sesion 7: Convivencia Escolar y Ley 1620'

    def handle(self, *args, **kwargs):
        try:
            sesion = Sesion.objects.get(numero=7)
        except Sesion.DoesNotExist:
            self.stdout.write(self.style.ERROR('Primero ejecuta: python manage.py cargar_sesiones'))
            return

        if Pregunta.objects.filter(sesion=sesion).exists():
            self.stdout.write(self.style.WARNING('Las preguntas de Sesion 7 ya existen. Omitiendo.'))
            return

        preguntas_data = [
            {
                'componente': 'normativo',
                'dificultad': 'media',
                'enunciado': 'La Ley 1620 de 2013 crea en Colombia el Sistema Nacional de Convivencia Escolar con el objetivo principal de:',
                'opcion_a': 'Sancionar a los estudiantes que cometan faltas graves de convivencia.',
                'opcion_b': 'Promover y fortalecer la convivencia escolar, el ejercicio de los DDHH, la educacion para la sexualidad y la prevencion de la violencia escolar.',
                'opcion_c': 'Regular el uso del uniforme y las normas de presentacion personal en las IE.',
                'opcion_d': 'Establecer el regimen disciplinario de los docentes en las IE.',
                'respuesta_correcta': 'B',
                'justificacion': 'La Ley 1620 de 2013 crea el SNCE con un enfoque preventivo y formativo, no punitivo. Su proposito es promover la convivencia, los DDHH, la educacion para la sexualidad y la ciudadania, ademas de prevenir y mitigar la violencia escolar.',
                'fuente_normativa': 'Ley 1620 de 2013 - Art. 1',
            },
            {
                'componente': 'normativo',
                'dificultad': 'alta',
                'enunciado': 'Las tres rutas de atencion integral de la Ley 1620 de 2013 son:',
                'opcion_a': 'Prevencion, intervencion y sancion.',
                'opcion_b': 'Promocion, prevencion y atencion.',
                'opcion_c': 'Deteccion, reporte y seguimiento.',
                'opcion_d': 'Orientacion, mediacion y conciliacion.',
                'respuesta_correcta': 'B',
                'justificacion': 'Las tres rutas de atencion integral del SNCE son: 1) Promocion (fortalecer convivencia positiva), 2) Prevencion (identificar y mitigar riesgos antes de que ocurran) y 3) Atencion (responder cuando ya ocurrio la situacion). Esta estructura es clave en el concurso.',
                'fuente_normativa': 'Ley 1620 de 2013 - Tres rutas de atencion',
            },
            {
                'componente': 'normativo',
                'dificultad': 'media',
                'enunciado': 'Segun la Ley 1620 de 2013, el Comite de Convivencia Escolar de una IE debe estar conformado por:',
                'opcion_a': 'Solo directivos docentes y docentes orientadores.',
                'opcion_b': 'El rector, docentes, estudiantes, padres de familia y representante del sector productivo.',
                'opcion_c': 'El rector, el personero estudiantil y un representante de los docentes.',
                'opcion_d': 'Solo el rector y los coordinadores de convivencia.',
                'respuesta_correcta': 'B',
                'justificacion': 'La Ley 1620 establece que el Comite de Convivencia es un organo plural que incluye al rector, docentes, padres de familia, estudiantes y representante del sector productivo local. Esta composicion garantiza la participacion de toda la comunidad educativa.',
                'fuente_normativa': 'Ley 1620 de 2013 - Decreto 1965 - Comite de Convivencia',
            },
            {
                'componente': 'normativo',
                'dificultad': 'alta',
                'enunciado': 'La Ley 1620 clasifica las situaciones que afectan la convivencia escolar en tres tipos. Una situacion Tipo II corresponde a:',
                'opcion_a': 'Conflictos manejables entre estudiantes que no generan dano.',
                'opcion_b': 'Situaciones que causan dano al cuerpo o a la salud fisica o mental y que no constituyen delito.',
                'opcion_c': 'Delitos contra la libertad, integridad y formacion sexual.',
                'opcion_d': 'Faltas leves al manual de convivencia sin consecuencias graves.',
                'respuesta_correcta': 'B',
                'justificacion': 'La Ley 1620 clasifica en Tipo I (conflictos o incidentes sin dano intencional), Tipo II (situaciones con dano al cuerpo/salud sin delito, como acoso escolar o matoneo) y Tipo III (situaciones constitutivas de delito). Cada tipo tiene una ruta de atencion diferente.',
                'fuente_normativa': 'Ley 1620 de 2013 - Tipos de situaciones - Art. 40',
            },
            {
                'componente': 'pedagogico',
                'dificultad': 'media',
                'enunciado': 'El matoneo o bullying escolar se define como:',
                'opcion_a': 'Cualquier conflicto o pelea entre estudiantes dentro de la IE.',
                'opcion_b': 'Conducta negativa, intencional, repetida y sostenida en el tiempo que causa dano a quien la padece, con desequilibrio de poder entre agresor y victima.',
                'opcion_c': 'Una discusion verbal entre estudiantes que ocurre una sola vez.',
                'opcion_d': 'El incumplimiento de las normas del manual de convivencia.',
                'respuesta_correcta': 'B',
                'justificacion': 'El bullying (Olweus) tiene tres caracteristicas esenciales: intencionalidad (hay voluntad de causar dano), repeticion (ocurre de forma sistematica) y desequilibrio de poder (el agresor tiene mas poder que la victima). Un conflicto puntual sin repeticion no es bullying.',
                'fuente_normativa': 'Ley 1620 - Olweus - Definicion de matoneo',
            },
            {
                'componente': 'normativo',
                'dificultad': 'alta',
                'enunciado': 'Un estudiante reporta al docente que esta siendo victima de acoso escolar por parte de companeros. Segun la ruta de atencion de la Ley 1620, la accion inmediata del docente debe ser:',
                'opcion_a': 'Llamar a los padres del agresor para que resuelvan el problema en casa.',
                'opcion_b': 'Registrar el caso en el libro de convivencia, atender de forma inmediata al estudiante afectado, informar al coordinador y activar el protocolo del Comite de Convivencia.',
                'opcion_c': 'Hablar con el estudiante agresor para que pida disculpas.',
                'opcion_d': 'Esperar a que ocurra otra situacion antes de reportar formalmente.',
                'respuesta_correcta': 'B',
                'justificacion': 'La Ley 1620 establece una ruta clara: el docente debe atender inmediatamente al afectado, registrar el caso, informar al coordinador y activar el protocolo del Comite de Convivencia. No puede resolver el caso de forma individual ni esperar para reportar.',
                'fuente_normativa': 'Ley 1620 - Decreto 1965 - Ruta de atencion Tipo II',
            },
            {
                'componente': 'pedagogico',
                'dificultad': 'media',
                'enunciado': 'El manual de convivencia de una IE, segun la Ley 1620, debe ser:',
                'opcion_a': 'Elaborado exclusivamente por el rector y los coordinadores.',
                'opcion_b': 'Construido con participacion de toda la comunidad educativa y contener las pautas de convivencia, derechos y deberes de todos los miembros.',
                'opcion_c': 'Copiado del modelo que proporciona la secretaria de educacion.',
                'opcion_d': 'Actualizado cada cinco anos por decision del Consejo Directivo.',
                'respuesta_correcta': 'B',
                'justificacion': 'La Ley 1620 exige que el manual de convivencia sea construido participativamente con estudiantes, docentes, padres y directivos. Debe incluir las pautas de convivencia, derechos y responsabilidades, rutas de atencion y protocolos para cada tipo de situacion.',
                'fuente_normativa': 'Ley 1620 de 2013 - Manual de convivencia participativo',
            },
            {
                'componente': 'pedagogico',
                'dificultad': 'alta',
                'enunciado': 'Desde la Guia 49 del MEN, el estilo docente asertivo/democratico se caracteriza por:',
                'opcion_a': 'Alto nivel de estructura (normas claras) y bajo nivel de cuidado hacia los estudiantes.',
                'opcion_b': 'Bajo nivel de estructura y alto nivel de cuidado, siendo permisivo con el incumplimiento.',
                'opcion_c': 'Alto nivel de cuidado hacia los estudiantes Y alto nivel de estructura con normas construidas colectivamente.',
                'opcion_d': 'Bajo nivel de cuidado y bajo nivel de estructura, caracterizado por la negligencia.',
                'respuesta_correcta': 'C',
                'justificacion': 'La Guia 49 (Chaux) describe cuatro estilos: autoritario (alta estructura, bajo cuidado), permisivo (alto cuidado, baja estructura), negligente (bajos ambos) y asertivo/democratico (altos ambos). El estilo asertivo combina cuidado genuino CON normas claras construidas democraticamente.',
                'fuente_normativa': 'Guia 49 MEN - Estilos docentes - Chaux',
            },
            {
                'componente': 'normativo',
                'dificultad': 'media',
                'enunciado': 'El ciberacoso o ciberbullying esta contemplado en la Ley 1620 porque:',
                'opcion_a': 'Es un delito informatico que solo deben atender las autoridades policiales.',
                'opcion_b': 'Aunque ocurra fuera de la IE, afecta la convivencia escolar y debe ser atendido por la IE segun sus protocolos.',
                'opcion_c': 'Solo aplica cuando el acoso ocurre dentro de la IE usando dispositivos tecnologicos.',
                'opcion_d': 'Es competencia exclusiva de los padres de familia resolver esta situacion.',
                'respuesta_correcta': 'B',
                'justificacion': 'La Ley 1620 incluye el ciberacoso porque reconoce que el acoso a traves de medios digitales afecta la convivencia escolar aunque ocurra fuera del horario y las instalaciones de la IE. La escuela tiene responsabilidad de atenderlo segun sus protocolos.',
                'fuente_normativa': 'Ley 1620 de 2013 - Ciberacoso - Art. 2',
            },
            {
                'componente': 'pedagogico',
                'dificultad': 'alta',
                'enunciado': 'La mediacion escolar como estrategia de resolucion de conflictos se fundamenta en:',
                'opcion_a': 'La imposicion de una sancion por parte del directivo docente.',
                'opcion_b': 'La participacion voluntaria de las partes con un tercero neutral que facilita el dialogo y la busqueda de acuerdos mutuamente satisfactorios.',
                'opcion_c': 'La decision del docente sobre quien tiene la razon en el conflicto.',
                'opcion_d': 'La aplicacion del reglamento interno sin escuchar las versiones de los involucrados.',
                'respuesta_correcta': 'B',
                'justificacion': 'La mediacion es un proceso voluntario, confidencial y colaborativo donde un tercero neutral (mediador) facilita la comunicacion entre las partes para que encuentren una solucion consensuada. Desarrolla competencias ciudadanas y es coherente con el enfoque restaurativo de la Ley 1620.',
                'fuente_normativa': 'Ley 1620 - Mediacion escolar - Competencias ciudadanas',
            },
        ]

        self.stdout.write(self.style.WARNING('Cargando 10 preguntas de Sesion 7...'))
        creadas = 0
        for data in preguntas_data:
            data['sesion'] = sesion
            Pregunta.objects.create(**data)
            creadas += 1
            self.stdout.write(self.style.SUCCESS(f'  Pregunta {creadas} creada'))
        self.stdout.write(self.style.SUCCESS(f'\n{creadas} preguntas cargadas para Sesion 7'))
