# Auditoría Técnica y Funcional de la Plataforma — ConcursoDocente

**Alcance:** toda la plataforma fuera del Banco de Ítems (`banco.BancoPregunta`), que permanece congelado a la espera del Sistema Maestro de Producción de Ítems (SMPI). Cubre arquitectura, base de datos, UI/UX, navegación, seguridad, escalabilidad, formularios, manejo de errores y panel de administración.

**Método:** revisión módulo por módulo, pantalla por pantalla y componente por componente sobre el árbol de trabajo actual (incluye cambios sin commitear). Cada hallazgo indica archivo:línea cuando aplica.

**No se modificó ni eliminó ningún archivo para producir este informe.**

---

## Resumen ejecutivo

La plataforma tiene una base sólida en las tres áreas más sensibles — pagos (Wompi end-to-end, con validación de firma real y verificación server-side por dos vías independientes), autenticación (OAuth de Google completo, con manejo correcto de CSRF/estado), y el motor de simulacro (timing server-side, scoring graduado ya conectado al modelo de idoneidad). Los problemas encontrados se concentran en tres frentes: **(1) un bug silencioso que rompe la primera pantalla que ve cada usuario**, **(2) deuda de arquitectura acumulada por iteración rápida** (apps vacías instaladas, dependencias sin usar, comandos de build que borran datos sin red de seguridad), y **(3) una capa de "seguimiento del estudiante" que existe pero es demasiado delgada para sostener el producto** que se quiere construir.

---

## 1. CRÍTICOS — deben corregirse antes de continuar

