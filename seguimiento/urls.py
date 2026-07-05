from django.urls import path
from . import views

urlpatterns = [
    path('', views.mi_progreso, name='mi_progreso'),
]