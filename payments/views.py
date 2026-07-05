import json
import uuid
from decimal import Decimal

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache

from access_control.services import grant_module_access
from commerce.models import Cart, Order, OrderItem, Product
from payments.models import Payment
from payments.services import WompiService, send_purchase_confirmation


def _mark_order_approved(order, transaction_id, raw_response, notes):
    order.status = 'paid'
    order.save(update_fields=['status'])
    Payment.objects.update_or_create(
        transaction_id=transaction_id,
        defaults={
            'order': order,
            'status': 'approved',
            'amount': order.total,
            'currency': order.currency,
            'gateway': 'wompi',
            'raw_response': raw_response,
            'paid_at': timezone.now(),
        }
    )
    for item in order.items.select_related('module'):
        grant_module_access(order.user, item.module, notes=notes)
    send_purchase_confirmation(order)


def _mark_order_failed(order, transaction_id, status, raw_response):
    order.status = 'failed'
    order.save(update_fields=['status'])
    Payment.objects.update_or_create(
        transaction_id=transaction_id,
        defaults={
            'order': order,
            'status': status,
            'amount': order.total,
            'currency': order.currency,
            'gateway': 'wompi',
            'raw_response': raw_response,
            'paid_at': None,
        }
    )
    order.user.estado_pago = 'rechazado'
    order.user.save(update_fields=['estado_pago'])


def _build_order_from_products(user, products):
    reference = f"CNSC-{uuid.uuid4().hex[:12].upper()}"
    total = sum(Decimal(product.final_price) for product in products)
    order = Order.objects.create(
        user=user,
        reference=reference,
        status='pending',
        subtotal=total,
        total=total,
        currency='COP',
    )
    for product in products:
        OrderItem.objects.create(order=order, module=product.module, price=product.final_price)
    user.estado_pago = 'pendiente'
    user.save(update_fields=['estado_pago'])
    return order


@login_required
def buy_module(request, product_id):
    product = get_object_or_404(Product.objects.select_related('module'), id=product_id, active=True)
    order = _build_order_from_products(request.user, [product])
    return redirect('payments:checkout_order', order_id=order.id)


@never_cache
@login_required
def checkout_order(request, order_id):
    order = get_object_or_404(Order.objects.prefetch_related('items__module'), id=order_id, user=request.user)
    amount_in_cents = int(order.total * 100)
    acceptance_token = ''
    wompi_error = ''
    payment_config_errors = []

    if not settings.WOMPI_PUBLIC_KEY:
        payment_config_errors.append('Falta WOMPI_PUBLIC_KEY en .env.')
    if not settings.WOMPI_PRIVATE_KEY:
        payment_config_errors.append('Falta WOMPI_PRIVATE_KEY en .env.')

    public_key = settings.WOMPI_PUBLIC_KEY.strip()
    base_url = settings.WOMPI_BASE_URL.strip().lower()
    current_host = request.get_host().split(':')[0].lower()
    is_local_request = current_host in {'127.0.0.1', 'localhost'}
    if public_key.startswith('pub_prod_') and 'sandbox' in base_url:
        payment_config_errors.append('La llave publica es de produccion (pub_prod_) pero WOMPI_BASE_URL apunta a sandbox. Usa https://production.wompi.co/v1.')
    if public_key.startswith('pub_test_') and 'production' in base_url:
        payment_config_errors.append('La llave publica es de pruebas (pub_test_) pero WOMPI_BASE_URL apunta a produccion. Usa https://sandbox.wompi.co/v1.')
    if public_key.startswith('pub_prod_') and is_local_request:
        payment_config_errors.append('Estas usando Wompi de produccion desde 127.0.0.1. Para cobro real abre la plataforma desde un dominio publico HTTPS o un tunel HTTPS y configura SITE_PUBLIC_URL. En localhost el modal de produccion puede quedarse procesando.')
    if not settings.WOMPI_INTEGRITY_SECRET:
        payment_config_errors.append('Falta WOMPI_INTEGRITY_SECRET en .env. Sin esta llave Wompi no renderiza correctamente el checkout firmado.')
    if not request.user.email:
        payment_config_errors.append('El usuario no tiene correo asociado para el checkout.')

    signature = ''
    if not payment_config_errors:
        signature = WompiService.transaction_signature(order.reference, amount_in_cents, order.currency)
        try:
            acceptance_token = WompiService.get_acceptance_token()
        except Exception as exc:
            wompi_error = str(exc)

    context = {
        'order': order,
        'public_key': settings.WOMPI_PUBLIC_KEY,
        'acceptance_token': acceptance_token,
        'amount_in_cents': amount_in_cents,
        'reference': order.reference,
        'email': request.user.email,
        'customer_full_name': request.user.get_full_name() or request.user.username or request.user.email,
        'currency': order.currency,
        'signature': signature,
        'redirect_url': (settings.SITE_PUBLIC_URL + reverse('payments:payment_return', args=[order.id])) if settings.SITE_PUBLIC_URL else request.build_absolute_uri(reverse('payments:payment_return', args=[order.id])),
        'wompi_error': wompi_error,
        'payment_config_errors': payment_config_errors,
        'enable_local_payment_approval': settings.ENABLE_LOCAL_PAYMENT_APPROVAL,
    }
    return render(request, 'payments/checkout.html', context)