| # | Hallazgo | Evidencia | Impacto |
|---|---|---|---|
| C1 | **El dashboard de inicio nunca muestra módulos.** `contenidos/views.py:20-28` pasa las claves de contexto `modulos`/`metricas['modulos']` (sin tilde); `templates/contenidos/dashboard.html:30,38` las lee como `módulos`/`metricas.módulos` (con tilde). Django resuelve variables de contexto inexistentes como cadena vacía — sin excepción, sin log. | Confirmado a nivel de bytes (`\xc3\xb3`). | La sección "Ruta formativa" completa y el contador "Módulos de ruta" están vacíos para el 100% de los usuarios, en la pantalla más visitada de la plataforma. Indetectable sin inspección de código — no genera ningún error que aparezca en logs de Render. |
| C2 | **`Modulo.TIPOS` (choices) desactualizado respecto a los datos reales.** `contenidos/models.py:5-10` sólo declara 4 valores legacy (todos con `activo=False` en producción); los 11 módulos activos reales usan valores (`diagnostico_inicial`, `lectura_critica_aplicada`, etc.) que **no existen en la lista de choices**. | Cruce directo entre `Modulo.TIPOS` y los valores `tipo` reales en BD. | El formulario de edición de `Modulo.tipo` en el admin de Django no puede representar correctamente 11 de 15 filas. Cualquier código futuro que haga `dict(Modulo.TIPOS)[m.tipo]` lanza `KeyError`. Funciona hoy sólo porque el pipeline de seed usa `update_or_create` (bypassa validación de choices) y Django no valida choices a nivel de BD. |
| C3 | **`build.sh` ejecuta comandos que borran filas de producción automáticamente en cada deploy, sin gate ni backup en el pipeline.** `build.sh:8-12` corre `deduplicar_datos` (que hace `dup.delete()` — `banco/management/commands/deduplicar_datos.py:46`), `renombrar_arquitectura_institucional`, `seed_modulos`, `apply_market_ready_upgrade`, `repair_text_quality` contra la BD real en cada `git push` a main. | Lectura directa de `build.sh` y del comando. | Si `deduplicar_datos` tiene alguna vez un bug en la lógica de "cuál fila conservar" (`deduplicar_datos.py:31-35`), el próximo deploy borra datos reales de producción sin intervención humana y sin backup automático previo (`_backups/database/` existe pero es manual). Es el mecanismo con mayor blast radius de todo el pipeline. |
| C4 | **Acciones con efectos secundarios disparadas por GET, sin protección CSRF.** "Agregar al carrito", "retirar del carrito" y "comprar" son enlaces `<a href>` (GET), no formularios POST — `commerce/views.py:add_to_cart` (línea 42), `payments/views.py:buy_module` (línea 91), templates `product_list.html:31`, `cart_detail.html:17,28`. | Lectura de vistas + templates. | GET debe ser seguro/idempotente. Un `<img src="https://concurso-docente.onrender.com/tienda/cart/remove/3/">` incrustado en cualquier sitio externo, cargado mientras el usuario tiene sesión activa, ejecuta la acción sin su consentimiento. Daño hoy limitado al propio carrito del usuario, pero es el patrón exacto que se vuelve grave en cuanto crezca el catálogo. |
| C5 | **Envío de correo de resultado 100% síncrono dentro de una transacción de BD abierta.** `simulacros/views.py:realizar_simulacro` línea 222 llama `_send_result_email(intento)` **dentro** del bloque `transaction.atomic()` (línea 178) que envuelve el guardado del intento; `_send_result_email` hace `send_mail(...)` bloqueante. No hay cola de tareas (Celery/Redis están instalados pero sin ningún wiring — confirmado por grep). | Lectura de `simulacros/views.py` + `requirements.txt` + ausencia de `CELERY_*` en settings. | Con usuarios concurrentes terminando simulacros, cada envío de correo mantiene abierta una transacción con locks sobre `Intento`/`RespuestaIntento` durante todo el round-trip SMTP. Riesgo real de timeouts/contención bajo carga, no sólo lentitud. |
| C6 | **10 comandos de management activos importan de una app no instalada — crash garantizado si se ejecutan.** `contenidos/management/commands/cargar_preguntas_sesion1.py` … `sesion7.py`, `cargar_preguntas_sesiones_3_4_5.py`, `_6_7_8.py`, `_8_9_10.py`, `limpiar_duplicados.py` hacen `from evaluaciones.models import Pregunta`, pero `evaluaciones` no está en `INSTALLED_APPS`. | Grep + `settings.py:49-70`. | Cualquier persona del equipo (o un agente de IA) que intente correr uno de estos comandos pensando que funciona obtiene un crash de Django a mitad de ejecución. Riesgo operativo, no de datos. |

---

## 2. ALTOS — siguiente fase

