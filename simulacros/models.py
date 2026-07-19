from django.db import models
from academics.models import Module
from banco.models import BancoPregunta


class Simulacro(models.Model):
    TIPOS = [
        ('simulacro', 'Simulacro'),
        ('diagnostico', 'Diagnostico'),
        ('tematico', 'Tematico'),
        ('tjs', 'TJS Premium'),
        ('elite', 'CNSC Elite'),
        ('area', 'Simulacro por área'),
    ]

    AREA_CHOICES = BancoPregunta.AREA_CHOICES

    nombre = models.CharField(max_length=250)
    descripcion = models.TextField()
    tipo = models.CharField(max_length=20, choices=TIPOS, default='simulacro')
    module = models.ForeignKey(
        Module,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='simulacros'
    )
    area = models.CharField(max_length=40, choices=AREA_CHOICES, default='general')
    tiempo_limite_minutos = models.PositiveIntegerField(default=120)
    tiempo_por_pregunta_segundos = models.PositiveIntegerField(default=120)
    puntaje_minimo_aprobacion = models.PositiveIntegerField(default=70)
    es_premium = models.BooleanField(default=True)
    paquete_codigo = models.CharField(max_length=80, blank=True)
    activo = models.BooleanField(default=True)
    preguntas = models.ManyToManyField(BancoPregunta, related_name='simulacros')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['nombre']

    @property
    def total_preguntas(self):
        return self.preguntas.count()

    def __str__(self):
        return self.nombre
