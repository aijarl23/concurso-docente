# Informe de Código Muerto — ConcursoDocente

Ningún archivo fue eliminado ni modificado para producir este informe. Clasificación final por elemento en la sección de cierre.

---

### 1. App Django `analytics`

- **Ruta**: `analytics/` (`models.py`, `views.py`, `admin.py`, sin `urls.py`)
- **Función que cumplía**: apartado originalmente para funcionalidad de analítica/seguimiento; nunca se implementó nada dentro.
- **Motivo por el que se considera código muerto**: `models.py`/`views.py` son el boilerplate sin modificar de `startapp` (`# Create your models here.` / `# Create your views here.`), `admin.py` sin registros, sin `urls.py`.
- **Evidencia de ausencia de referencias activas**: grep de `analytics` sobre todo el proyecto no devuelve ningún `import`/`include` fuera de `INSTALLED_APPS`; `python manage.py showmigrations analytics` → `(no migrations)`.
- **Riesgo de eliminar**: ninguno — no hay tablas, no hay datos, no hay código dependiente.
- **Posibilidad de reutilización futura**: **alta**. El nombre y propósito coinciden exactamente con la "Mejora recomendada #1" de la auditoría técnica (seguimiento y analítica real del estudiante) que quieres construir a continuación. Antes de eliminarla, vale la pena decidir si se **reutiliza como el namespace real** para esa funcionalidad en vez de crear una app nueva desde cero.

### 2. App Django `landing`

- **Ruta**: `landing/` (`models.py`, `views.py`, `admin.py`, sin `urls.py`)
- **Función que cumplía**: pensada como página de aterrizaje separada de la home autenticada.
- **Motivo**: mismo patrón que `analytics` — boilerplate sin modificar, cero contenido.
- **Evidencia**: grep sin resultados fuera de `INSTALLED_APPS`; `showmigrations landing` → `(no migrations)`. La home real ("landing") hoy la sirve `contenidos.views.dashboard`, no esta app.
- **Riesgo de eliminar**: ninguno.
- **Reutilización futura**: media — sólo tendría sentido si en algún momento se decide separar una landing pública (marketing, no autenticada) de la home actual (que ya mezcla ambos roles). No hay indicio de que eso esté planeado.

### 3. App `evaluaciones` completa

- **Ruta**: `evaluaciones/` (`models.py`, `views.py`, `urls.py`, `admin.py`, `migrations/`, `management/commands/` con 10 comandos de carga)
- **Función que cumplía**: predecesora del actual `banco`+`contenidos` — modelo `Pregunta` propio, vistas de simulacro propias, comandos de carga masiva de preguntas por "sesión".
- **Motivo**: **no está en `INSTALLED_APPS`** (`concurso_web/settings.py:49-70`, confirmado ausente); nada en el código vivo la referencia.
- **Evidencia**: grep de `evaluaciones.views`/`evaluaciones.urls` sin resultados fuera del propio directorio; ausencia confirmada en `INSTALLED_APPS`.
- **Riesgo de eliminar**: **bajo-medio, con una dependencia a resolver junto con el ítem 4** — 10 comandos activos dentro de la app viva `contenidos` importan `from evaluaciones.models import Pregunta`. Si se borra sólo `evaluaciones/` sin tocar esos 10 comandos, el error que producirían pasa de "app no instalada" a `ImportError` — mismo resultado práctico (ya están rotos hoy), pero conviene eliminar ambos al mismo tiempo para dejar el repo limpio, no a medias.
- **Reutilización futura**: nula — el contenido y la arquitectura que representaba ya fueron migrados (y luego reconstruidos desde cero) en `banco`/`contenidos` esta misma sesión.

### 4. 10 comandos de management en `contenidos/management/commands/` que dependen de `evaluaciones`

