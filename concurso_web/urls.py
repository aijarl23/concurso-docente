from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('contenidos.urls')),
    path('simulacros/', include('simulacros.urls')),
    path('progreso/', include('seguimiento.urls')),
    path('cuentas/', include('usuarios.urls')),
    path('payments/', include('payments.urls')),
    path('tienda/', include('commerce.urls')),
    path('cuentas/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('cuentas/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path(
        'cuentas/recuperar/',
        auth_views.PasswordResetView.as_view(
            template_name='registration/password_reset_form.html',
            email_template_name='registration/password_reset_email.html',
            subject_template_name='registration/password_reset_subject.txt',
            success_url='/cuentas/recuperar/enviado/',
        ),
        name='password_reset',
    ),
    path(
        'cuentas/recuperar/enviado/',
        auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
        name='password_reset_done',
    ),
    path(
        'cuentas/recuperar/confirmar/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='registration/password_reset_confirm.html',
            success_url='/cuentas/recuperar/completo/',
        ),
        name='password_reset_confirm',
    ),
    path(
        'cuentas/recuperar/completo/',
        auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
        name='password_reset_complete',
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
