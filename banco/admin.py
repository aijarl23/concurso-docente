from django.contrib import admin
from .models import Categoria, Subcategoria, BancoPregunta


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    search_fields = ('nombre',)


@admin.register(Subcategoria)
class SubcategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria')
    list_filter = ('categoria',)
    search_fields = ('nombre', 'categoria__nombre')


@admin.register(BancoPregunta)
class BancoPreguntaAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'categoria', 'subcategoria', 'area', 'competencia', 'nivel_dificultad', 'hash_contenido', 'activa')
    list_filter = ('categoria', 'subcategoria', 'area', 'nivel_dificultad', 'dificultad', 'es_premium', 'activa')
    search_fields = ('titulo', 'contexto', 'enunciado', 'competencia', 'hash_contenido')
