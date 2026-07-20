from django.core.management.base import BaseCommand, CommandError
from django.db.models import Count


class Command(BaseCommand):
    help = (
        'Deduplica Simulacro (por nombre), Subcategoria (por categoria+nombre) y Tema '
        '(por modulo+orden, y por modulo+titulo), creados por corridas repetidas de '
        'apply_market_ready_upgrade/import scripts o por fusiones de Modulo (ver '
        'repair_text_quality._reparar_tipo_modulo). Antes de borrar cada duplicado, '
        'reasigna cualquier historial real que dependa de el (Intento de usuarios -> '
        'Simulacro, BancoPregunta -> Subcategoria) al registro que se conserva, para no '
        'perder progreso de nadie. Corre automaticamente en cada deploy (build.sh), '
        'ANTES de seed_modulos, para garantizar que Tema.objects.update_or_create('
        'modulo=modulo, orden=topic_order, ...) nunca reciba una combinacion (modulo, '
        'orden) duplicada y falle con MultipleObjectsReturned. Incluye una valvula de '
        'seguridad que aborta sin borrar nada si el volumen a eliminar parece anormal, '
        'para que un bug futuro en la logica de agrupacion no pueda arrasar datos de '
        'produccion sin que nadie lo note (usar --force para saltarla de forma '
        'deliberada).'
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
        self._dedupe_temas(check_only, force)
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

    def _dedupe_temas(self, check_only, force):
        from contenidos.models import Tema

        # Tema no tiene hoy ningun modelo que le apunte por FK (verificado:
        # solo Tema.modulo -> Modulo existe en ese sentido). Si en el futuro
        # se agrega una relacion hacia Tema, reasignarla aqui antes del
        # delete, igual que se hace abajo con Intento/BancoPregunta.
        def score(t):
            return (bool((t.descripcion or '').strip()), t.activo, t.id)

        def planear(queryset_dupes, obtener_grupo, etiqueta):
            planes = []
            vistos_para_eliminar = set()
            for d in queryset_dupes:
                grupo = [t for t in obtener_grupo(d) if t.id not in vistos_para_eliminar]
                if len(grupo) < 2:
                    continue
                grupo.sort(key=score)
                conservar = grupo[-1]
                eliminar = grupo[:-1]
                self.stdout.write(
                    f'Tema [{etiqueta}] "{conservar.titulo}" (modulo_id={conservar.modulo_id}): '
                    f'conservar id={conservar.id} (orden={conservar.orden}), '
                    f'eliminar ids={[t.id for t in eliminar]}'
                )
                vistos_para_eliminar.update(t.id for t in eliminar)
                planes.append((conservar, eliminar))
            return planes

        # Pasada 1: mismo (modulo, orden) - es la clave logica real que usa
        # seed_modulos.update_or_create(modulo=modulo, orden=topic_order, ...).
        # Un duplicado aqui es exactamente lo que revienta el deploy con
        # MultipleObjectsReturned (incidente de produccion de julio 2026,
        # originado en una fusion de Modulo que movia Tema sin revisar esto -
        # ver repair_text_quality._reparar_tipo_modulo, ya corregido tambien).
        dupes_orden = Tema.objects.values('modulo_id', 'orden').annotate(n=Count('id')).filter(n__gt=1)
        planes = planear(
            dupes_orden,
            lambda d: list(Tema.objects.filter(modulo_id=d['modulo_id'], orden=d['orden']).order_by('id')),
            'mismo modulo+orden',
        )

        # Pasada 2: mismo (modulo, titulo) con 'orden' distinto - duplicado
        # logico aunque todavia no choque con la clave tecnica de arriba.
        dupes_titulo = Tema.objects.values('modulo_id', 'titulo').annotate(n=Count('id')).filter(n__gt=1)
        planes += planear(
            dupes_titulo,
            lambda d: list(Tema.objects.filter(modulo_id=d['modulo_id'], titulo=d['titulo']).order_by('id')),
            'mismo modulo+titulo',
        )

        planned_total = sum(len(eliminar) for _, eliminar in planes)
        universe_total = Tema.objects.count()
        if check_only or not self._safety_check('Tema', planned_total, universe_total, force):
            return

        total = 0
        for conservar, eliminar in planes:
            for dup in eliminar:
                dup.delete()
                total += 1
        self.stdout.write(self.style.SUCCESS(f'Temas duplicados eliminados: {total}'))

    def _dedupe_simulacros(self, check_only, force):
        from simulacros.models import Simulacro
        from seguimiento.models import Intento

        def score(s):
            return (Intento.objects.filter(simulacro=s).count(), s.activo, s.id)

        def planear(queryset_dupes, obtener_grupo, etiqueta):
            planes = []
            vistos_para_eliminar = set()
            for d in queryset_dupes:
                grupo = [s for s in obtener_grupo(d) if s.id not in vistos_para_eliminar]
                if len(grupo) < 2:
                    continue
                grupo.sort(key=score)
                conservar = grupo[-1]
                eliminar = grupo[:-1]
                self.stdout.write(
                    f'Simulacro [{etiqueta}] "{conservar.nombre}": conservar id={conservar.id} '
                    f'(activo={conservar.activo}), eliminar ids={[s.id for s in eliminar]}'
                )
                vistos_para_eliminar.update(s.id for s in eliminar)
                planes.append((conservar, eliminar))
            return planes

        # Pasada 1: mismo nombre exacto (duplicados de reintentos de seed).
        dupes_nombre = Simulacro.objects.values('nombre').annotate(n=Count('id')).filter(n__gt=1)
        planes = planear(
            dupes_nombre,
            lambda d: list(Simulacro.objects.filter(nombre=d['nombre']).order_by('id')),
            'mismo nombre',
        )

        # Pasada 2: mismo (module, tipo, area) con nombres distintos - ocurre
        # cuando un rename (renombrar_arquitectura_institucional) alcanza una
        # fila pero deja huerfana otra con un nombre viejo que ya no esta en
        # su mapa de renombres (ej. sufijo "- Simulacro premium V2").
        dupes_modulo = (
            Simulacro.objects.exclude(module__isnull=True)
            .values('module_id', 'tipo', 'area').annotate(n=Count('id')).filter(n__gt=1)
        )
        planes += planear(
            dupes_modulo,
            lambda d: list(Simulacro.objects.filter(
                module_id=d['module_id'], tipo=d['tipo'], area=d['area']
            ).order_by('id')),
            'mismo modulo',
        )

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
