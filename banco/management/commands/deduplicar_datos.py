from django.core.management.base import BaseCommand, CommandError
from django.db.models import Count


class Command(BaseCommand):
    help = (
        'Deduplica Simulacro (por nombre) y Subcategoria (por categoria+nombre), '
        'creados por corridas repetidas de apply_market_ready_upgrade/import scripts. '
        'Antes de borrar cada duplicado, reasigna cualquier historial real que dependa '
        'de el (Intento de usuarios -> Simulacro, BancoPregunta -> Subcategoria) al '
        'registro que se conserva, para no perder progreso de nadie. '
        'Corre automaticamente en cada deploy (build.sh) contra la BD real: incluye '
        'una valvula de seguridad que aborta sin borrar nada si el volumen a eliminar '
        'parece anormal, para que un bug futuro en la logica de agrupacion no pueda '
        'arrasar datos de produccion sin que nadie lo note (usar --force para saltarla '
        'de forma deliberada).'
    )

    # Si el numero de filas a eliminar en una corrida supera este umbral (y tambien
    # supera el 50% de las filas totales del modelo), se aborta esa seccion sin
    # borrar nada. Duplicados reales, generados por reintentos de un mismo seed,
    # nunca deberian acercarse a este volumen.
    SAFETY_CAP = 15

    def add_arguments(self, parser):
        parser.add_argument('--check-only', action='store_true', help='Solo reporta, no borra ni reasigna nada.')
        parser.add_argument(
            '--force', action='store_true',
            help='Ignora la valvula de seguridad y borra aunque el volumen parezca anormal.'
        )

    def handle(self, *args, **options):
        check_only = options['check_only']
        force = options['force']
        self._dedupe_simulacros(check_only, force)
        self._dedupe_subcategorias(check_only, force)

    def _safety_check(self, label, planned_total, universe_total, force):
        """Aborta esta seccion (sin tocar la BD) si el borrado planeado luce anormal."""
        if planned_total == 0:
            return True
        looks_abnormal = planned_total > self.SAFETY_CAP and planned_total > universe_total * 0.5
        if looks_abnormal and not force:
            self.stderr.write(self.style.ERROR(
                f'[deduplicar_datos] ABORTADO ({label}): se planeaban eliminar {planned_total} '
                f'de {universe_total} filas — supera la valvula de seguridad ({self.SAFETY_CAP} '
                'filas y >50% del total). No se borro nada en esta seccion. Revisa manualmente '
                '(python manage.py deduplicar_datos --check-only) o vuelve a correr con --force '
                'si el volumen es legitimo.'
            ))
            return False
        return True

    def _dedupe_simulacros(self, check_only, force):
        from simulacros.models import Simulacro
        from seguimiento.models import Intento

        dupes = Simulacro.objects.values('nombre').annotate(n=Count('id')).filter(n__gt=1)
        planes = []
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
            planes.append((conservar, eliminar))

        planned_total = sum(len(eliminar) for _, eliminar in planes)
        universe_total = Simulacro.objects.count()
        if check_only or not self._safety_check('Simulacro', planned_total, universe_total, force):
            return

        total = 0
        for conservar, eliminar in planes:
            for dup in eliminar:
                reasignados = Intento.objects.filter(simulacro=dup).update(simulacro=conservar)
                if reasignados:
                    self.stdout.write(f'  reasignados {reasignados} intentos id={dup.id} -> id={conservar.id}')
                dup.delete()
                total += 1
        self.stdout.write(self.style.SUCCESS(f'Simulacros duplicados eliminados: {total}'))

    def _dedupe_subcategorias(self, check_only, force):
        from banco.models import Subcategoria, BancoPregunta

        dupes = Subcategoria.objects.values('categoria_id', 'nombre').annotate(n=Count('id')).filter(n__gt=1)
        planes = []
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
            planes.append((conservar, eliminar))

        planned_total = sum(len(eliminar) for _, eliminar in planes)
        universe_total = Subcategoria.objects.count()
        if check_only or not self._safety_check('Subcategoria', planned_total, universe_total, force):
            return

        total = 0
        for conservar, eliminar in planes:
            for dup in eliminar:
                reasignadas = BancoPregunta.objects.filter(subcategoria=dup).update(subcategoria=conservar)
                if reasignadas:
                    self.stdout.write(f'  reasignadas {reasignadas} preguntas id={dup.id} -> id={conservar.id}')
                dup.delete()
                total += 1
        self.stdout.write(self.style.SUCCESS(f'Subcategorias duplicadas eliminadas: {total}'))
