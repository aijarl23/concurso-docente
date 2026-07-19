import secrets
from urllib.parse import urlencode

import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import RegistroForm
from .models import Usuario

GOOGLE_AUTH_URL = 'https://accounts.google.com/o/oauth2/v2/auth'
GOOGLE_TOKEN_URL = 'https://oauth2.googleapis.com/token'
GOOGLE_USERINFO_URL = 'https://www.googleapis.com/oauth2/v3/userinfo'

def google_redirect_uri(request):
    if settings.SITE_PUBLIC_URL:
        return settings.SITE_PUBLIC_URL.rstrip('/') + reverse('google_callback')
    return settings.GOOGLE_OAUTH_REDIRECT_URI or request.build_absolute_uri(reverse('google_callback'))


def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Bienvenido {user.first_name}. Tu cuenta fue creada exitosamente.')
            return redirect('dashboard')
    else:
        form = RegistroForm()
    return render(request, 'usuarios/registro.html', {'form': form})


@login_required
def mi_perfil(request):
    return render(request, 'usuarios/perfil.html', {'usuario': request.user})


def google_login(request):
    client_id = settings.GOOGLE_OAUTH_CLIENT_ID
    client_secret = settings.GOOGLE_OAUTH_CLIENT_SECRET
    redirect_uri = google_redirect_uri(request)
    missing = []
    if not client_id:
        missing.append('GOOGLE_OAUTH_CLIENT_ID')
    if not client_secret:
        missing.append('GOOGLE_OAUTH_CLIENT_SECRET')
    if not redirect_uri:
        missing.append('GOOGLE_OAUTH_REDIRECT_URI')
    if missing:
        messages.error(request, 'Google OAuth requiere configurar en .env: ' + ', '.join(missing) + '.')
        return redirect('login')

    state = secrets.token_urlsafe(24)
    request.session['google_oauth_state'] = state
    params = {
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'response_type': 'code',
        'scope': 'openid email profile',
        'state': state,
        'access_type': 'online',
        'prompt': 'select_account',
    }
    response = redirect(f'{GOOGLE_AUTH_URL}?{urlencode(params)}')
    response.set_signed_cookie(
        'google_oauth_state',
        state,
        max_age=600,
        httponly=True,
        secure=not settings.DEBUG,
        samesite='Lax',
    )
    return response


def google_callback(request):
    expected_state = request.session.pop('google_oauth_state', None)
    if not expected_state:
        try:
            expected_state = request.get_signed_cookie('google_oauth_state', max_age=600)
        except Exception:
            expected_state = None
    if not expected_state or request.GET.get('state') != expected_state:
        messages.error(request, 'No se pudo validar la respuesta de Google. Intenta nuevamente.')
        response = redirect('login')
        response.delete_cookie('google_oauth_state')
        return response

    code = request.GET.get('code')
    if not code:
        messages.error(request, 'Google no devolvio un codigo de autorizacion valido.')
        response = redirect('login')
        response.delete_cookie('google_oauth_state')
        return response

    redirect_uri = google_redirect_uri(request)
    token_response = requests.post(
        GOOGLE_TOKEN_URL,
        data={
            'code': code,
            'client_id': settings.GOOGLE_OAUTH_CLIENT_ID,
            'client_secret': settings.GOOGLE_OAUTH_CLIENT_SECRET,
            'redirect_uri': redirect_uri,
            'grant_type': 'authorization_code',
        },
        timeout=20,
    )
    if token_response.status_code != 200:
        messages.error(request, 'Google rechazo el intercambio de credenciales. Revisa client_id, secret y redirect_uri.')
        response = redirect('login')
        response.delete_cookie('google_oauth_state')
        return response

    access_token = token_response.json().get('access_token')
    user_response = requests.get(
        GOOGLE_USERINFO_URL,
        headers={'Authorization': f'Bearer {access_token}'},
        timeout=20,
    )
    if user_response.status_code != 200:
        messages.error(request, 'No fue posible obtener el perfil de Google.')
        response = redirect('login')
        response.delete_cookie('google_oauth_state')
        return response

    profile = user_response.json()
    email = (profile.get('email') or '').strip().lower()
    uid = (profile.get('sub') or '').strip()
    if not email or not uid:
        messages.error(request, 'El perfil de Google no entrego correo o uid.')
        response = redirect('login')
        response.delete_cookie('google_oauth_state')
        return response

    user = Usuario.objects.filter(uid=uid).order_by('id').first()
    if user is None:
        user = Usuario.objects.filter(email__iexact=email).order_by('id').first()
    if user is None:
        user = Usuario(email=email)

    base_username = (email.split('@')[0] or 'google_user').replace(' ', '_')
    username = user.username or base_username
    counter = 1
    while Usuario.objects.filter(username=username).exclude(id=user.id).exists():
        counter += 1
        username = f'{base_username}{counter}'

    user.username = username
    user.email = email
    user.first_name = profile.get('given_name', '') or user.first_name
    user.last_name = profile.get('family_name', '') or user.last_name
    user.uid = uid
    user.oauth_provider = 'google'
    user.auth_email_verified = bool(profile.get('email_verified'))
    user.is_active = True
    user.save()
    login(request, user)
    messages.success(request, f'Bienvenido {user.nombre}.')
    response = redirect(settings.LOGIN_REDIRECT_URL)
    response.delete_cookie('google_oauth_state')
    return response
