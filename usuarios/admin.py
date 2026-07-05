from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'area_concurso', 'entidad_territorial', 'is_staff')
    list_filter = ('area_concurso', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    
    fieldsets = UserAdmin.fieldsets + (
        ('Datos del concurso', {
            'fields': ('area_concurso', 'entidad_territorial', 'meta_puntaje')
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Datos del concurso', {
            'fields': ('area_concurso', 'entidad_territorial', 'meta_puntaje')
        }),
    )