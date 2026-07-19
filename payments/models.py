from django.db import models
from commerce.models import Order


class Payment(models.Model):
    GATEWAY_CHOICES = [
        ('wompi', 'Wompi'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('approved', 'Aprobado'),
        ('declined', 'Rechazado'),
        ('failed', 'Fallido'),
        ('cancelled', 'Cancelado'),
    ]

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='payments'
    )

    gateway = models.CharField(
        max_length=20,
        choices=GATEWAY_CHOICES,
        default='wompi'
    )

    transaction_id = models.CharField(
        max_length=255,
        unique=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    currency = models.CharField(
        max_length=10,
        default='COP'
    )

    raw_response = models.JSONField(
        null=True,
        blank=True
    )

    paid_at = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Pago'
        verbose_name_plural = 'Pagos'

    def __str__(self):
        return f"{self.order.reference} - {self.status}"