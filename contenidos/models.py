from django.db import models


class Modulo(models.Model):
    TIPOS = [
        ('lectura_tjs', 'Lectura Crítica'),
        ('perfil_docente', 'Rol Docente'),
        ('pedagogico', 'Competencias Pedagógicas'),
        ('psicotecnico', 'Análisis de Casos'),
    ]

    titulo = models.CharField(max_length=200)
    tipo = models.CharField(max_length=30, choices=TIPOS, unique=True)
    descripcion = models.TextField()
    orden = models.PositiveIntegerField(default=1)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ['orden']

    def __str__(self):
        return self.titulo


class Tema(models.Model):
    modulo = models.ForeignKey(
        Modulo,
        on_delete=models.CASCADE,
        related_name='temas'
    )

    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    orden = models.PositiveIntegerField(default=1)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ['orden']

    def __str__(self):
        return self.titulo