@login_required
def approve_order_dev(request, order_id):
    if not settings.ENABLE_LOCAL_PAYMENT_APPROVAL:
        return HttpResponseForbidden('Aprobacion local deshabilitada')
    order = get_object_or_404(Order.objects.prefetch_related('items__module'), id=order_id, user=request.user)
    _mark_order_approved(order, f'DEV-{order.reference}', {'mode': 'debug'}, 'Aprobacion local DEBUG')
    messages.success(request, 'Pago de prueba aprobado y acceso premium habilitado.')
    return redirect('simulacros:lista_simulacros')


@csrf_exempt
def wompi_webhook(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Metodo no permitido'}, status=405)

    try:
        payload = json.loads(request.body.decode('utf-8'))
        if not WompiService.validate_event(payload, request.headers.get('X-Event-Signature')):
            return JsonResponse({'error': 'Firma invalida'}, status=403)

        transaction = payload.get('data', {}).get('transaction', {})
        reference = transaction.get('reference')
        transaction_id = transaction.get('id')
        status = (transaction.get('status') or '').lower()
        if not reference or not transaction_id:
            return JsonResponse({'error': 'Payload invalido'}, status=400)

        order = Order.objects.get(reference=reference)
        if status == 'approved':
            _mark_order_approved(order, transaction_id, payload, 'Webhook Wompi aprobado')
        elif status in {'declined', 'voided', 'error'}:
            _mark_order_failed(order, transaction_id, status, payload)
        else:
            Payment.objects.update_or_create(
                transaction_id=transaction_id,
                defaults={
                    'order': order,
                    'status': status or 'pending',
                    'amount': order.total,
                    'currency': order.currency,
                    'gateway': 'wompi',
                    'raw_response': payload,
                    'paid_at': None,
                }
            )

        return JsonResponse({'status': 'ok'})
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Orden no encontrada'}, status=404)
    except Exception as exc:
        return JsonResponse({'error': str(exc)}, status=400)


@login_required
def payment_return(request, order_id):
    order = get_object_or_404(Order.objects.prefetch_related('items__module'), id=order_id, user=request.user)
    transaction_id = request.GET.get('id') or request.GET.get('transaction_id')
    status = request.GET.get('status', '').lower()
    verify_error = ''

    if transaction_id and order.status != 'paid':
        try:
            transaction = WompiService.get_transaction(transaction_id)
            reference = transaction.get('reference')
            transaction_status = (transaction.get('status') or status).lower()
            if reference and reference != order.reference:
                verify_error = 'La referencia de Wompi no coincide con la orden.'
            elif transaction_status == 'approved':
                _mark_order_approved(order, transaction_id, transaction, 'Retorno Wompi verificado')
                messages.success(request, 'Pago aprobado. Tu acceso premium fue habilitado.')
            elif transaction_status in {'declined', 'voided', 'error'}:
                _mark_order_failed(order, transaction_id, transaction_status, transaction)
                messages.error(request, 'El pago fue rechazado o no pudo completarse.')
            else:
                Payment.objects.update_or_create(
                    transaction_id=transaction_id,
                    defaults={
                        'order': order,
                        'status': transaction_status or 'pending',
                        'amount': order.total,
                        'currency': order.currency,
                        'gateway': 'wompi',
                        'raw_response': transaction,
                        'paid_at': None,
                    }
                )
                messages.info(request, 'El pago quedo pendiente de confirmacion.')
        except Exception as exc:
            verify_error = str(exc)

    order.refresh_from_db()
    return render(request, 'payments/payment_return.html', {
        'order': order,
        'transaction_id': transaction_id,
        'verify_error': verify_error,
    })
