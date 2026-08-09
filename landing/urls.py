from django.urls import path
from . import views

app_name = 'landing'

urlpatterns = [
    path('terminos/', views.terminos, name='terminos'),
    path('privacidad/', views.privacidad, name='privacidad'),
    path('reembolsos/', views.reembolsos, name='reembolsos'),
]
