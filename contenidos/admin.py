from django.contrib import admin
from .models import Modulo, Tema


class TemaInline(admin.TabularInline):
    model = Tema
    extra = 0
    fields = ('orden', 'titulo', 'activo')
    ordering = ('orden',)


@admin.register(Modulo)
class ModuloAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tipo', 'orden', 'activo')
    list_filter = ('activo', 'tipo')
    search_fields = ('titulo', 'descripcion')
    ordering = ('orden',)
    inlines = [TemaInline]


@admin.register(Tema)
class TemaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'modulo', 'orden', 'activo')
    list_filter = ('activo', 'modulo')
    search_fields = ('titulo', 'descripcion')
    ordering = ('modulo', 'orden')
