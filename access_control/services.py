from django.utils import timezone

from .models import UserAccess

ELITE_SLUG = 'elite-cnsc-2026'


def _active_access_queryset(user):
    now = timezone.now()
    active_no_expiry = UserAccess.objects.filter(user=user, status='active', expires_at__isnull=True)
    active_with_expiry = UserAccess.objects.filter(user=user, status='active', expires_at__gt=now)
    return active_no_expiry | active_with_expiry


def user_has_module_access(user, module):
    if not user.is_authenticated:
        return False
    if user.is_staff or user.is_superuser:
        return True
    if module is None:
        return True
    return _active_access_queryset(user).filter(module__slug=ELITE_SLUG).exists()


def user_has_full_access(user):
    if not user.is_authenticated:
        return False
    if user.is_staff or user.is_superuser:
        return True
    return _active_access_queryset(user).filter(module__slug=ELITE_SLUG).exists()


def grant_module_access(user, module, access_type='combo', expires_at=None, notes=''):
    from academics.models import Module

    elite = module if module.slug == ELITE_SLUG else Module.objects.get(slug=ELITE_SLUG)
    access, _ = UserAccess.objects.update_or_create(
        user=user,
        module=elite,
        defaults={
            'access_type': 'combo',
            'status': 'active',
            'expires_at': expires_at,
            'notes': notes or 'Acceso completo por pago único',
        },
    )
    user.estado_pago = 'activo'
    user.modulo_adquirido = ELITE_SLUG
    user.fecha_expiracion = expires_at
    user.save(update_fields=['estado_pago', 'modulo_adquirido', 'fecha_expiracion'])
    return access


def grant_full_access(user, access_type='combo', expires_at=None, notes=''):
    from academics.models import Module

    elite = Module.objects.get(slug=ELITE_SLUG)
    return grant_module_access(user, elite, access_type=access_type, expires_at=expires_at, notes=notes)