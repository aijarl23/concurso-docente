from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'order', 'gateway', 'status', 'amount', 'paid_at', 'created_at')
    list_filter = ('gateway', 'status')
    search_fields = ('transaction_id', 'order__reference', 'order__user__email')
