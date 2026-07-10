from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Compatibilidad: redirige la carga antigua al upgrade vigente con pago unico y banco auditado.'

    def handle(self, *args, **options):
        call_command('apply_market_ready_upgrade')
