from django.utils import timezone

from .models import UserAccess

ELITE_SLUG = 'elite-cnsc-2026'


def _active_access_queryset(user):
    now = timezone.now()
    return UserAccess.objects.filter(user=user, status='active').filter(expires_at__isnull=True) | UserAccess.objects.filter(user=user, status='active', expires_at__gt=now)


def user_has_module_access(user, module):
    if not user.is_authenticated:
        return False
    if user.is_staff or user.is_superuser:
        return True
    if module is None:
        return True

    active_access = _active_access_queryset(user)
    return active_access.filter(module=module).exists() or active_access.filter(module__slug=ELITE_SLUG).exists()


def user_has_full_access(user):
    if not user.is_authenticated:
        return False
    if user.is_staff or user.is_superuser:
        return True
    return _active_access_queryset(user).filter(module__slug=ELITE_SLUG).exists()


def grant_module_access(user, module, access_type='single_purchase', expires_at=None, notes=''):
    access, _ = UserAccess.objects.update_or_create(
        user=user,
        module=module,
        defaults={
            'access_type': 'combo' if module.slug == ELITE_SLUG else access_type,
            'status': 'active',
            'expires_at': expires_at,
            'notes': notes,
        }
    )
    user.estado_pago = 'activo'
    user.modulo_adquirido = module.slug
    user.fecha_expiracion = expires_at
    user.save(update_fields=['estado_pago', 'modulo_adquirido', 'fecha_expiracion'])
    return access


def grant_full_access(user, access_type='combo', expires_at=None, notes=''):
    from academics.models import Module

    elite = Module.objects.get(slug=ELITE_SLUG)
    return grant_module_access(user, elite, access_type=access_type, expires_at=expires_at, notes=notes)
