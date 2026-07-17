from django.core.management.base import BaseCommand
from django.db.models import Count


class Command(BaseCommand):
    help = (
        'Deduplica Simulacro (por nombre) y Subcategoria (por categoria+nombre), '
        'creados por corridas repetidas de apply_market_ready_upgrade/import scripts. '
        'Antes de borrar cada duplicado, reasigna cualquier historial real que dependa '
        'de el (Intento de usuarios -> Simulacro, BancoPregunta -> Subcategoria) al '
        'registro que se conserva, para no perder progreso de nadie.'
    )

    def add_arguments(self, parser):
        parser.add_argument('--check-only', action='store_true', help='Solo reporta, no borra ni reasigna nada.')

    def handle(self, *args, **options):
        check_only = options['check_only']
        self._dedupe_simulacros(check_only)
        self._dedupe_subcategorias(check_only)

    def _dedupe_simulacros(self, check_only):
        from simulacros.models import Simulacro
        from seguimiento.models import Intento

        dupes = Simulacro.objects.values('nombre').annotate(n=Count('id')).filter(n__gt=1)
        total = 0
        for d in dupes:
            grupo = list(Simulacro.objects.filter(nombre=d['nombre']).order_by('id'))

            def score(s):
                return (Intento.objects.filter(simulacro=s).count(), s.activo, s.id)

            grupo.sort(key=score)
            conservar = grupo[-1]
            eliminar = grupo[:-1]
            self.stdout.write(
                f'Simulacro "{d["nombre"]}": conservar id={conservar.id} '
                f'(activo={conservar.activo}), eliminar ids={[s.id for s in eliminar]}'
            )
            if not check_only:
                for dup in eliminar:
                    reasignados = Intento.objects.filter(simulacro=dup).update(simulacro=conservar)
                    if reasignados:
                        self.stdout.write(f'  reasignados {reasignados} intentos id={dup.id} -> id={conservar.id}')
                    dup.delete()
                    total += 1
        self.stdout.write(self.style.SUCCESS(f'Simulacros duplicados eliminados: {total}'))

    def _dedupe_subcategorias(self, check_only):
        from banco.models import Subcategoria, BancoPregunta

        dupes = Subcategoria.objects.values('categoria_id', 'nombre').annotate(n=Count('id')).filter(n__gt=1)
        total = 0
        for d in dupes:
            grupo = list(
                Subcategoria.objects.filter(categoria_id=d['categoria_id'], nombre=d['nombre']).order_by('id')
            )

            def score(s):
                return (BancoPregunta.objects.filter(subcategoria=s).count(), s.id)

            grupo.sort(key=score)
            conservar = grupo[-1]
            eliminar = grupo[:-1]
            self.stdout.write(
                f'Subcategoria "{d["nombre"]}" (categoria_id={d["categoria_id"]}): '
                f'conservar id={conservar.id}, eliminar ids={[s.id for s in eliminar]}'
            )
            if not check_only:
                for dup in eliminar:
                    reasignadas = BancoPregunta.objects.filter(subcategoria=dup).update(subcategoria=conservar)
                    if reasignadas:
                        self.stdout.write(f'  reasignadas {reasignadas} preguntas id={dup.id} -> id={conservar.id}')
                    dup.delete()
                    total += 1
        self.stdout.write(self.style.SUCCESS(f'Subcategorias duplicadas eliminadas: {total}'))
