from django.contrib import admin
from .models import Intento, RespuestaIntento, ProgresoModulo


class RespuestaIntentoInline(admin.TabularInline):
    model = RespuestaIntento
    extra = 0
    fields = ('pregunta', 'respuesta_seleccionada', 'es_correcta', 'respondida_en_tiempo')
    readonly_fields = ('pregunta', 'respuesta_seleccionada', 'es_correcta', 'respondida_en_tiempo')
    can_delete = False
    show_change_link = True


@admin.register(Intento)
class IntentoAdmin(admin.ModelAdmin):
    list_display = (
        'usuario', 'simulacro', 'estado', 'puntaje_obtenido',
        'total_correctas', 'total_incorrectas', 'total_sin_responder',
        'reporte_enviado', 'fecha_inicio', 'fecha_finalizacion',
    )
    list_filter = ('estado', 'reporte_enviado', 'simulacro')
    search_fields = ('usuario__username', 'usuario__email', 'simulacro__nombre')
    date_hierarchy = 'fecha_inicio'
    autocomplete_fields = ('usuario', 'simulacro')
    inlines = [RespuestaIntentoInline]


@admin.register(RespuestaIntento)
class RespuestaIntentoAdmin(admin.ModelAdmin):
    list_display = ('intento', 'pregunta', 'respuesta_seleccionada', 'es_correcta', 'respondida_en_tiempo')
    list_filter = ('es_correcta', 'respondida_en_tiempo')
    search_fields = ('intento__usuario__username', 'pregunta__enunciado')
    autocomplete_fields = ('intento', 'pregunta')


@admin.register(ProgresoModulo)
class ProgresoModuloAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'modulo', 'porcentaje')
    list_filter = ('modulo',)
    search_fields = ('usuario__username', 'usuario__email', 'modulo__titulo')
    autocomplete_fields = ('usuario', 'modulo')
