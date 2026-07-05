import json
from django.core.management.base import BaseCommand
from evaluaciones.models import Pregunta
from contenidos.models import Tema


class Command(BaseCommand):
    help = 'Importar preguntas CNSC desde JSON'

    def handle(self, *args, **kwargs):
        with open('preguntas_cnsc.json', 'r', encoding='utf-8') as f:
            preguntas = json.load(f)

        creadas = 0

        for item in preguntas:
            tema, _ = Tema.objects.get_or_create(
                nombre=item["tema"]
            )

            Pregunta.objects.create(
                tema=tema,
                componente='normativo',
                dificultad='alta',
                contexto=item["contexto"],
                enunciado=item["enunciado"],
                opcion_a=item["opcion_a"],
                opcion_b=item["opcion_b"],
                opcion_c=item["opcion_c"],
                opcion_d=item["opcion_d"],
                respuesta_correcta=item["respuesta_correcta"],
                justificacion=item["justificacion"],
                fuente_normativa=item["fuente_normativa"],
                activa=True
            )

            creadas += 1

        self.stdout.write(
            self.style.SUCCESS(f'{creadas} preguntas importadas correctamente')
        )