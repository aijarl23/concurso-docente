from django.core.management.base import BaseCommand
from django.db import transaction
from contenidos.models import Sesion
from evaluaciones.models import Pregunta


class Command(BaseCommand):
    help = 'Limpia preguntas duplicadas por sesión y muestra estado real del banco'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('🔍 DIAGNÓSTICO PREVIO A LA LIMPIEZA\n'))

        total_antes = Pregunta.objects.count()
        self.stdout.write(f'Total preguntas antes: {total_antes}\n')

        for sesion in Sesion.objects.all().order_by('numero'):
            preguntas = Pregunta.objects.filter(sesion=sesion).order_by('id')
            count = preguntas.count()
            self.stdout.write(f'  Sesión {sesion.numero} ({sesion.titulo[:30]}): {count} preguntas')

        self.stdout.write(self.style.WARNING('\n🧹 INICIANDO LIMPIEZA DE DUPLICADOS\n'))

        total_eliminadas = 0
        MAX_POR_SESION = 30

        with transaction.atomic():
            for sesion in Sesion.objects.all().order_by('numero'):
                preguntas = Pregunta.objects.filter(sesion=sesion).order_by('id')
                count = preguntas.count()

                if count <= MAX_POR_SESION:
                    self.stdout.write(
                        self.style.SUCCESS(f'  ✓ Sesión {sesion.numero}: {count} preguntas — OK')
                    )
                    continue

                # Detectar duplicados por enunciado
                enunciados_vistos = set()
                ids_duplicados = []

                for p in preguntas:
                    enunciado_norm = p.enunciado.strip()[:100]
                    if enunciado_norm in enunciados_vistos:
                        ids_duplicados.append(p.id)
                    else:
                        enunciados_vistos.add(enunciado_norm)

                if ids_duplicados:
                    Pregunta.objects.filter(id__in=ids_duplicados).delete()
                    eliminadas = len(ids_duplicados)
                    total_eliminadas += eliminadas
                    self.stdout.write(
                        self.style.WARNING(
                            f'  ⚠ Sesión {sesion.numero}: {count} → {count - eliminadas} '
                            f'(eliminados {eliminadas} duplicados exactos)'
                        )
                    )
                else:
                    # Si no hay duplicados exactos pero hay más de 30,
                    # mantenemos las primeras 30 (las de mejor calidad)
                    ids_exceso = list(preguntas.values_list('id', flat=True)[MAX_POR_SESION:])
                    Pregunta.objects.filter(id__in=ids_exceso).delete()
                    eliminadas = len(ids_exceso)
                    total_eliminadas += eliminadas
                    self.stdout.write(
                        self.style.WARNING(
                            f'  ⚠ Sesión {sesion.numero}: {count} → {MAX_POR_SESION} '
                            f'(recortadas {eliminadas} preguntas excedentes)'
                        )
                    )

        self.stdout.write(self.style.WARNING(f'\n📊 ESTADO FINAL\n'))
        total_despues = Pregunta.objects.count()

        for sesion in Sesion.objects.all().order_by('numero'):
            count = Pregunta.objects.filter(sesion=sesion).count()
            status = '✅' if count >= 25 else ('⚠️' if count > 0 else '❌')
            self.stdout.write(f'  {status} Sesión {sesion.numero}: {count} preguntas')

        self.stdout.write(
            self.style.SUCCESS(
                f'\n✅ Limpieza completada: '
                f'{total_antes} → {total_despues} preguntas '
                f'({total_eliminadas} eliminadas)'
            )
        )
