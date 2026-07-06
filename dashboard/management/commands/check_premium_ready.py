from django.conf import settings
from django.core.management.base import BaseCommand
from django.urls import reverse

from banco.models import BancoPregunta
from commerce.models import Product
from simulacros.models import Simulacro


class Command(BaseCommand):
    help = 'Verifica la configuración crítica de la plataforma premium sin imprimir secretos.'

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

        self.stdout.write('Verificación ConcursoDocente Premium')

        if settings.DEBUG:
            warn('DEBUG=True: correcto para local, no usar así en producción.')
        else:
            ok('DEBUG=False')

        if settings.SECRET_KEY and not settings.SECRET_KEY.startswith('django-insecure-'):
            ok('SECRET_KEY seguro configurado')
        elif settings.DEBUG:
            warn('SECRET_KEY de desarrollo activa. Cambiar antes de producción.')
        else:
            fail('SECRET_KEY seguro requerido con DEBUG=False')

        if settings.ALLOWED_HOSTS:
            ok('ALLOWED_HOSTS configurado')
        else:
            fail('ALLOWED_HOSTS vacío')

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
        if not getattr(settings, 'WOMPI_PUBLIC_KEY', ''):
            missing_wompi.append('WOMPI_PUBLIC_KEY')
        if not getattr(settings, 'WOMPI_PRIVATE_KEY', ''):
            missing_wompi.append('WOMPI_PRIVATE_KEY')
        if not getattr(settings, 'WOMPI_INTEGRITY_SECRET', ''):
            missing_wompi.append('WOMPI_INTEGRITY_SECRET')
        if not getattr(settings, 'WOMPI_EVENTS_SECRET', ''):
            missing_wompi.append('WOMPI_EVENTS_SECRET')

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
            fail('Wompi incompleto para producción. Faltan: ' + ', '.join(missing_wompi))

        email_backend = getattr(settings, 'EMAIL_BACKEND', '')
        if 'console' in email_backend:
            warn('EMAIL_BACKEND usa consola. Correcto local; no envía correos reales.')
        elif getattr(settings, 'EMAIL_HOST', '') or 'sendgrid' in email_backend.lower() or 'resend' in email_backend.lower():
            ok('Email transaccional configurado')
        else:
            fail('Email transaccional no configurado')

        questions = BancoPregunta.objects.filter(categoria__nombre='Banco Premium CNSC 2026 V3', activa=True).count()
        simulacros = Simulacro.objects.filter(activo=True).count()
        area_simulacros = Simulacro.objects.filter(activo=True, tipo='area').count()
        products = Product.objects.filter(active=True).count()

        if questions >= 360:
            ok(f'Banco premium cargado: {questions} preguntas')
        else:
            fail(f'Banco premium insuficiente: {questions} preguntas')

        if simulacros >= 12:
            ok(f'Simulacros activos: {simulacros}')
        else:
            fail(f'Simulacros activos insuficientes: {simulacros}')

        expected_areas = {'ingles', 'tecnologia', 'matematicas', 'ciencias_naturales', 'ciencias_sociales'}
        loaded_areas = set(
            Simulacro.objects.filter(activo=True, tipo='area').values_list('area', flat=True)
        )
        missing_areas = sorted(expected_areas - loaded_areas)

        if area_simulacros >= 5 and not missing_areas:
            ok(f'Simulacros por área: {area_simulacros}')
        else:
            fail(f'Simulacros por área insuficientes: {area_simulacros}. Faltan: {", ".join(missing_areas)}')

        if products >= 9:
            ok(f'Productos activos: {products}')
        else:
            fail(f'Productos activos insuficientes: {products}')

        self.stdout.write('')
        if issues:
            self.stdout.write(self.style.ERROR(f'Resultado: {len(issues)} faltante(s) critico(s).'))
            raise SystemExit(1)
        if warnings:
            self.stdout.write(self.style.WARNING(f'Resultado: listo para local con {len(warnings)} advertencia(s).'))
        else:
            self.stdout.write(self.style.SUCCESS('Resultado: listo.'))
