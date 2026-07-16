from django.core.management.base import BaseCommand
from django.db.models import Count

from academics.models import Category, Module, NormativeResource
from banco.models import BancoPregunta, Categoria, Subcategoria
from commerce.models import Product
from contenidos.models import Modulo, Tema
from simulacros.models import Simulacro
from usuarios.models import Usuario


TEXT_MODELS = [
    Category,
    Module,
    NormativeResource,
    Categoria,
    Subcategoria,
    BancoPregunta,
    Product,
    Modulo,
    Tema,
    Simulacro,
    Usuario,
]


REPLACEMENTS = {
    '?rea': 'área',
    '?reas': 'áreas',
    '?nico': 'único',
    '?nicos': 'únicos',
    'm?dulo': 'módulo',
    'm?dulos': 'módulos',
    'diagn?stico': 'diagnóstico',
    'Diagn?stico': 'Diagnóstico',
    'cr?tica': 'crítica',
    'Cr?tica': 'Crítica',
    'pedag?gica': 'pedagógica',
    'pedag?gicas': 'pedagógicas',
    'decisi?n': 'decisión',
    'informaci?n': 'información',
    'retroalimentaci?n': 'retroalimentación',
    'Matematicas': 'Matemáticas',
    'Tecnologia e Informatica': 'Tecnología e Informática',
    'Lectura Critica': 'Lectura Crítica',
    'Lectura critica': 'Lectura crítica',
    'Diagnostico inicial': 'Diagnóstico inicial',
    'Competencias pedagogicas': 'Competencias pedagógicas',
    'Pedagogia y didactica': 'Pedagogía y didáctica',
    'Simulacro por area': 'Simulacro por área',
    'Simulacros por area': 'Simulacros por área',
    'Ingles': 'Inglés',
    'Pago unico': 'Pago único',
    'pago unico': 'pago único',
    'Acceso unico': 'Acceso único',
    'acceso unico': 'acceso único',
    'retroalimentacion': 'retroalimentación',
    'Revision tecnica': 'Revisión técnica',
    'revision tecnica': 'revisión técnica',
    'Continuar practica': 'Continuar práctica',
    'Evaluacion': 'Evaluación',
    'evaluacion': 'evaluación',
    'Pedagogia': 'Pedagogía',
    'pedagogia': 'pedagogía',
    'didactica': 'didáctica',
    'Didactica': 'Didáctica',
    'comunicacion': 'comunicación',
    'Comunicacion': 'Comunicación',
    'orientacion': 'orientación',
    'Orientacion': 'Orientación',
    'gestion': 'gestión',
    'Gestion': 'Gestión',
    'Analisis': 'Análisis',
    'analisis': 'análisis',
    'Comprension': 'Comprensión',
    'comprension': 'comprensión',
    'Informacion': 'Información',
    'informacion': 'información',
    'Metacognicion': 'Metacognición',
    'Integracion': 'Integración',
    'integracion': 'integración',
    'Educacion': 'Educación',
    'educacion': 'educación',
}


def repair_encoding(value):
    if not any(marker in value for marker in ("Ã", "Â")):
        return value
    try:
        decoded = value.encode("latin1").decode("utf-8")
    except UnicodeError:
        return value
    return decoded if decoded.count("�") <= value.count("�") else value


class Command(BaseCommand):
    help = 'Corrige textos visibles, codificación y acentos en datos activos sin tocar lógica funcional.'

    def add_arguments(self, parser):
        parser.add_argument('--check-only', action='store_true', help='Solo reporta problemas sin modificar datos.')

    def handle(self, *args, **options):
        check_only = options['check_only']
        scanned = 0
        changed = 0
        suspicious = []

        for model in TEXT_MODELS:
            fields = [
                field.name
                for field in model._meta.fields
                if field.get_internal_type() in {'CharField', 'TextField', 'SlugField', 'EmailField'}
            ]
            for obj in model.objects.all():
                scanned += 1
                updates = {}
                for field in fields:
                    value = getattr(obj, field, None)
                    if not isinstance(value, str) or not value:
                        continue
                    fixed = repair_encoding(value)
                    for source, target in REPLACEMENTS.items():
                        fixed = fixed.replace(source, target)
                    if fixed != value:
                        updates[field] = fixed
                    if any(marker in fixed for marker in ['�', 'Ã', 'Â']) or any(fragment in fixed for fragment in ['?rea', '?nico', '?tica', '?dulo']):
                        suspicious.append((model.__name__, obj.pk, field, fixed[:120]))
                if updates and not check_only:
                    for field, value in updates.items():
                        setattr(obj, field, value)
                    obj.save(update_fields=list(updates.keys()))
                    changed += 1

        active_questions = BancoPregunta.objects.filter(activa=True)
        duplicate_groups = list(
            active_questions.exclude(hash_contenido='')
            .values('hash_contenido')
            .annotate(total=Count('id'))
            .filter(total__gt=1)
        )
        duplicate_questions = sum(row['total'] for row in duplicate_groups)
        total_questions = active_questions.count()
        missing_feedback = active_questions.filter(justificacion='').count()
        invalid_answer = active_questions.exclude(respuesta_correcta__in=['A', 'B', 'C', 'D']).count()

        self.stdout.write(f'Objetos revisados: {scanned}')
        self.stdout.write(f'Objetos corregidos: {changed}')
        self.stdout.write(f'Preguntas activas: {total_questions}')
        self.stdout.write(f'Preguntas sin justificación: {missing_feedback}')
        self.stdout.write(f'Preguntas con respuesta inválida: {invalid_answer}')
        self.stdout.write(
            f'Preguntas activas con hash_contenido duplicado: {duplicate_questions} '
            f'en {len(duplicate_groups)} grupos'
        )
        if suspicious:
            self.stdout.write(self.style.WARNING(f'Textos sospechosos pendientes: {len(suspicious)}'))
            for item in suspicious[:20]:
                self.stdout.write(self.style.WARNING(str(item)))
        else:
            self.stdout.write(self.style.SUCCESS('Sin textos corruptos visibles detectados.'))
        if missing_feedback or invalid_answer or duplicate_questions:
            # Se reporta como advertencia, no se aborta el build: un problema de
            # contenido (una pregunta sin justificacion, un hash duplicado) no
            # deberia poder bloquear el despliegue de un arreglo de codigo no
            # relacionado (ver build.sh, que usa "set -o errexit").
            self.stdout.write(self.style.WARNING(
                'Hay problemas de calidad de datos pendientes de revisar en el admin (no bloquean el deploy).'
            ))
