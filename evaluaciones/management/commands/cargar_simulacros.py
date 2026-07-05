from django.core.management.base import BaseCommand
from evaluaciones.models import Simulacro, Pregunta


SIMULACROS = [
    {
        "nombre": "Simulacro 1 - Modelos Pedagogicos",
        "descripcion": "Preguntas sobre modelos pedagogicos",
        "sesiones": [1],
    },
    {
        "nombre": "Simulacro 2 - Evaluacion y Curriculo",
        "descripcion": "Preguntas sobre evaluacion y curriculo",
        "sesiones": [2, 3],
    },
    {
        "nombre": "Simulacro 3 - Estrategias Didacticas Activas",
        "descripcion": "Preguntas sobre estrategias didacticas activas",
        "sesiones": [4, 5],
    },
    {
        "nombre": "Simulacro 4 - Completo",
        "descripcion": "Simulacro completo con todas las sesiones",
        "sesiones": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    },
]


class Command(BaseCommand):
    help = 'Crea simulacros y asigna preguntas por sesion automaticamente'

    def handle(self, *args, **kwargs):
        for data in SIMULACROS:
            simulacro, created = Simulacro.objects.get_or_create(
                nombre=data["nombre"],
                defaults={"descripcion": data["descripcion"]}
            )

            if not created:
                self.stdout.write(self.style.WARNING(
                    f'Ya existe: {simulacro.nombre} - actualizando preguntas...'
                ))

            preguntas = Pregunta.objects.filter(sesion__numero__in=data["sesiones"])

            if not preguntas.exists():
                self.stdout.write(self.style.ERROR(
                    f'Sin preguntas para sesiones {data["sesiones"]}'
                ))
                continue

            simulacro.preguntas.set(preguntas)
            simulacro.save()

            self.stdout.write(self.style.SUCCESS(
                f'OK: {simulacro.nombre} - {preguntas.count()} preguntas asignadas'
            ))