- **Rutas**: `cargar_preguntas_sesion1.py` … `cargar_preguntas_sesion7.py`, `cargar_preguntas_sesiones_3_4_5.py`, `cargar_preguntas_sesiones_6_7_8.py`, `cargar_preguntas_sesiones8_9_10.py`, `limpiar_duplicados.py` (todos bajo `contenidos/management/commands/`)
- **Función que cumplía**: cargar manualmente, por lotes ("sesiones"), preguntas curadas hacia el modelo `evaluaciones.Pregunta`.
- **Motivo**: hacen `from evaluaciones.models import Pregunta`, pero esa app no está instalada — ejecutarlos hoy garantiza un crash.
- **Evidencia**: grep de `from evaluaciones.models import` dentro de `contenidos/management/commands/`, cruzado contra la ausencia de `evaluaciones` en `INSTALLED_APPS`.
- **Riesgo de eliminar**: ninguno — ya están rotos, no hay forma de que estén en uso.
- **Reutilización futura**: nula — el contenido que cargaban (preguntas de las "sesiones" 1-10) pertenece a una generación de banco de preguntas anterior a la reconstrucción total de esta sesión; no tiene relación con el SMPI que se va a construir.

### 5. Templates huérfanos: `templates/contenidos/lista_sesiones.html` y `detalle_sesion.html`

- **Rutas**: `templates/contenidos/lista_sesiones.html`, `templates/contenidos/detalle_sesion.html`
- **Función que cumplía**: UI de una feature de "sesiones de estudio" (listado + detalle con breadcrumbs) que nunca se completó del lado de vistas/URLs.
- **Motivo**: referencian `{% url 'lista_sesiones' %}`, `{% url 'detalle_sesion' ... %}`, `{% url 'completar_sesion' ... %}` — ninguno de esos nombres existe en `contenidos/urls.py` actual, y las vistas correspondientes tampoco existen en `contenidos/views.py` actual (sólo sobreviven en `_backups/legacy_project/BACKUP_PRO/`). Si alguna vista intentara renderizarlos hoy, Django lanzaría `NoReverseMatch` de inmediato.
- **Evidencia**: cruce de nombres de URL usados en los templates contra los patterns registrados en `contenidos/urls.py`.
- **Riesgo de eliminar**: ninguno — ninguna vista viva los renderiza.
- **Reutilización futura**: **media** — es la única pieza de UI (incluye breadcrumbs, algo que no existe en ningún otro template vivo) pensada para una navegación por "sesiones de estudio" secuenciales. Si en algún momento el SMPI organiza el contenido en sesiones/rutas de estudio, este diseño podría servir de punto de partida visual antes de descartarlo.

### 6. `templates/evaluaciones/` completo (3 archivos)

- **Rutas**: `templates/evaluaciones/lista_simulacros.html`, `realizar_simulacro.html`, `resultado_simulacro.html`
- **Función que cumplía**: UI de la app `evaluaciones` (ítem 3).
- **Motivo**: la app que las sirve no está instalada; nada las referencia.
- **Evidencia**: grep sin resultados fuera del propio directorio.
- **Riesgo de eliminar**: ninguno.
- **Reutilización futura**: nula — son una versión anterior y de menor calidad de las plantillas ya vivas en `templates/simulacros/` (por ejemplo, `resultado_simulacro.html` de `evaluaciones` resuelve el texto de la opción A/B/C/D con una cascada de `{% if %}` en vez del lookup por diccionario que ya usa la versión viva).

### 7. Bloque muerto dentro de `dashboard/question_generator.py` (líneas 283-425, ~500 líneas)

- **Ruta**: `dashboard/question_generator.py:283-425`
- **Función que cumplía**: generador mecánico de preguntas curadas (`build_math_item`, `build_question`, `validate_item`, `register_item`, `generate_question_set`, `iter_generation_modules`, más los bloques de datos `CURATED_TOPICS`, `AREA_TOPICS_CURATED`, `READING_PASSAGES`, `CURATED_VARIANTS`) — predecesor mecánico de lo que hoy hará el SMPI con IA.
- **Motivo**: ninguna de esas funciones/símbolos se invoca desde ningún otro punto del código.
- **Evidencia**: grep de `generate_question_set|CURATED_TOPICS|iter_generation_modules` sólo encuentra resultados dentro del propio archivo de definición.
- **Riesgo de eliminar**: **medio, por ser un archivo mixto** — el mismo archivo define símbolos que sí están vivos y en uso activo: `MODULES` (catálogo de los 11 módulos, consumido por `apply_market_ready_upgrade.py`), `ELITE_SLUG`, `AREA_MODULE_SLUG`, `QUESTION_CATEGORY`, `SIMILARITY_THRESHOLD`, `jaccard`, `normalize`, `token_set`. Borrar el archivo completo rompería el catálogo de módulos. Hay que extraer/eliminar quirúrgicamente sólo el bloque 283-425, no el archivo entero.
- **Reutilización futura**: nula — conceptualmente reemplazado por el SMPI que se va a construir.

