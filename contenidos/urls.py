from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('modulo/<int:modulo_id>/', views.detalle_modulo, name='detalle_modulo'),
]