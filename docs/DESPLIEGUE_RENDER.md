# Despliegue en Render - ConcursoDocente

## Recomendacion tecnica
Publica esta plataforma en Render con PostgreSQL administrado. Es la opcion mas directa para Django, HTTPS, dominio publico y webhooks de Wompi.

## 1. Subir el proyecto a GitHub
Desde `C:\ConcursoDocente`:

```powershell
git init
git add .
git commit -m "Preparar despliegue Render"
git branch -M main
git remote add origin URL_DE_TU_REPOSITORIO
git push -u origin main
```

No subas `.env`, `db.sqlite3`, `venv/` ni `staticfiles/`; ya estan protegidos por `.gitignore`.

## 2. Crear el servicio en Render
1. Entra a Render.
2. New > Blueprint.
3. Conecta el repositorio de GitHub.
4. Render detectara `render.yaml` y creara:
   - Web service `concurso-docente`.
   - PostgreSQL `concurso-docente-db`.

## 3. Variables obligatorias en Render
Cuando Render cree el servicio, completa estas variables:

```env
ALLOWED_HOSTS=tu-app.onrender.com
CSRF_TRUSTED_ORIGINS=https://tu-app.onrender.com
SITE_PUBLIC_URL=https://tu-app.onrender.com

GOOGLE_OAUTH_CLIENT_ID=tu_client_id_google
GOOGLE_OAUTH_CLIENT_SECRET=tu_client_secret_google
GOOGLE_OAUTH_REDIRECT_URI=https://tu-app.onrender.com/cuentas/google/callback/

WOMPI_PUBLIC_KEY=pub_prod_xxxxx
WOMPI_PRIVATE_KEY=prv_prod_xxxxx
WOMPI_EVENTS_SECRET=xxxxx
WOMPI_INTEGRITY_SECRET=xxxxx

DEFAULT_FROM_EMAIL=soporte@tudominio.com
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.tuproveedor.com
EMAIL_PORT=587
EMAIL_HOST_USER=usuario_smtp
EMAIL_HOST_PASSWORD=password_smtp
EMAIL_USE_TLS=True
```

`SECRET_KEY` y `DATABASE_URL` los genera Render automaticamente segun `render.yaml`.

## 4. Configurar Google OAuth
En Google Cloud > Google Auth Platform > Clientes > tu cliente web:

Origenes autorizados de JavaScript:

```text
https://tu-app.onrender.com
```

URI de redireccionamiento autorizado:

```text
https://tu-app.onrender.com/cuentas/google/callback/
```

Si usas dominio propio, agrega tambien ese dominio con HTTPS.

## 5. Configurar Wompi
En Wompi > Desarrollo > Programadores:

URL de Eventos:

```text
https://tu-app.onrender.com/payments/webhook/wompi/
```

La aplicacion ya usa `SITE_PUBLIC_URL` para enviar a Wompi la URL de retorno:

```text
https://tu-app.onrender.com/payments/return/<orden>/
```

## 6. Verificacion despues del despliegue
En Render Shell ejecuta:

```bash
python manage.py check
python manage.py check_premium_ready
```

Luego prueba este flujo:

1. Abrir la app publica por HTTPS.
2. Entrar con Google.
3. Agregar un modulo premium al carrito.
4. Ir a pagar.
5. Confirmar que abre Wompi, no el mensaje de localhost.
6. Volver desde Wompi y verificar que el modulo queda habilitado solo con pago aprobado.
