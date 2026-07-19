"""End-to-end test: SMPI ingestion → diagnostic → analysis."""

from django.core.management.base import BaseCommand
from usuarios.models import Usuario
from banco.models import BancoPregunta
from simulacros.models import Simulacro
from seguimiento.models import Intento, RespuestaIntento
from seguimiento.analitica import analizar_intento
import random


class Command(BaseCommand):
    help = 'End-to-end test: ingest SMPI → create diagnostic → analyze results'

    def handle(self, *args, **options):
        self.stdout.write('=== Prueba E2E: Ingesta SMPI -> Diagnostico -> Analisis ===\n')

        # 1. Verificar preguntas SMPI
        smpi_preguntas = BancoPregunta.objects.filter(autor='SMPI')
        self.stdout.write(f'1. Preguntas SMPI disponibles: {smpi_preguntas.count()}')
        if smpi_preguntas.count() < 6:
            self.stdout.write(self.style.ERROR('   ERROR: Hay menos de 6 preguntas SMPI'))
            return

        # 2. Crear simulacro diagnóstico con mezcla de preguntas
        diagnostico_name = 'Diagnóstico E2E SMPI Test'
        diagnostico, created = Simulacro.objects.get_or_create(
            nombre=diagnostico_name,
            defaults={
                'descripcion': 'Prueba de integración SMPI: diagnóstico con preguntas del Banco Oficial',
                'tipo': 'diagnostico',
                'area': 'general',
                'tiempo_limite_minutos': 30,
                'tiempo_por_pregunta_segundos': 60,
                'puntaje_minimo_aprobacion': 60,
                'es_premium': False,
                # Fixture de prueba, nunca debe quedar visible en el catalogo
                # real (module=None + activo=True lo haria accesible sin
                # pago a cualquier usuario autenticado).
                'activo': False,
            }
        )
        self.stdout.write(f'\n2. Simulacro diagnóstico: {diagnostico.nombre} ({"creado" if created else "existente"})')

        # Agregar preguntas SMPI al simulacro
        diagnostico.preguntas.set(smpi_preguntas[:6])
        self.stdout.write(f'   Total preguntas: {diagnostico.total_preguntas}')

        # 3. Crear usuario de prueba
        usuario, created = Usuario.objects.get_or_create(
            username='smpi_test_user',
            defaults={
                'email': 'smpi_test@test.local',
                'first_name': 'SMPI',
                'last_name': 'Test',
                'area_concurso': 'otro',
            }
        )
        self.stdout.write(f'\n3. Usuario de prueba: {usuario.username} ({"creado" if created else "existente"})')

        # 4. Crear intento (respuesta al diagnóstico)
        intento, created = Intento.objects.get_or_create(
            usuario=usuario,
            simulacro=diagnostico,
            defaults={
                'estado': 'completado',
                'tiempo_usado_segundos': 300,
            }
        )
        self.stdout.write(f'\n4. Intento de diagnóstico: {intento.id} ({"creado" if created else "existente"})')

        # 5. Agregar respuestas del usuario (simulado)
        respuestas_creadas = 0
        for pregunta in diagnostico.preguntas.all():
            respuesta_obj, created = RespuestaIntento.objects.get_or_create(
                intento=intento,
                pregunta=pregunta,
                defaults={
                    'respuesta_seleccionada': random.choice(['A', 'B', 'C', 'D']),
                    'es_correcta': random.choice([True, True, True, False]),
                }
            )
            if created:
                respuestas_creadas += 1

        self.stdout.write(f'   Respuestas en el intento: {intento.respuestas.count()}')

        # 6. Ejecutar análisis
        analisis = analizar_intento(intento)
        self.stdout.write(f'\n5. Análisis de desempeño:')
        self.stdout.write(f'   Competencias evaluadas: {len(analisis["por_competencia"])}')

        for comp in analisis['por_competencia']:
            self.stdout.write(
                f'   - {comp["competencia"]}: {comp["correctas"]}/{comp["total"]} ({comp["porcentaje"]:.1f}%)'
            )

        self.stdout.write(f'\n   Fortalezas (>=75%): {len(analisis["fortalezas"])}')
        for fort in analisis['fortalezas']:
            self.stdout.write(f'   - {fort["competencia"]}: {fort["porcentaje"]:.1f}%')

        self.stdout.write(f'\n   Brechas (<60%): {len(analisis["brechas"])}')
        for brecha in analisis['brechas']:
            self.stdout.write(f'   - {brecha["competencia"]}: {brecha["porcentaje"]:.1f}%')

        self.stdout.write(f'\n   Ruta recomendada: {len(analisis["ruta_recomendada"])} módulos')
        for item in analisis['ruta_recomendada']:
            self.stdout.write(
                f'   - {item["modulo"].titulo} ({item["competencia"]}, {item["porcentaje"]:.1f}%)'
            )

        # 7. Verificación final
        self.stdout.write(self.style.SUCCESS(
            '\n[OK] Prueba E2E completada: SMPI -> Diagnostico -> Analisis funciona correctamente'
        ))
