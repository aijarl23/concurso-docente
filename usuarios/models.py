from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    """Usuario extendido con datos del concurso docente y acceso premium."""

    AREA_CHOICES = [
        ('matematicas', 'Matematicas'),
        ('lenguaje', 'Lenguaje'),
        ('ciencias_naturales', 'Ciencias Naturales'),
        ('ciencias_sociales', 'Ciencias Sociales'),
        ('ingles', 'Ingles'),
        ('preescolar', 'Preescolar'),
        ('primaria', 'Primaria'),
        ('educacion_fisica', 'Educacion Fisica'),
        ('artistica', 'Educacion Artistica'),
        ('tecnologia', 'Tecnologia e Informatica'),
        ('otro', 'Otro'),
    ]

    ESTADO_PAGO_CHOICES = [
        ('sin_pago', 'Sin pago'),
        ('pendiente', 'Pendiente'),
        ('activo', 'Activo'),
        ('expirado', 'Expirado'),
        ('rechazado', 'Rechazado'),
    ]

    area_concurso = models.CharField(
        max_length=30,
        choices=AREA_CHOICES,
        default='otro',
        verbose_name='Area del concurso'
    )
    entidad_territorial = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Entidad territorial'
    )
    meta_puntaje = models.PositiveIntegerField(
        default=80,
        verbose_name='Meta de puntaje (0-100)'
    )
    uid = models.CharField(max_length=160, blank=True, db_index=True)
    oauth_provider = models.CharField(max_length=40, blank=True)
    auth_email_verified = models.BooleanField(default=False)
    estado_pago = models.CharField(
        max_length=20,
        choices=ESTADO_PAGO_CHOICES,
        default='sin_pago'
    )
    modulo_adquirido = models.CharField(max_length=120, blank=True)
    fecha_expiracion = models.DateTimeField(null=True, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    @property
    def nombre(self):
        return self.get_full_name() or self.username

    def __str__(self):
        return f"{self.nombre} - {self.get_area_concurso_display()}"
