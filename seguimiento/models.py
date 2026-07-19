from django.db import models
from django.conf import settings
from simulacros.models import Simulacro
from banco.models import BancoPregunta
from contenidos.models import Modulo


class Intento(models.Model):
    ESTADO_CHOICES = [
        ('en_curso', 'En curso'),
        ('completado', 'Completado'),
        ('abandonado', 'Abandonado'),
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='seguimiento_intentos'
    )
    simulacro = models.ForeignKey(Simulacro, on_delete=models.CASCADE)
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_finalizacion = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='en_curso')
    puntaje_obtenido = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    total_correctas = models.PositiveIntegerField(default=0)
    total_incorrectas = models.PositiveIntegerField(default=0)
    total_sin_responder = models.PositiveIntegerField(default=0)
    tiempo_usado_segundos = models.PositiveIntegerField(default=0)
    reporte_enviado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.usuario} - {self.simulacro} - {self.estado}"


class RespuestaIntento(models.Model):
    intento = models.ForeignKey(
        Intento,
        on_delete=models.CASCADE,
        related_name='respuestas'
    )
    pregunta = models.ForeignKey(
        BancoPregunta,
        on_delete=models.CASCADE,
        related_name='seguimiento_respuestas'
    )
    respuesta_seleccionada = models.CharField(max_length=1, null=True, blank=True)
    es_correcta = models.BooleanField(default=False)
    respondida_en_tiempo = models.BooleanField(default=True)
    tiempo_usado_segundos = models.PositiveIntegerField(default=0)


class ProgresoModulo(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE)
    porcentaje = models.PositiveIntegerField(default=0)
