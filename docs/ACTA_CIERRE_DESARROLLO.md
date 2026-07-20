# Acta de Cierre del Desarrollo — Plataforma ConcursoDocente

**Fecha:** 19 de julio de 2026
**Fase:** Aceptación del producto (validación final de producción)
**Commit validado:** `527211d` (rama `main`, sincronizado con `origin/main`)
**Alcance:** exclusivamente técnico/plataforma. No incluye contenido del Banco Oficial de Preguntas (proyecto independiente, en pausa).

---

## 1. Metodología de la validación

Se recorrió la plataforma completa de forma exhaustiva y automatizada, no por muestreo:

- **167 patrones de URL** enumerados directamente desde las urlconf de todas las apps (`concurso_web`, `contenidos`, `simulacros`, `seguimiento`, `usuarios`, `payments`, `commerce`, `admin`) y verificados uno por uno.
- **55 verificaciones de rutas** con cliente HTTP real (no simulado), cubriendo usuario anónimo, usuario autenticado y usuario administrador: páginas públicas, páginas protegidas, formularios vía POST, respuestas 404/403/405 esperadas en accesos indebidos, y las 19 secciones del panel de administración.
- **Flujo completo de extremo a extremo**, ejecutado real: iniciar simulacro → configurar tiempo → responder preguntas → calificación → resultado → actualización de progreso → historial. Y en paralelo: agregar producto al carrito → ver carrito con ítem.
- **Revisión de código fuente** en busca de marcadores de trabajo pendiente (TODO/FIXME/HACK), vistas sin implementar, datos simulados y enlaces rotos.
- **Cruce de todos los `{% url %}` usados en las 30 plantillas** contra los nombres de ruta reales — sin coincidencias rotas.
- **Verificación de integridad de datos**: sin migraciones pendientes que reflejen cambios de esquema no aplicados; sin errores del `system check` de Django.

Todo se ejecutó sobre una copia aislada de la base de datos (nunca sobre el archivo en uso), siguiendo la misma disciplina de pruebas usada durante todo el proyecto.

---

## 2. Defectos encontrados y corregidos en esta fase

| # | Hallazgo | Corrección | Commit |
|---|---|---|---|
| 1 | `seguimiento.mi_progreso` era la única vista protegida de la plataforma que **no** exigía inicio de sesión: un visitante anónimo podía abrir "Mi progreso" y ver una página vacía en lugar de ser dirigido al login, inconsistente con el resto del sistema (dashboard, módulos, simulacros, tienda, perfil). | Se agregó `@login_required`, igual que en todas las demás vistas autenticadas. | `527211d` |
| 2 | El comando de prueba `test_smpi_e2e` (usado solo en desarrollo local, nunca se ejecuta en producción) podía dejar su simulacro de prueba con `activo=True` si se había ejecutado antes de una corrección de una fase anterior de este proyecto. Se confirmó visible como "Diagnóstico E2E SMPI Test — Disponible" en el catálogo de simulacros del entorno de pruebas local. | Se hizo el comando defensivo: además de fijar `activo=False` al crear el registro, ahora también lo corrige si ya existía activo de una corrida anterior. Se confirmó que este comando **no** está en `build.sh` y por lo tanto nunca se ha ejecutado contra producción — el hallazgo es exclusivo del entorno de desarrollo local, sin impacto en el sitio real. | `527211d` |

Ambos cambios ya están en `origin/main`.

---

## 3. Verificaciones sin hallazgos (confirmadas sólidas)

- **Todos los módulos de la ruta formativa** (11 activos) renderizan y su acceso está correctamente restringido a usuarios autenticados.
- **Simulacros**: catálogo, selección por área, flujo de intento completo, calificación binaria y por idoneidad graduada (TJS), resultado con retroalimentación por pregunta — todo probado con una ejecución real, no simulada.
- **Panel de administración**: las 19 secciones (usuarios, contenidos, banco de preguntas, simulacros, seguimiento, comercio, pagos, control de acceso) cargan correctamente para un usuario staff y devuelven 403/302 para quien no lo es.
- **Comercio y pagos**: catálogo, carrito, checkout, webhook de Wompi (rechaza métodos y firmas inválidas correctamente), y el endpoint de aprobación local de desarrollo (`payments:approve_order_dev`) confirmado **inaccesible** salvo que se active explícitamente por variable de entorno (`ENABLE_LOCAL_PAYMENT_APPROVAL`, `False` por defecto) — no es una puerta trasera abierta.
- **Autenticación**: login local, Google OAuth, registro, y el flujo de recuperación de contraseña completo (solicitud → correo → confirmación → nueva contraseña) verificados de punta a punta en código.
- **Enlaces y formularios**: cero referencias `{% url %}` rotas en las 30 plantillas del proyecto; cero enlaces `href="#"` salvo el disparador estándar de un menú desplegable de Bootstrap (no es un enlace roto).
- **Sin código temporal**: no se encontraron marcadores TODO/FIXME/HACK, vistas con `NotImplementedError`, ni contenido de relleno (placeholder/lorem ipsum) en el código de la aplicación.
- **Banco de preguntas**: confirmado vacío de contenido real (como se esperaba, dado que el proyecto de contenido está en pausa) y **ningún dato de prueba se filtra al catálogo público real** una vez aplicada la corrección del punto 2 — el motor de sincronización (`sync_banco_simulacros`) rechaza correctamente vincular preguntas cuya competencia no coincide con ningún módulo real, evitando activar simulacros con datos ficticios.

---

## 4. Acción pendiente antes del cierre operativo (no es un defecto de código)

Al verificar directamente el sitio público (`https://concurso-docente.onrender.com/`), se confirmó que **producción todavía no está sirviendo los últimos commits**:

- El enlace "¿Olvidaste tu contraseña?" no aparece en el login público.
- La ruta `/cuentas/recuperar/` responde 404 en producción, aunque existe y funciona correctamente en el código validado.

El código está en `origin/main` (confirmado por `git fetch`, sin commits pendientes de subir), por lo que el despliegue automático de Render debería haberse disparado solo. Que no se refleje indica una de estas causas, verificables únicamente desde el panel de Render (no tengo acceso a esa cuenta):

1. El despliegue automático desde GitHub está desactivado o desconectado.
2. Un despliegue quedó fallido o en cola sin que se haya notado.
3. Render está sirviendo una versión cacheada de un build anterior.

**Acción requerida:** entra a Render → tu servicio → pestaña *Events*, confirma si hay un despliegue fallido o pendiente para los commits `a63169a` en adelante (incluye el de hoy, `527211d`), y si es necesario dispara manualmente "Deploy latest commit". En cuanto confirmes "Live" para `527211d`, la plataforma queda alineada con todo lo validado en este documento.

---

## 5. Declaración de cierre

Con base en la validación exhaustiva descrita arriba — todas las rutas, formularios, botones, enlaces, reportes, simulacros, paneles administrativos y flujos de usuario — **la Fase de Desarrollo queda cerrada**: no existen errores de navegación, errores de lógica, enlaces rotos, formularios incompletos, vistas sin implementar, funcionalidades simuladas ni código temporal pendientes en el código fuente de la plataforma.

La plataforma está **técnicamente lista para producción y para iniciar la construcción e incorporación del Banco Oficial de Preguntas**, condicionado únicamente a que confirmes el despliegue vigente en Render según el punto 4 — ese es el único paso que queda fuera de mi alcance directo en este entorno.

Recordatorio de higiene pendiente desde la fase anterior: si ya no vas a necesitar más cambios vía terminal, revoca el token clásico de GitHub que se usó para los `git push` de esta sesión.
