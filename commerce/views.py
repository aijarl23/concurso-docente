from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Case, IntegerField, When
from django.shortcuts import get_object_or_404, redirect, render

from .models import Cart, CartItem, Product

ELITE_SLUG = 'elite-cnsc-2026'


def _active_cart(request):
    cart, _ = Cart.objects.get_or_create(user=request.user, status='active')
    return cart


@login_required
def product_list(request):
    products = (
        Product.objects.select_related('module', 'module__category')
        .filter(active=True, module__is_active=True, module__slug=ELITE_SLUG)
        .annotate(
            sales_order=Case(
                When(module__slug='elite-cnsc-2026', then=0),
                When(module__slug='diagnostico-inicial', then=1),
                When(module__slug='lectura-critica-aplicada', then=2),
                When(module__slug='competencias-pedagogicas', then=3),
                When(module__slug='competencias-comportamentales-tjs', then=4),
                When(module__slug='normativa-contexto-docente', then=5),
                When(module__slug='simulacros-por-area', then=6),
                When(module__slug='simulacro-final-concurso', then=7),
                When(module__slug='reporte-progreso-plan-mejora', then=8),
                default=20,
                output_field=IntegerField(),
            )
        )
        .order_by('sales_order', 'module__title')
    )
    return render(request, 'commerce/product_list.html', {'products': products})


@login_required
def add_to_cart(request, product_id):
    get_object_or_404(Product, id=product_id, active=True)
    product = get_object_or_404(Product, module__slug=ELITE_SLUG, active=True)
    cart = _active_cart(request)
    cart.items.exclude(product=product).delete()
    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': 1, 'unit_price': product.final_price}
    )
    if not created:
        item.quantity = 1
        item.unit_price = product.final_price
        item.save(update_fields=['quantity', 'unit_price'])
    messages.success(request, 'Producto agregado al carrito.')
    return redirect('commerce:cart_detail')


@login_required
def cart_detail(request):
    cart = _active_cart(request)
    items = list(cart.items.select_related('product__module'))
    for item in items:
        if item.quantity != 1 or item.unit_price != item.product.final_price:
            item.quantity = 1
            item.unit_price = item.product.final_price
            item.save(update_fields=['quantity', 'unit_price'])
    total = sum(item.subtotal for item in items)
    return render(request, 'commerce/cart_detail.html', {'cart': cart, 'items': items, 'total': total})


@login_required
def remove_from_cart(request, item_id):
    cart = _active_cart(request)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    item.delete()
    messages.info(request, 'Producto retirado del carrito.')
    return redirect('commerce:cart_detail')


@login_required
def checkout_cart(request):
    from payments.views import _build_order_from_products

    cart = _active_cart(request)
    items = list(cart.items.select_related('product__module'))
    if not items:
        messages.warning(request, 'El carrito esta vacio.')
        return redirect('commerce:product_list')
    elite_product = get_object_or_404(Product, module__slug=ELITE_SLUG, active=True)
    order = _build_order_from_products(request.user, [elite_product])
    cart.status = 'converted'
    cart.save(update_fields=['status'])
    return redirect('payments:checkout_order', order_id=order.id)


