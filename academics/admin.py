from django.contrib import admin
from .models import Category, Module, NormativeResource


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category_type', 'active', 'order')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'category',
        'difficulty_level',
        'is_active',
        'is_premium'
    )
    list_filter = ('category', 'difficulty_level', 'is_active')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(NormativeResource)
class NormativeResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'reference', 'active')