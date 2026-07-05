from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import Cart, CartItem, Product


def _active_cart(request):
    cart, _ = Cart.objects.get_or_create(user=request.user, status='active')
    return cart


@login_required
def product_list(request):
    products = Product.objects.select_related('module', 'module__category').filter(active=True, module__is_active=True)
    return render(request, 'commerce/product_list.html', {'products': products})


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id, active=True)
    cart = _active_cart(request)
    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': 1, 'unit_price': product.final_price}
    )
    if not created:
        item.quantity += 1
        item.unit_price = product.final_price
        item.save(update_fields=['quantity', 'unit_price'])
    messages.success(request, 'Producto agregado al carrito.')
    return redirect('commerce:cart_detail')


@login_required
def cart_detail(request):
    cart = _active_cart(request)
    items = cart.items.select_related('product__module')
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
    products = [item.product for item in items]
    order = _build_order_from_products(request.user, products)
    cart.status = 'converted'
    cart.save(update_fields=['status'])
    return redirect('payments:checkout_order', order_id=order.id)
