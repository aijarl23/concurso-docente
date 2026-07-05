from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_simulacros, name='lista_simulacros'),
    path('<int:simulacro_id>/iniciar/', views.iniciar_simulacro, name='iniciar_simulacro'),
    path('intento/<int:intento_id>/', views.realizar_simulacro, name='realizar_simulacro'),
    path('intento/<int:intento_id>/resultado/', views.resultado_simulacro, name='resultado_simulacro'),
]