| # | Hallazgo | Evidencia | Impacto |
|---|---|---|---|
| A1 | 3 migraciones pendientes sin generar (`contenidos`, `simulacros`, `usuarios`) por cambios de choices (tildes) no reflejados en migraciones. | `makemigrations --check --dry-run`. | Bajo riesgo de esquema (Django no valida choices en BD), pero cualquier CI con `--check` fallaría hoy, y es señal de higiene descuidada. |
| A2 | Contador "Preguntas activas" del home usa un nombre de categoría hardcodeado (`'Banco Premium CNSC 2026 V3'`) que no coincide con nada existente. `contenidos/views.py:22`. | Comparado contra `QUESTION_CATEGORY` real y la única `Categoria` viva en BD. | Métrica siempre en 0, indefinidamente, hasta que alguien cablee el valor correcto — y ese valor cambiará otra vez cuando el SMPI defina su propia categorización. |
| A3 | `wompi_webhook` expone el mensaje crudo de la excepción (`str(exc)`) directamente en la respuesta HTTP (`payments/views.py:211-212`), y `wompi_error`/`verify_error` se renderizan sin sanitizar en `checkout.html`. | Lectura de vista + template. | Filtración de detalles internos (rutas, mensajes de librería) a quien golpee el endpoint o mire el checkout. |
| A4 | Admin sin `ModelAdmin` real en `contenidos` (`Modulo`, `Tema`) y `seguimiento` (`Intento`, `RespuestaIntento`, `ProgresoModulo`) — sólo `admin.site.register(Model)` desnudo. | `contenidos/admin.py:5-6`, `seguimiento/admin.py:4-6`. | El equipo gestiona contenido y soporte manualmente vía admin; sin `list_display`/`search_fields`/`list_filter`, depurar "¿por qué a este usuario no le llegó el resultado?" es impracticable a medida que crece el volumen. |
| A5 | No existen `404.html`/`500.html` custom ni `handler404`/`handler500`. | Búsqueda exhaustiva, cero resultados. | En producción (`DEBUG=False`) cualquier error muestra la página blanca genérica de Django, sin navbar ni forma de volver al sitio. |
| A6 | Bug dormido: `add_to_cart`/`buy_module` reciben `product_id`, lo validan, y **descartan el resultado**, sustituyéndolo siempre por el producto `ELITE_SLUG` fijo (`commerce/views.py:43-44`, `payments/views.py:92-93`). | Lectura de ambas vistas. | Inofensivo mientras exista un solo producto activo. Se convierte en "el usuario compra el producto equivocado" en cuanto se active un segundo `Product`. |
| A7 | Sin control de órdenes `pending` duplicadas — cada click en "comprar" crea una `Order` nueva sin verificar si ya hay una pendiente del mismo usuario/producto. `payments/views.py:_build_order_from_products` (línea 72-87). | Lectura de vista. | Doble click o "atrás + repetir" acumula filas huérfanas en `commerce_order`/`commerce_orderitem`. |
| A8 | `seguimiento` es funcionalmente mínimo: `ProgresoModulo.porcentaje` se estampa a 100 en el primer intento completado (`simulacros/views.py:_sync_module_progress`) — es binario, no un porcentaje real. No hay historial de intentos, desglose por competencia ni tendencia de puntaje visible al estudiante. | `seguimiento/models.py`, `seguimiento/views.py:5-19`, `mi_progreso.html`. | Es la brecha de producto más visible para un estudiante que ya pagó — "seguimiento del estudiante" hoy no cumple su promesa. (Ver Mejoras recomendadas para alcance de la solución.) |

---

## 3. MEDIOS

