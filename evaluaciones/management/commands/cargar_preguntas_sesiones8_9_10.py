from django.core.management.base import BaseCommand
from contenidos.models import Sesion
from evaluaciones.models import Pregunta


class Command(BaseCommand):
    help = 'Carga preguntas para Sesiones 8, 9 y 10 (Ley 115, PEI-TIC, Decreto 1278)'

    def handle(self, *args, **kwargs):

        # ── SESION 8: Ley 115 ──
        s8_data = [
            {'componente': 'normativo', 'dificultad': 'media',
             'enunciado': 'Segun la Ley 115 de 1994, la educacion en Colombia es definida como:',
             'opcion_a': 'Un servicio publico que tiene una funcion social acorde con las necesidades e intereses de las personas, la familia y la sociedad.',
             'opcion_b': 'Un derecho exclusivo de los ciudadanos colombianos mayores de edad.',
             'opcion_c': 'Una actividad privada regulada por el Estado solamente en casos especiales.',
             'opcion_d': 'Un proceso academico orientado exclusivamente al mercado laboral.',
             'respuesta_correcta': 'A',
             'justificacion': 'La Ley 115 Art. 1 define la educacion como un proceso de formacion permanente, personal, cultural y social que se fundamenta en una concepcion integral de la persona humana, su dignidad, derechos y deberes. Es un servicio publico con funcion social.',
             'fuente_normativa': 'Ley 115 de 1994 - Art. 1'},
            {'componente': 'normativo', 'dificultad': 'alta',
             'enunciado': 'La Ley 115 de 1994 establece como uno de los fines de la educacion colombiana:',
             'opcion_a': 'La preparacion exclusiva para el trabajo tecnico y tecnologico.',
             'opcion_b': 'El pleno desarrollo de la personalidad sin mas limitaciones que las que le imponen los derechos de los demas.',
             'opcion_c': 'La homogeneizacion cultural de todos los estudiantes colombianos.',
             'opcion_d': 'La memorizacion de los contenidos academicos establecidos por el MEN.',
             'respuesta_correcta': 'B',
             'justificacion': 'La Ley 115 Art. 5 establece 13 fines de la educacion. El primero es el pleno desarrollo de la personalidad. Otros incluyen la formacion en valores, la capacidad critica, el respeto a la diversidad y la formacion para la participacion ciudadana.',
             'fuente_normativa': 'Ley 115 de 1994 - Art. 5'},
            {'componente': 'normativo', 'dificultad': 'media',
             'enunciado': 'Las areas obligatorias y fundamentales establecidas en el Art. 23 de la Ley 115 incluyen:',
             'opcion_a': 'Solo matematicas, lenguaje y ciencias naturales.',
             'opcion_b': 'Ciencias naturales, ciencias sociales, humanidades, matematicas, tecnologia, educacion artistica, educacion fisica, educacion religiosa y etica.',
             'opcion_c': 'Unicamente las areas evaluadas en las pruebas Saber.',
             'opcion_d': 'Las areas que cada IE defina en su PEI sin restriccion alguna.',
             'respuesta_correcta': 'B',
             'justificacion': 'El Art. 23 de la Ley 115 establece 9 grupos de areas obligatorias: ciencias naturales, ciencias sociales, humanidades (lengua castellana e idiomas extranjeros), matematicas, tecnologia, educacion artistica, educacion fisica, educacion religiosa y etica y valores.',
             'fuente_normativa': 'Ley 115 de 1994 - Art. 23'},
            {'componente': 'normativo', 'dificultad': 'alta',
             'enunciado': 'Segun la Ley 115, la autonomia escolar de las IE les permite:',
             'opcion_a': 'Ignorar los lineamientos del MEN y definir libremente todo su curriculo.',
             'opcion_b': 'Organizar las areas obligatorias por asignaturas, definir su PEI, adaptar el curriculo al contexto y establecer areas optativas dentro de los parametros legales.',
             'opcion_c': 'Cobrar tarifas adicionales a los padres para financiar proyectos institucionales.',
             'opcion_d': 'Seleccionar a los estudiantes que pueden acceder segun sus capacidades academicas.',
             'respuesta_correcta': 'B',
             'justificacion': 'La Ley 115 Art. 77 establece la autonomia escolar: las IE pueden organizar su curriculo, adaptar las areas al contexto, definir metodologias y establecer proyectos propios, dentro del marco de los fines, objetivos y areas obligatorias establecidos por la ley.',
             'fuente_normativa': 'Ley 115 de 1994 - Art. 77'},
            {'componente': 'normativo', 'dificultad': 'media',
             'enunciado': 'El gobierno escolar en Colombia, segun la Ley 115, esta conformado por:',
             'opcion_a': 'Solo el rector y los coordinadores de la IE.',
             'opcion_b': 'El Consejo Directivo, el Consejo Academico y el rector.',
             'opcion_c': 'Los docentes y los padres de familia exclusivamente.',
             'opcion_d': 'El MEN, la secretaria de educacion y el rector.',
             'respuesta_correcta': 'B',
             'justificacion': 'La Ley 115 Art. 142 establece que el gobierno escolar esta conformado por: el rector (representante legal), el Consejo Directivo (con representantes de todos los estamentos) y el Consejo Academico (organo consultivo para asuntos academicos).',
             'fuente_normativa': 'Ley 115 de 1994 - Art. 142-145'},
        ]

        # ── SESION 9: PEI y TIC ──
        s9_data = [
            {'componente': 'normativo', 'dificultad': 'media',
             'enunciado': 'El Proyecto Educativo Institucional (PEI) de una IE colombiana debe contener obligatoriamente:',
             'opcion_a': 'Solo el horizonte institucional (mision, vision y valores).',
             'opcion_b': 'La identidad institucional, el componente pedagogico, el componente de gestion y el componente comunitario.',
             'opcion_c': 'Unicamente el manual de convivencia y el SIEE.',
             'opcion_d': 'El presupuesto anual y el plan de compras de la IE.',
             'respuesta_correcta': 'B',
             'justificacion': 'El PEI segun la Ley 115 Art. 73 y el Decreto 1075 debe incluir: principios y fundamentos (identidad), analisis de la situacion institucional, objetivos generales, estrategia pedagogica, organizacion y gestion, y componente comunitario.',
             'fuente_normativa': 'Ley 115 Art. 73 - Decreto 1075 de 2015'},
            {'componente': 'pedagogico', 'dificultad': 'alta',
             'enunciado': 'El uso pedagogico de las TIC en el aula, segun el MEN colombiano, se fundamenta en que:',
             'opcion_a': 'La tecnologia reemplaza al docente en el proceso de ensenanza.',
             'opcion_b': 'Las TIC son herramientas mediadoras que potencian el aprendizaje cuando se usan con intencionalidad pedagogica alineada con competencias y objetivos de aprendizaje.',
             'opcion_c': 'El uso de dispositivos electronicos garantiza por si mismo mejores resultados academicos.',
             'opcion_d': 'Las TIC solo deben usarse en la clase de tecnologia e informatica.',
             'respuesta_correcta': 'B',
             'justificacion': 'El MEN establece que las TIC son mediadoras del aprendizaje, no fines en si mismas. Su valor pedagogico depende de la intencionalidad didactica con que se usen: deben estar alineadas con competencias, objetivos y estrategias de evaluacion claras.',
             'fuente_normativa': 'MEN - Competencias TIC para el desarrollo profesional docente'},
            {'componente': 'pedagogico', 'dificultad': 'media',
             'enunciado': 'Las competencias TIC del docente colombiano, segun el MEN, se organizan en cinco niveles que van desde:',
             'opcion_a': 'El uso basico de internet hasta la programacion de aplicaciones.',
             'opcion_b': 'Explorador (uso basico), integrador (incorpora TIC al aula), innovador (transforma practicas), lider (orienta a otros) e investigador (genera conocimiento).',
             'opcion_c': 'El uso del computador hasta el diseno de plataformas educativas.',
             'opcion_d': 'La alfabetizacion digital hasta la certificacion en herramientas offimaticas.',
             'respuesta_correcta': 'B',
             'justificacion': 'El MEN define 5 niveles de competencia TIC docente: explorador (reconoce e incorpora), integrador (usa TIC en ensenanza), innovador (transforma practicas), lider (orienta comunidad) e investigador (genera conocimiento TIC). Es una progresion de menor a mayor complejidad.',
             'fuente_normativa': 'MEN - Competencias TIC para el desarrollo profesional docente 2013'},
            {'componente': 'normativo', 'dificultad': 'alta',
             'enunciado': 'El ambiente de aprendizaje en educacion se define como:',
             'opcion_a': 'Exclusivamente el espacio fisico del aula de clase.',
             'opcion_b': 'El conjunto de condiciones fisicas, sociales, culturales y pedagogicas que posibilitan experiencias de aprendizaje significativas.',
             'opcion_c': 'Los materiales educativos y recursos tecnologicos disponibles en la IE.',
             'opcion_d': 'El horario y la distribucion del tiempo escolar.',
             'respuesta_correcta': 'B',
             'justificacion': 'El ambiente de aprendizaje es un concepto amplio que incluye dimensiones fisicas (espacio), sociales (relaciones), culturales (significados) y pedagogicas (intencionalidad). Jakeline Duarte y el MEN enfatizan que el ambiente va mas alla del salon de clases.',
             'fuente_normativa': 'MEN - Ambientes de aprendizaje - Duarte'},
            {'componente': 'pedagogico', 'dificultad': 'media',
             'enunciado': 'La Ensenanza para la Comprension (EpC) como marco de planeacion propone que los docentes organicen su ensenanza desde:',
             'opcion_a': 'Los contenidos tematicos del libro de texto por periodo.',
             'opcion_b': 'Topicos generativos, metas de comprension, desempenos de comprension y valoracion continua.',
             'opcion_c': 'Los resultados de las pruebas Saber del ano anterior.',
             'opcion_d': 'Los intereses espontaneos de los estudiantes sin estructura previa.',
             'respuesta_correcta': 'B',
             'justificacion': 'La EpC (Perkins y Blythe, Harvard) organiza la planeacion en cuatro elementos: topicos generativos (temas centrales y conectores), metas de comprension (que comprendera), desempenos de comprension (como demostrara) y valoracion continua (como se retroalimenta).',
             'fuente_normativa': 'EpC - Project Zero Harvard - MEN'},
        ]

        # ── SESION 10: Decreto 1278 ──
        s10_data = [
            {'componente': 'normativo', 'dificultad': 'media',
             'enunciado': 'El Decreto 1278 de 2002 establece el Estatuto de Profesionalizacion Docente. Su principal diferencia con el Decreto 2277 de 1979 es:',
             'opcion_a': 'El Decreto 2277 exige mayor nivel academico que el 1278.',
             'opcion_b': 'El Decreto 1278 vincula el ascenso en el escalafon al merito y la evaluacion de desempeno; el 2277 lo vincula principalmente a la antiguedad y titulos.',
             'opcion_c': 'El Decreto 1278 aplica solo a docentes de secundaria y el 2277 a primaria.',
             'opcion_d': 'Ambos decretos son equivalentes pero aplican a diferentes regiones del pais.',
             'respuesta_correcta': 'B',
             'justificacion': 'La diferencia fundamental es el criterio de ascenso: el Decreto 2277 privilegia la antiguedad y los titulos academicos. El Decreto 1278 introduce la cultura del merito: el ascenso y la reubicacion salarial dependen de la evaluacion de desempeno y las competencias demostradas.',
             'fuente_normativa': 'Decreto 1278 de 2002 vs Decreto 2277 de 1979'},
            {'componente': 'normativo', 'dificultad': 'alta',
             'enunciado': 'Segun el Decreto 1278 de 2002, las funciones del docente en el aula incluyen:',
             'opcion_a': 'Solo dictar clases segun el horario asignado.',
             'opcion_b': 'Planear y desarrollar procesos de ensenanza, evaluar el aprendizaje, promover valores, atender dificultades de aprendizaje y contribuir al PEI.',
             'opcion_c': 'Administrar los recursos fisicos de la IE y supervisar el aseo.',
             'opcion_d': 'Reemplazar al rector en sus funciones administrativas cuando sea necesario.',
             'respuesta_correcta': 'B',
             'justificacion': 'El Decreto 1278 Art. 4 define las funciones docentes en tres dimensiones: en el aula (planear, ensenaar, evaluar), en la institucion (contribuir al PEI, participar en gobierno escolar) y en la comunidad (vincular la IE con el entorno). Las funciones academicas son el nucleo.',
             'fuente_normativa': 'Decreto 1278 de 2002 - Art. 4'},
            {'componente': 'normativo', 'dificultad': 'alta',
             'enunciado': 'La evaluacion de desempeno del docente del Decreto 1278, segun la Guia 31, valora:',
             'opcion_a': 'Solo los resultados academicos de los estudiantes en pruebas estandarizadas.',
             'opcion_b': 'Competencias funcionales (70%) y competencias comportamentales (30%) mediante evidencias de desempeno.',
             'opcion_c': 'Exclusivamente la asistencia y puntualidad del docente.',
             'opcion_d': 'Solo la presentacion de documentos administrativos requeridos.',
             'respuesta_correcta': 'B',
             'justificacion': 'La Guia 31 establece que la evaluacion anual de desempeno valora: competencias funcionales (70%) que incluyen dominio curricular, planeacion, pedagogia, evaluacion del aprendizaje y gestion institucional; y competencias comportamentales (30%) como liderazgo, trabajo en equipo e iniciativa.',
             'fuente_normativa': 'Guia 31 MEN - Evaluacion desempeno Decreto 1278'},
            {'componente': 'normativo', 'dificultad': 'media',
             'enunciado': 'El periodo de prueba en el Decreto 1278 de 2002 es:',
             'opcion_a': 'Un periodo de 5 anos antes de obtener la propiedad en el cargo.',
             'opcion_b': 'Un periodo de un ano en el que el docente recien nombrado demuestra sus competencias, al final del cual es evaluado para obtener la propiedad o ser desvinculado.',
             'opcion_c': 'Una etapa de capacitacion obligatoria antes de ingresar al concurso.',
             'opcion_d': 'El tiempo de preparacion para la evaluacion de competencias del concurso.',
             'respuesta_correcta': 'B',
             'justificacion': 'El Decreto 1278 Art. 31 establece el periodo de prueba: el docente que gana el concurso es nombrado en periodo de prueba por un ano. Al finalizar es evaluado; si supera la evaluacion obtiene la propiedad en el cargo; si no la supera, es retirado del servicio.',
             'fuente_normativa': 'Decreto 1278 de 2002 - Art. 31 - Periodo de prueba'},
            {'componente': 'normativo', 'dificultad': 'alta',
             'enunciado': 'Segun el Decreto 1278 de 2002, el ascenso en el escalafon docente se logra mediante:',
             'opcion_a': 'La antiguedad en el cargo sin necesidad de evaluacion adicional.',
             'opcion_b': 'La obtencion de titulos de posgrado y la superacion de una evaluacion de competencias ante la CNSC.',
             'opcion_c': 'La recomendacion del rector ante la secretaria de educacion.',
             'opcion_d': 'El pago de una inscripcion ante el Ministerio de Educacion Nacional.',
             'respuesta_correcta': 'B',
             'justificacion': 'El Decreto 1278 establece un escalafon de 3 grados (1, 2, 3) con 4 niveles salariales cada uno (A, B, C, D). El ascenso de grado requiere titulo de posgrado y superar una evaluacion de competencias ante la CNSC. La reubicacion salarial (nivel) depende de la evaluacion de desempeno.',
             'fuente_normativa': 'Decreto 1278 de 2002 - Escalafon - Art. 18-21'},
        ]

        total_creadas = 0

        for numero_sesion, datos in [(8, s8_data), (9, s9_data), (10, s10_data)]:
            try:
                sesion = Sesion.objects.get(numero=numero_sesion)
            except Sesion.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Sesion {numero_sesion} no encontrada'))
                continue

            if Pregunta.objects.filter(sesion=sesion).exists():
                self.stdout.write(self.style.WARNING(f'Sesion {numero_sesion} ya tiene preguntas. Omitiendo.'))
                continue

            self.stdout.write(self.style.WARNING(f'\nCargando Sesion {numero_sesion}...'))
            for data in datos:
                data['sesion'] = sesion
                Pregunta.objects.create(**data)
                total_creadas += 1
                self.stdout.write(self.style.SUCCESS(f'  Pregunta creada: {data["enunciado"][:50]}...'))

        self.stdout.write(self.style.SUCCESS(f'\n{total_creadas} preguntas cargadas para sesiones 8, 9 y 10'))
