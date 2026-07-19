from django.conf import settings
from django.core.management.base import BaseCommand
from django.urls import reverse

from banco.models import BancoPregunta
from dashboard.question_generator import QUESTION_CATEGORY, SIMILARITY_THRESHOLD, jaccard, normalize, token_set
from commerce.models import Product
from simulacros.models import Simulacro


class Command(BaseCommand):
    help = 'Verifica configuracion critica, banco de preguntas, pago único y simulacros activos.'

    def handle(self, *args, **options):
        issues = []
        warnings = []

        def ok(label):
            self.stdout.write(self.style.SUCCESS(f'[OK] {label}'))

        def warn(label):
            warnings.append(label)
            self.stdout.write(self.style.WARNING(f'[WARN] {label}'))

        def fail(label):
            issues.append(label)
            self.stdout.write(self.style.ERROR(f'[FALTA] {label}'))

        self.stdout.write('Verificacion ConcursoDocente Premium')

        if settings.DEBUG:
            warn('DEBUG=True: correcto para local, no usar asi en produccion.')
        else:
            ok('DEBUG=False')

        if settings.SECRET_KEY and not settings.SECRET_KEY.startswith('django-insecure-'):
            ok('SECRET_KEY seguro configurado')
        elif settings.DEBUG:
            warn('SECRET_KEY de desarrollo activa. Cambiar antes de produccion.')
        else:
            fail('SECRET_KEY seguro requerido con DEBUG=False')

        if settings.ALLOWED_HOSTS:
            ok('ALLOWED_HOSTS configurado')
        else:
            fail('ALLOWED_HOSTS vacio')

        if getattr(settings, 'GOOGLE_OAUTH_CLIENT_ID', '') and getattr(settings, 'GOOGLE_OAUTH_CLIENT_SECRET', '') and getattr(settings, 'GOOGLE_OAUTH_REDIRECT_URI', ''):
            ok('Google OAuth configurado')
        else:
            fail('Google OAuth incompleto: CLIENT_ID, CLIENT_SECRET y REDIRECT_URI son obligatorios')

        redirect = getattr(settings, 'GOOGLE_OAUTH_REDIRECT_URI', '')
        expected_path = reverse('google_callback')
        if redirect and redirect.endswith(expected_path):
            ok('Google redirect URI termina en /cuentas/google/callback/')
        elif redirect:
            fail('Google redirect URI no coincide con /cuentas/google/callback/')

        missing_wompi = []
        for name in ['WOMPI_PUBLIC_KEY', 'WOMPI_PRIVATE_KEY', 'WOMPI_INTEGRITY_SECRET', 'WOMPI_EVENTS_SECRET']:
            if not getattr(settings, name, ''):
                missing_wompi.append(name)

        public_key = getattr(settings, 'WOMPI_PUBLIC_KEY', '').strip()
        base_url = getattr(settings, 'WOMPI_BASE_URL', '').strip().lower()
        if public_key.startswith('pub_prod_') and 'sandbox' in base_url:
            missing_wompi.append('WOMPI_BASE_URL debe ser https://production.wompi.co/v1 para llaves pub_prod_')
        if public_key.startswith('pub_test_') and 'production' in base_url:
            missing_wompi.append('WOMPI_BASE_URL debe ser https://sandbox.wompi.co/v1 para llaves pub_test_')

        if not missing_wompi:
            ok('Wompi configurado')
        elif settings.DEBUG:
            warn('Wompi incompleto. Faltan: ' + ', '.join(missing_wompi) + '. Para pruebas locales solo puedes simular pago si ENABLE_LOCAL_PAYMENT_APPROVAL=True.')
        else:
            fail('Wompi incompleto para produccion. Faltan: ' + ', '.join(missing_wompi))

        email_backend = getattr(settings, 'EMAIL_BACKEND', '')
        if 'console' in email_backend and settings.DEBUG:
            warn('EMAIL_BACKEND usa consola. Correcto local; no envia correos reales.')
        elif 'console' in email_backend:
            fail('EMAIL_BACKEND usa consola. En produccion no enviara correos reales.')
        elif getattr(settings, 'EMAIL_HOST', '') or 'sendgrid' in email_backend.lower() or 'resend' in email_backend.lower():
            ok('Email transaccional configurado')
        else:
            fail('Email transaccional no configurado')

        question_qs = BancoPregunta.objects.filter(categoria__nombre=QUESTION_CATEGORY, activa=True)
        questions = question_qs.count()
        simulacros = Simulacro.objects.filter(activo=True).count()
        area_simulacros = Simulacro.objects.filter(activo=True, tipo='area').count()
        products = Product.objects.filter(active=True).count()

        if questions >= 360:
            ok(f'Banco premium cargado: {questions} preguntas')
        else:
            fail(f'Banco premium insuficiente: {questions} preguntas')

        seen_items = set()
        duplicate_items = 0
        duplicate_hashes = 0
        semantic_duplicates = 0
        recycled_options = 0
        invalid_options = 0
        invalid_answers = 0
        missing_feedback = 0
        missing_metadata = 0
        seen_hashes = set()
        seen_options = set()
        signatures = []
        levels = set()
        for question in question_qs:
            key = (''.join((question.contexto or '').lower().split()), ''.join((question.enunciado or '').lower().split()))
            if key in seen_items:
                duplicate_items += 1
            seen_items.add(key)

            if not question.hash_contenido or not question.nivel_dificultad:
                missing_metadata += 1
            if question.hash_contenido:
                if question.hash_contenido in seen_hashes:
                    duplicate_hashes += 1
                seen_hashes.add(question.hash_contenido)
            if question.nivel_dificultad:
                levels.add(question.nivel_dificultad)

            options = [
                normalize(question.opcion_a or ''),
                normalize(question.opcion_b or ''),
                normalize(question.opcion_c or ''),
                normalize(question.opcion_d or ''),
            ]
            if len(set(options)) != 4 or any(not option for option in options):
                invalid_options += 1
            for option in options:
                if option in seen_options:
                    recycled_options += 1
                seen_options.add(option)

            signature = token_set((question.contexto or '') + ' ' + (question.enunciado or ''))
            for previous in signatures:
                if jaccard(signature, previous) > SIMILARITY_THRESHOLD:
                    semantic_duplicates += 1
                    break
            signatures.append(signature)

            if question.respuesta_correcta not in {'A', 'B', 'C', 'D'}:
                invalid_answers += 1
            if not (question.justificacion or '').strip():
                missing_feedback += 1

        if duplicate_items:
            fail(f'Banco con preguntas duplicadas: {duplicate_items}')
        else:
            ok('Banco sin duplicados exactos de contexto/enunciado')
        if duplicate_hashes:
            fail(f'Banco con hashes duplicados: {duplicate_hashes}')
        else:
            ok('Hashes de contenido unicos')
        if semantic_duplicates:
            fail(f'Banco con preguntas demasiado similares: {semantic_duplicates}')
        else:
            ok('Banco sin similitud semantica por encima del umbral')
        if recycled_options:
            fail(f'Opciones recicladas literalmente entre preguntas: {recycled_options}')
        else:
            ok('Opciones sin reciclaje literal entre preguntas')
        if missing_metadata:
            fail(f'Preguntas sin hash o nivel de dificultad: {missing_metadata}')
        else:
            ok('Metadatos de hash y nivel completos')
        expected_levels = {'basico', 'intermedio', 'avanzado'}
        if expected_levels.issubset(levels):
            ok('Distribucion incluye niveles basico, intermedio y avanzado')
        else:
            fail('Faltan niveles de dificultad: ' + ', '.join(sorted(expected_levels - levels)))
        if invalid_options:
            fail(f'Preguntas con opciones repetidas o vacias: {invalid_options}')
        else:
            ok('Opciones de respuesta unicas y completas')
        if invalid_answers:
            fail(f'Preguntas con respuesta correcta invalida: {invalid_answers}')
        else:
            ok('Respuesta correcta valida en todas las preguntas')
        if missing_feedback:
            fail(f'Preguntas sin justificacion tecnica: {missing_feedback}')
        else:
            ok('Retroalimentación tecnica registrada en todas las preguntas')

        if simulacros >= 12:
            ok(f'Simulacros activos: {simulacros}')
        else:
            fail(f'Simulacros activos insuficientes: {simulacros}')

        expected_areas = {'ingles', 'tecnologia', 'matematicas', 'ciencias_naturales', 'ciencias_sociales'}
        loaded_areas = set(Simulacro.objects.filter(activo=True, tipo='area').values_list('area', flat=True))
        missing_areas = sorted(expected_areas - loaded_areas)
        if area_simulacros >= 5 and not missing_areas:
            ok(f'Simulacros por área: {area_simulacros}')
        else:
            fail(f'Simulacros por área insuficientes: {area_simulacros}. Faltan: {", ".join(missing_areas)}')

        active_products = Product.objects.filter(active=True).select_related('module')
        elite_product = active_products.filter(module__slug='elite-cnsc-2026').first()
        if products == 1 and elite_product and elite_product.final_price == 20000:
            ok('Producto unico activo: acceso completo por COP 20.000')
        else:
            fail(f'Modelo de pago inconsistente: {products} producto(s) activo(s). Debe existir solo elite-cnsc-2026 por COP 20.000')

        self.stdout.write('')
        if issues:
            self.stdout.write(self.style.ERROR(f'Resultado: {len(issues)} faltante(s) critico(s).'))
            raise SystemExit(1)
        if warnings:
            self.stdout.write(self.style.WARNING(f'Resultado: listo para local con {len(warnings)} advertencia(s).'))
        else:
            self.stdout.write(self.style.SUCCESS('Resultado: listo.'))
