from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('buy/<int:product_id>/', views.buy_module, name='buy_module'),
    path('checkout/<int:order_id>/', views.checkout_order, name='checkout_order'),
    path('return/<int:order_id>/', views.payment_return, name='payment_return'),
    path('dev/approve/<int:order_id>/', views.approve_order_dev, name='approve_order_dev'),
    path('webhook/', views.wompi_webhook, name='wompi_webhook'),
]
