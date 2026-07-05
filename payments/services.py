import hashlib
import hmac
import requests
from django.conf import settings
from django.core.mail import send_mail


class WompiService:
    @staticmethod
    def base_url():
        return getattr(settings, 'WOMPI_BASE_URL', 'https://sandbox.wompi.co/v1').rstrip('/')

    @staticmethod
    def get_acceptance_token():
        response = requests.get(
            f"{WompiService.base_url()}/merchants/{settings.WOMPI_PUBLIC_KEY}",
            timeout=20,
        )
        if response.status_code != 200:
            raise Exception(f"WOMPI merchant error: {response.status_code} | {response.text}")
        data = response.json()
        return data['data']['presigned_acceptance']['acceptance_token']

    @staticmethod
    def transaction_signature(reference, amount_in_cents, currency='COP'):
        integrity = getattr(settings, 'WOMPI_INTEGRITY_SECRET', '')
        if not integrity:
            return ''
        raw = f'{reference}{amount_in_cents}{currency}{integrity}'
        return hashlib.sha256(raw.encode('utf-8')).hexdigest()


    @staticmethod
    def get_transaction(transaction_id):
        if not getattr(settings, 'WOMPI_PRIVATE_KEY', ''):
            raise Exception('WOMPI_PRIVATE_KEY no configurada')
        response = requests.get(
            f"{WompiService.base_url()}/transactions/{transaction_id}",
            headers={'Authorization': f"Bearer {settings.WOMPI_PRIVATE_KEY}"},
            timeout=20,
        )
        if response.status_code != 200:
            raise Exception(f"WOMPI transaction error: {response.status_code} | {response.text}")
        return response.json().get('data', {})

    @staticmethod
    def validate_event(payload, event_signature=None):
        secret = getattr(settings, 'WOMPI_EVENTS_SECRET', '')
        if not secret:
            return True
        if not event_signature:
            return False
        expected = hmac.new(secret.encode('utf-8'), str(payload).encode('utf-8'), hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected, event_signature)


def send_purchase_confirmation(order):
    if not order.user.email:
        return 0
    modules = ', '.join(item.module.title for item in order.items.select_related('module'))
    subject = 'Compra confirmada - Concurso Docente CNSC 2026'
    body = (
        f'Hola {order.user.nombre},\n\n'
        f'Tu compra fue confirmada.\n'
        f'Orden: {order.reference}\n'
        f'Modulos habilitados: {modules}\n'
        f'Total: {order.total} {order.currency}\n\n'
        'Ya puedes ingresar a tus simulacros premium desde la plataforma.'
    )
    return send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [order.user.email], fail_silently=True)