### 8. 11 dependencias en `requirements.txt` sin ningún uso en el código

- **Ruta**: `requirements.txt` (paquetes: `celery`, `kombu`, `billiard`, `amqp`, `vine`, `redis`, `djangorestframework`, `django-jazzmin`, `django-cors-headers`, `django-extensions`, `django-sslserver-v2`)
- **Función que cumplía**: cada una fue instalada pensando en una feature no implementada — cola de tareas en background (celery/redis y sus dependencias internas kombu/billiard/amqp/vine), API REST (djangorestframework), admin con mejor UX (django-jazzmin), CORS (django-cors-headers), utilidades de desarrollo (django-extensions), servidor de desarrollo con SSL (django-sslserver-v2).
- **Motivo**: ninguna aparece en `INSTALLED_APPS`/`MIDDLEWARE`, ninguna tiene código que la invoque (`@shared_task`, `serializers.py`, `viewsets.py`, configuración `CELERY_*`, etc. — todo ausente).
- **Evidencia**: grep completo por nombre de import de cada paquete, cero resultados fuera de `requirements.txt`.
- **Riesgo de eliminar**: bajo en general, **pero no deben tratarse como un bloque uniforme**: `celery`+`redis` son precisamente la solución natural al hallazgo C5 de la auditoría técnica (correo síncrono dentro de una transacción abierta), y `djangorestframework` sería necesario si en algún momento se separa un frontend propio del backend Django. Eliminarlas ahora sólo para tenerlas que reinstalar en semanas sería trabajo perdido.
- **Reutilización futura**: alta para `celery`/`redis`/`djangorestframework`; baja para `django-jazzmin`/`django-extensions`/`django-sslserver-v2`/`django-cors-headers` (ninguna resuelve un problema ya identificado en la auditoría).

### 9. Imports sin usar (hallazgo menor, 5 archivos)

- **Rutas y símbolos**: `Tema` en `contenidos/views.py:5`; `Cart` en `payments/views.py:16`; `render` en `banco/views.py`, `academics/views.py`, `access_control/views.py` (boilerplate de `startapp`, apps sin ninguna vista real).
- **Función que cumplía**: ninguna — residuo de refactors o de scaffolding inicial.
- **Motivo**: AST scan confirma cero referencias al símbolo dentro del propio archivo tras la línea de import.
- **Evidencia**: análisis estático (AST) de los 5 archivos.
- **Riesgo de eliminar**: ninguno.
- **Reutilización futura**: no aplica.

---

## Clasificación final

### 1. Seguro para eliminar
- App `evaluaciones` completa **+** los 10 comandos dependientes en `contenidos/management/commands/` (eliminar juntos, en el mismo cambio, para no dejar un `ImportError` a medias).
- `templates/evaluaciones/` (3 archivos).
- Imports sin usar (`Tema`, `Cart`, `render` ×3).

### 2. Recomendado archivar (mover a `_backups/` o similar, no borrar del historial de golpe)
- App `landing` — sin uso previsto conocido, pero de riesgo cero mantenerla archivada en vez de borrada por si se retoma la idea de una landing pública separada.

### 3. Requiere revisión antes de eliminar (decisión tuya, con recomendación explícita)
- **App `analytics`** → recomendación: **no eliminar, reutilizar** como base de la nueva funcionalidad de seguimiento/analítica (Mejora #1 de la auditoría técnica) en vez de crear una app nueva.
- **`templates/contenidos/lista_sesiones.html` / `detalle_sesion.html`** → recomendación: revisar el diseño (incluye el único breadcrumb del proyecto) antes de decidir si se descarta o se adapta para una futura navegación por sesiones/rutas de estudio.
- **Bloque `dashboard/question_generator.py:283-425`** → recomendación: extraer quirúrgicamente sólo ese bloque, conservando intacto el resto del archivo (`MODULES` y las demás utilidades en uso activo).
- **11 dependencias sin uso en `requirements.txt`** → recomendación: mantener `celery`/`redis`/`djangorestframework` (resuelven problemas ya identificados: C5 y una eventual API), decidir caso por caso sobre `django-jazzmin`/`django-extensions`/`django-sslserver-v2`/`django-cors-headers`.