| # | Hallazgo | Evidencia |
|---|---|---|
| M1 | N+1 queries: `seguimiento/views.py:9-11` (`mi_progreso`, falta `select_related('modulo')`) y `simulacros/views.py:121-129` (`lista_simulacros`, chequea acceso por fila en vez de precomputar el set). | Lectura directa. |
| M2 | Sin paginación en `lista_simulacros` ni `product_list` (`.all()`/`.filter()` completos, sin `Paginator`). | `simulacros/views.py:120`, `commerce/views.py:17`. |
| M3 | Sin capa de caché en todo el proyecto — cero `CACHES`, cero `@cache_page`/`cache.get`. Cada carga de `dashboard` recalcula `Avg('puntaje_obtenido')` sobre todos los intentos del usuario. | Grep completo + `contenidos/views.py:17`. |
| M4 | `RespuestaIntento` se crea con `.create()` uno por uno dentro de un loop (`simulacros/views.py:186-210`) en vez de `bulk_create`. | Lectura directa. |
| M5 | Tres patrones de validación de formularios distintos y sin convención: `ModelForm` completo (`usuarios`), parsing manual con `try/except` (`simulacros`), ninguna validación (`commerce`/`payments`, sólo `product_id` de URL). | Lectura de las 4 vistas. |
| M6 | `registro.html`/`login.html` no usan `{{ form.field }}` — reconstruyen `<input>` manualmente sin `id`/`value`; si la validación falla server-side, el usuario **pierde todo lo escrito** y no hay error resaltado por campo. Tampoco hay asociación `<label for>`↔`<input id>` (sí presente correctamente en `configurar_simulacro.html`, inconsistente). | `templates/usuarios/registro.html:24,28,34,39,44,61,67,71`, `templates/registration/login.html:20,24`. |
| M7 | 9 enlaces con rutas absolutas hardcodeadas en vez de `{% url %}` (`dashboard.html`, `detalle_modulo.html`, `mi_progreso.html`, `perfil.html`). | Grep cruzado contra `{% url %}`. |
| M8 | Nav duplicado: "Inicio" y "Módulos" en `base.html:27-28` apuntan al mismo `{% url 'dashboard' %}`, sin diferencia funcional. | Lectura directa. |
| M9 | `{% block title %}` inconsistente — la mayoría de las páginas (`dashboard`, `lista_simulacros`, `mi_progreso`, `cart_detail`, `product_list`, `checkout`, `payment_return`) no lo define; todas muestran el título genérico de `base.html`. | Grep de `{% block title %}` en cada template. |
| M10 | Empty states manejados ad-hoc, sin componente compartido — 5 wordings/estilos distintos para "no hay nada que mostrar". | `product_list.html:36`, `lista_simulacros.html:48`, `cart_detail.html:31`, `mi_progreso.html:32`, `seleccionar_area.html:39`. |
| M11 | Cero uso de `{% include %}` o partials en todo el proyecto — cada template es un monolito plano. Duplicación concreta confirmada: badge "status-pill" (2 archivos), grid de métricas mini (2 archivos), card genérica `card border-0 shadow-sm` (10 archivos), barra de progreso (2 archivos), bloque de respuesta/justificación de pregunta implementado 3 veces con estructuras distintas. | Detalle completo en auditoría de origen, sección 3. |
| M12 | 11 de 22 dependencias en `requirements.txt` no están wireadas a ningún lado: `celery`, `kombu`, `billiard`, `amqp`, `vine`, `redis`, `djangorestframework`, `django-jazzmin`, `django-cors-headers`, `django-extensions`, `django-sslserver-v2`. | Grep completo, cero referencias fuera de `requirements.txt`. Inflan el `pip install` de cada deploy sin aportar nada hoy — ver informe de código muerto para recomendación caso por caso (algunas, como celery/redis, son candidatas a *activarse* en vez de eliminarse, dado C5). |
| M13 | Imports sin usar: `Tema` (`contenidos/views.py:5`), `Cart` (`payments/views.py:16`), `render` en `banco/views.py`, `academics/views.py`, `access_control/views.py` (boilerplate de `startapp`). | AST scan. |

---

## 4. BAJOS

| # | Hallazgo |
|---|---|
| B1 | Chart.js 4.4.0 cargado globalmente en `base.html:82`; ningún template lo usa (`Chart(`/`<canvas` — cero resultados). |
| B2 | Íconos decorativos (`<i class="bi bi-...">`) sin `aria-hidden="true"` — mejora menor de accesibilidad. |
| B3 | `SECRET_KEY` con fallback inseguro hardcodeado en `settings.py:25` — mitigado por el check que exige cambiarlo si `DEBUG=False`, pero el valor por defecto queda visible en el repo. |
| B4 | Sin `SECURE_SSL_REDIRECT`/`SECURE_HSTS_*` explícitos a nivel de Django — depende 100% de que Render fuerce HTTPS en el edge (no verificable desde el código). |
| B5 | `STORAGES['default']` usa `FileSystemStorage` sobre un disco efímero de Render (sin bloque `disk:` en `render.yaml`). Riesgo **latente, no activo**: ningún modelo tiene `ImageField`/`FileField` hoy, pero cualquier futura foto de perfil, comprobante o certificado se perdería en el próximo deploy si se agrega sin antes montar un disco persistente o storage externo. |
| B6 | Acceso (`UserAccess`) no se revalida a mitad de un intento de simulacro ya iniciado — edge case de bajo impacto dado el modelo de compra única (no suscripción con expiración recurrente). |
| B7 | `WompiService.get_acceptance_token()` se llama de forma síncrona en cada carga de la página de checkout, sin caché — si Wompi está lento, el checkout se degrada directamente. |
| B8 | `django-cors-headers` instalado pero no activado en `INSTALLED_APPS`/`MIDDLEWARE` — peso muerto, sin riesgo activo. |

