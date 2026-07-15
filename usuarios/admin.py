from django.contrib import admin
from django.contrib import messages
from django.contrib.auth.admin import UserAdmin

from access_control.services import grant_full_access
from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'area_concurso',
        'estado_pago',
        'modulo_adquirido',
        'entidad_territorial',
        'is_staff',
    )
    list_filter = ('area_concurso', 'estado_pago', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    actions = ('habilitar_acceso_completo_prueba',)

    fieldsets = UserAdmin.fieldsets + (
        ('Datos del concurso', {
            'fields': ('area_concurso', 'entidad_territorial', 'meta_puntaje')
        }),
        ('Acceso premium', {
            'fields': ('estado_pago', 'modulo_adquirido', 'fecha_expiracion'),
            'description': (
                'Para usuarios de prueba, use la accion masiva '
                'Habilitar acceso completo de prueba sin pago desde el listado de usuarios.'
            ),
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Datos del concurso', {
            'fields': ('area_concurso', 'entidad_territorial', 'meta_puntaje')
        }),
    )

    @admin.action(description='Habilitar acceso completo de prueba sin pago')
    def habilitar_acceso_completo_prueba(self, request, queryset):
        total = 0
        for user in queryset:
            grant_full_access(
                user,
                access_type='admin_granted',
                notes='Acceso completo asignado manualmente desde el admin para pruebas.',
            )
            total += 1

        self.message_user(
            request,
            f'Acceso completo habilitado para {total} usuario(s).',
            messages.SUCCESS,
        )
