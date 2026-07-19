from django.contrib import admin
from .models import Simulacro


@admin.register(Simulacro)
class SimulacroAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'area', 'module', 'total_preguntas', 'es_premium', 'activo')
    list_filter = ('tipo', 'area', 'es_premium', 'activo')
    search_fields = ('nombre', 'descripcion', 'paquete_codigo')
    filter_horizontal = ('preguntas',)
