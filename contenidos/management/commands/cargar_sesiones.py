from django.core.management.base import BaseCommand
from contenidos.models import Sesion, RecursoNormativo


class Command(BaseCommand):
    help = 'Carga las 12 sesiones del plan de estudio del concurso docente'

    def handle(self, *args, **kwargs):
        sesiones_data = [
            {
                'numero': 1,
                'titulo': 'Modelos Pedagógicos',
                'descripcion': 'Tradicional, constructivista, crítico y por competencias. Teorías, representantes y aplicación en el aula colombiana.',
                'prioridad': 'alta',
                'tiempo_estimado_minutos': 90,
            },
            {
                'numero': 2,
                'titulo': 'Enfoques de Enseñanza-Aprendizaje',
                'descripcion': 'Conductismo, cognitivismo, socioconstructivismo y sus implicaciones pedagógicas.',
                'prioridad': 'alta',
                'tiempo_estimado_minutos': 75,
            },
            {
                'numero': 3,
                'titulo': 'Estrategias Didácticas Activas',
                'descripcion': 'ABP (Aprendizaje Basado en Problemas), aula invertida, aprendizaje colaborativo, gamificación.',
                'prioridad': 'alta',
                'tiempo_estimado_minutos': 75,
            },
            {
                'numero': 4,
                'titulo': 'Evaluación Educativa y Decreto 1290',
                'descripcion': 'Evaluación diagnóstica, formativa y sumativa. Instrumentos: rúbricas, listas de chequeo, pruebas escritas.',
                'prioridad': 'alta',
                'tiempo_estimado_minutos': 90,
            },
            {
                'numero': 5,
                'titulo': 'Planeación de Clase y DBA',
                'descripcion': 'Objetivos, competencias, Derechos Básicos de Aprendizaje, Estándares Básicos de Competencias.',
                'prioridad': 'alta',
                'tiempo_estimado_minutos': 75,
            },
            {
                'numero': 6,
                'titulo': 'Inclusión Educativa y Decreto 1421 de 2017',
                'descripcion': 'PIAR, DUA, atención a la diversidad, educación diferencial.',
                'prioridad': 'alta',
                'tiempo_estimado_minutos': 90,
            },
            {
                'numero': 7,
                'titulo': 'Convivencia Escolar y Gestión de Aula',
                'descripcion': 'Ley 1620 de 2013, Decreto 1965, Guía 49. Rutas de atención, manual de convivencia.',
                'prioridad': 'media',
                'tiempo_estimado_minutos': 75,
            },
            {
                'numero': 8,
                'titulo': 'Normatividad: Ley 115 y Fines de la Educación',
                'descripcion': 'Ley General de Educación, fines, principios, estructura del sistema educativo colombiano.',
                'prioridad': 'alta',
                'tiempo_estimado_minutos': 90,
            },
            {
                'numero': 9,
                'titulo': 'PEI, Ambientes de Aprendizaje y TIC',
                'descripcion': 'Proyecto Educativo Institucional, diseño de ambientes, uso pedagógico de las TIC en el aula.',
                'prioridad': 'media',
                'tiempo_estimado_minutos': 75,
            },
            {
                'numero': 10,
                'titulo': 'Decreto 1278 - Estatuto de Profesionalización Docente',
                'descripcion': 'Funciones docentes, escalafón, evaluación de desempeño, período de prueba, diferencias con Decreto 2277.',
                'prioridad': 'alta',
                'tiempo_estimado_minutos': 90,
            },
            {
                'numero': 11,
                'titulo': 'Simulacro Integrado',
                'descripcion': 'Simulacro de 40 preguntas tipo CNSC cubriendo todas las competencias.',
                'prioridad': 'alta',
                'tiempo_estimado_minutos': 120,
            },
            {
                'numero': 12,
                'titulo': 'Simulacro Final y Estrategia de Examen',
                'descripcion': 'Simulacro final, análisis de errores, técnica de eliminación, gestión del tiempo.',
                'prioridad': 'alta',
                'tiempo_estimado_minutos': 120,
            },
        ]

        recursos_normativos = [
            ('ley', '115 de 1994', 'Ley General de Educación'),
            ('ley', '1620 de 2013', 'Sistema Nacional de Convivencia Escolar'),
            ('decreto', '1278 de 2002', 'Estatuto de Profesionalización Docente'),
            ('decreto', '1290 de 2009', 'Evaluación del Aprendizaje'),
            ('decreto', '1421 de 2017', 'Educación Inclusiva, PIAR y DUA'),
            ('decreto', '1075 de 2015', 'Decreto Único Reglamentario del Sector Educación'),
            ('decreto', '1965 de 2013', 'Reglamenta Ley 1620 de Convivencia Escolar'),
            ('decreto', '915 de 2016', 'Reglamenta concurso docente'),
            ('decreto', '574 de 2022', 'Reglamenta Concurso Docente 2022'),
            ('resolucion', '3842 de 2022', 'Manual de Funciones, Requisitos y Competencias'),
            ('guia', '31', 'Guía para la evaluación de desempeño docente'),
            ('guia', '49', 'Guías pedagógicas para la convivencia escolar'),
        ]

        self.stdout.write(self.style.WARNING('Cargando sesiones...'))
        creadas = 0
        actualizadas = 0
        for data in sesiones_data:
            obj, created = Sesion.objects.update_or_create(
                numero=data['numero'],
                defaults=data
            )
            if created:
                creadas += 1
                self.stdout.write(self.style.SUCCESS(f'  ✓ Creada: Sesión {obj.numero} - {obj.titulo}'))
            else:
                actualizadas += 1
                self.stdout.write(f'  ↻ Actualizada: Sesión {obj.numero} - {obj.titulo}')

        self.stdout.write(self.style.WARNING('\nCargando recursos normativos...'))
        for tipo, numero, titulo in recursos_normativos:
            obj, created = RecursoNormativo.objects.update_or_create(
                tipo=tipo,
                numero=numero,
                defaults={'titulo': titulo}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  ✓ {obj.get_tipo_display()} {obj.numero}'))

        self.stdout.write(self.style.SUCCESS(f'\n✅ Proceso completo: {creadas} sesiones creadas, {actualizadas} actualizadas'))
        self.stdout.write(self.style.SUCCESS(f'✅ {len(recursos_normativos)} recursos normativos registrados'))