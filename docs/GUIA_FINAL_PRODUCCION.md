# Guia final de cierre - ConcursoDocente CNSC 2026

Proyecto real: `C:\ConcursoDocente`.

## Estado local resuelto

- Google OAuth funciona con las variables de `.env`.
- Login local alternativo funciona.
- Dashboard, modulo 2, simulacros, simulacros por area, tienda, carrito, perfil y progreso responden correctamente.
- Banco premium cargado: 375 preguntas.
- Simulacros activos: 18.
- Simulacros por area: 5.
- Productos activos: 12.
- Pago local DEBUG habilita acceso premium y envia correo por consola.

## Paso 1 - Rotar secreto de Google

Debes hacerlo porque el secreto fue compartido en chat. No es una recomendacion opcional.

1. Entra a Google Cloud Console con `jarlontech@gmail.com`.
2. Abre el proyecto `ConcursoDocente CNSC 2026-2027`.
3. Ve a `Google Auth Platform > Clientes`.
4. Abre el cliente web `ConcursoDocente Local`.
5. En `Secretos del cliente`, crea un secreto nuevo.
6. Copia el nuevo secreto una sola vez.
7. Pega el nuevo valor en `C:\ConcursoDocente\.env`:

```env
GOOGLE_OAUTH_CLIENT_SECRET=pega_aqui_el_nuevo_secret
```

8. Borra o deshabilita el secreto viejo.
9. Reinicia el servidor:

```powershell
cd C:\ConcursoDocente
.\start-server.ps1
```

## Paso 2 - Google OAuth local

En el cliente OAuth de Google deben quedar estos valores:

Origenes autorizados de JavaScript:

```text
http://127.0.0.1:8001
http://localhost:8001
```

URI de redireccionamiento autorizado:

```text
http://127.0.0.1:8001/cuentas/google/callback/
```

En `.env`:

```env
GOOGLE_OAUTH_CLIENT_ID=tu_client_id.apps.googleusercontent.com
GOOGLE_OAUTH_CLIENT_SECRET=tu_secret_vigente
GOOGLE_OAUTH_REDIRECT_URI=http://127.0.0.1:8001/cuentas/google/callback/
```

## Paso 3 - Google OAuth produccion

Cuando tengas dominio real, por ejemplo `https://concursodocente.com`, agrega en Google:

Origen autorizado:

```text
https://concursodocente.com
```

Redirect URI:

```text
https://concursodocente.com/cuentas/google/callback/
```

Y cambia `.env` de produccion:

```env
DEBUG=False
ALLOWED_HOSTS=concursodocente.com,www.concursodocente.com
CSRF_TRUSTED_ORIGINS=https://concursodocente.com,https://www.concursodocente.com
CSRF_COOKIE_SECURE=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SAMESITE=Lax
SESSION_COOKIE_SAMESITE=Lax
GOOGLE_OAUTH_REDIRECT_URI=https://concursodocente.com/cuentas/google/callback/
```

## Aclaracion importante sobre pagos locales

El boton `Aprobar pago de prueba local` no es un pago real. Es una herramienta de desarrollo y queda apagada por defecto. Solo aparece si defines:

```env
ENABLE_LOCAL_PAYMENT_APPROVAL=True
```

Para flujo real, deja esa variable en `False` y configura Wompi.

## Requisito para Wompi real

Wompi de produccion no debe probarse como cobro real desde `127.0.0.1`. Para cobrar de verdad necesitas abrir la plataforma desde una URL publica HTTPS. Puede ser un dominio final o un tunel HTTPS temporal.

Cuando tengas esa URL, define:

```env
SITE_PUBLIC_URL=https://TU_DOMINIO_O_TUNEL
ALLOWED_HOSTS=TU_DOMINIO_O_TUNEL
CSRF_TRUSTED_ORIGINS=https://TU_DOMINIO_O_TUNEL
```

El webhook de Wompi debe ser:

```text
https://TU_DOMINIO_O_TUNEL/payments/webhook/
```

## Paso 4 - Wompi real

Para local se puede usar sandbox. Para cobrar dinero real necesitas llaves de produccion de Wompi.

En `.env` local sandbox:

```env
WOMPI_BASE_URL=https://sandbox.wompi.co/v1
WOMPI_PUBLIC_KEY=pub_test_xxxxx
WOMPI_PRIVATE_KEY=prv_test_xxxxx
WOMPI_EVENTS_SECRET=event_secret_xxxxx
WOMPI_INTEGRITY_SECRET=integrity_secret_xxxxx
ENABLE_LOCAL_PAYMENT_APPROVAL=False
```

En produccion:

```env
WOMPI_BASE_URL=https://production.wompi.co/v1
WOMPI_PUBLIC_KEY=pub_prod_xxxxx
WOMPI_PRIVATE_KEY=prv_prod_xxxxx
WOMPI_EVENTS_SECRET=event_secret_prod_xxxxx
WOMPI_INTEGRITY_SECRET=integrity_secret_prod_xxxxx
```

Webhook que debes registrar en Wompi:

```text
https://TU_DOMINIO/payments/webhook/
```

## Paso 5 - Correo real

Ahora el correo local imprime en consola. Para enviar correos reales configura SMTP, SendGrid o Resend.

Ejemplo SMTP:

```env
DEFAULT_FROM_EMAIL=soporte@tudominio.com
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.tudominio.com
EMAIL_PORT=587
EMAIL_HOST_USER=soporte@tudominio.com
EMAIL_HOST_PASSWORD=tu_password_o_api_key
EMAIL_USE_TLS=True
```

## Paso 6 - Verificacion final

Ejecuta:

```powershell
cd C:\ConcursoDocente
venv\Scripts\python.exe manage.py check
venv\Scripts\python.exe manage.py check_premium_ready
.\start-server.ps1
```

Abre:

```text
http://127.0.0.1:8001/
```

Prueba este orden:

1. Iniciar sesion con Google.
2. Abrir `Simulacros`.
3. Abrir `Por area`.
4. Entrar a `Tienda`.
5. Agregar producto al carrito.
6. Ir a checkout.
7. En local DEBUG usar `Aprobar pago de prueba local`.
8. Volver a simulacros y abrir uno premium.
9. Finalizar simulacro y revisar el correo en consola o SMTP.

## Criterio de cierre

La aplicacion se considera lista localmente cuando:

- `manage.py check` no muestra errores.
- `check_premium_ready` no reporta faltantes criticos para el entorno objetivo.
- Google permite entrar y crea/actualiza usuario.
- El carrito crea orden.
- Wompi o aprobacion DEBUG cambia el usuario a `estado_pago=activo`.
- Un simulacro premium abre con 30 preguntas y temporizador.
- Al finalizar simulacro se genera reporte y se envia correo.
