from django.urls import path
from . import views

app_name = 'simulacros'

urlpatterns = [
    path('', views.lista_simulacros, name='lista_simulacros'),
    path('areas/', views.seleccionar_area, name='seleccionar_area'),
    path('iniciar/<int:simulacro_id>/', views.iniciar_simulacro, name='iniciar_simulacro'),
    path('realizar/<int:intento_id>/', views.realizar_simulacro, name='realizar_simulacro'),
    path('resultado/<int:intento_id>/', views.resultado_simulacro, name='resultado_simulacro'),
]
