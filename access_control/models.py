from django.conf import settings
from django.db import models

from academics.models import Module


class UserAccess(models.Model):
    ACCESS_TYPES = [
        ('combo', 'Acceso completo'),
        ('admin_granted', 'Asignado manualmente'),
    ]

    STATUS_CHOICES = [
        ('active', 'Activo'),
        ('expired', 'Expirado'),
        ('revoked', 'Revocado'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='module_accesses',
    )
    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name='user_accesses',
    )
    access_type = models.CharField(max_length=30, choices=ACCESS_TYPES, default='combo')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    granted_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ('user', 'module')
        verbose_name = 'Acceso usuario'
        verbose_name_plural = 'Accesos usuarios'

    def __str__(self):
        return f'{self.user.username} -> {self.module.title}'