---

## 5. MEJORAS RECOMENDADAS

Estas no son errores — son la distancia entre "funciona" y "está terminada", en las áreas que tú mismo señalaste como foco (arquitectura, UX, seguimiento, analítica, diagnóstico):

1. **Seguimiento y analítica real**: reemplazar `ProgresoModulo` (0/100 binario) por historial de intentos visible al estudiante, desglose de aciertos por competencia/subtema, tendencia de puntaje en el tiempo. Es la mejora de mayor impacto percibido por un usuario que ya pagó.
2. **Diagnóstico Inicial adaptativo**: hoy es un simulacro fijo más, sin ninguna lógica de selección basada en desempeño previo. Diseñar la lógica de selección/orientación ahora, de forma que sólo falte "enchufar" el banco de ítems del SMPI cuando esté listo.
3. **Análisis del Desempeño y Plan de Fortalecimiento**: ya se venden como productos en el catálogo (`commerce.Product`) pero no tienen ninguna vista/lógica detrás — hoy un usuario podría comprarlos y no recibir nada.
4. **Componentización de UI**: crear `templates/partials/` para status-pill, card genérica, barra de progreso, bloque de pregunta/respuesta y empty-state — elimina la duplicación de M11 y facilita mantener consistencia visual mientras la plataforma crece.
5. **Sacar los comandos de reparación de datos del pipeline automático de `build.sh`**, o gatearlos con una confirmación/flag — mitiga C3 sin perder la conveniencia de tenerlos automatizados para lo que sí es seguro (seed de catálogo).
6. **Resolver la colisión de nombres** entre la app Django `dashboard` (que no sirve UI, sólo alberga `question_generator.py` y comandos) y la vista `dashboard` de `contenidos` (que sí es la home) — confuso para onboarding de cualquier futuro colaborador.
7. **Documentar explícitamente el riesgo de storage efímero (B5)** en el propio repo (README o comentario en `settings.py`) antes de que alguien agregue un `FileField` sin saberlo.

---

## Dependencias entre módulos (mapa de referencia)

```
usuarios (Usuario, auth) 
   └─ referenciado por: TODAS las apps vía request.user

academics (Category, Module, NormativeResource)
   └─ FK target de: commerce.Product, access_control.UserAccess, simulacros.Simulacro

banco (Categoria, Subcategoria, BancoPregunta)   [CONGELADO — pendiente SMPI]
   └─ M2M target de: simulacros.Simulacro.preguntas

contenidos (Modulo, Tema)
   └─ FK target de: seguimiento.ProgresoModulo
   └─ poblado por: dashboard/question_generator.py:MODULES vía apply_market_ready_upgrade

simulacros (Simulacro)
   └─ orquesta: banco (preguntas) + seguimiento (Intento/RespuestaIntento) + access_control (gate)

seguimiento (Intento, RespuestaIntento, ProgresoModulo)
   └─ escrito por: simulacros.views
   └─ leído por: seguimiento.views (mi_progreso), contenidos.views (métricas home)

commerce (Product, Cart, Order) ←→ payments (Payment, WompiService) ←→ access_control (UserAccess)
   └─ ciclo completo: Product → Order → Payment → grant_full_access → UserAccess → user_has_module_access (gate en simulacros)
```

**Riesgo de escalabilidad estructural más relevante**: `simulacros` es el único punto de la aplicación que toca 4 apps a la vez en una sola vista (`banco`, `seguimiento`, `access_control`, y potencialmente `payments` vía redirect) dentro de una única transacción síncrona que también envía correo (C5). Es el nodo de mayor acoplamiento y el primero que sentirá presión si crece el tráfico concurrente.
