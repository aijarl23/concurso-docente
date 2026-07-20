# Informe Final — Desarrollo Técnico de la Plataforma ConcursoDocente

**Fecha:** 20 de julio de 2026
**Alcance:** exclusivamente técnico/plataforma. No incluye contenido del Banco Oficial de Preguntas (proyecto separado, en pausa por instrucción explícita).
**Último commit desplegable:** `a63169a` (push confirmado a `origin/main`; deploy en Render pendiente de confirmación — ver sección final).

---

## 1. Funcionalidades implementadas (nuevas en esta fase)

| # | Funcionalidad | Detalle |
|---|---|---|
| 1 | Pipeline de activación del banco | `activar_lote_oficial`: promueve un lote revisado (`en_revision`→`publicado`) por categoría/subtema. |
| 2 | Sincronización banco↔simulacro | `sync_banco_simulacros`: conecta preguntas publicadas con el `Simulacro` real de cada módulo, repara enlaces rotos a módulos legacy, crea el `Simulacro` que le faltaba a un módulo, puebla Diagnóstico Inicial con muestra real de los demás módulos. Corre automático en cada deploy. |
| 3 | Recuperación de contraseña | Flujo completo (solicitud → correo → confirmación → nueva contraseña), con las 4 plantillas propias y enlace en el login. Antes no existía ninguna vía de recuperación para login local. |
| 4 | Deduplicación robusta de Simulacro | `deduplicar_datos` ahora también agrupa por (módulo, tipo, área), no solo por nombre exacto — detecta duplicados que un renombrado dejó con nombres distintos. |
| 5 | Normalización de finales de línea | `build.sh`, `requirements.txt`, `render.yaml` pasados de CRLF a LF (causa raíz de que el build fallara por completo en Render). |
| 6 | Limpieza de código | Imports sin usar (`banco`, `academics`, `access_control`), templates huérfanos de una feature de "sesiones" nunca conectada. |

---

## 2. Funcionalidades verificadas (existentes, confirmadas funcionando)

Verificado con un cliente HTTP real (Django test client) sobre una copia aislada de la base de datos — no solo lectura de código:

- **Dashboard**: métricas reales (módulos, preguntas activas, simulacros, promedio, progreso).
- **Diagnóstico Inicial**: muestreo real de preguntas ya validadas de los demás módulos.
- **Módulos de estudio**: los 11 módulos renderizan correctamente, incluidos los dos que no tienen preguntas propias (Análisis del Desempeño y Plan de Fortalecimiento — se renderizan con análisis en vivo del historial del usuario).
- **Simulacros**: flujo completo iniciar → responder → resultado, probado con un simulacro real con preguntas reales.
- **Motor de evaluación**: scoring binario y scoring por idoneidad graduada (TJS / Análisis de Casos), ambos correctos.
- **Seguimiento del estudiante**: historial de intentos, gráfico de tendencia de puntaje (Chart.js), avance por módulo, desempeño por competencia.
- **Reportes (Análisis del Desempeño)**: cálculo en vivo desde `seguimiento/analitica.py`, no datos estáticos.
- **Plan de Fortalecimiento**: ruta recomendada generada en vivo a partir de las brechas detectadas.
- **Administración**: panel completo y funcional, con `ModelAdmin` real (filtros, búsqueda, inlines) en todas las apps relevantes.
- **Comercio y pagos**: catálogo, carrito, checkout, integración Wompi (webhook + retorno) con manejo de error sin fuga de información.
- **Autenticación**: registro, login local, Google OAuth, y ahora recuperación de contraseña — las 4 vías probadas.
- **Flujo completo de estudio**: registro → dashboard → módulo → simulacro → resultado → progreso, probado de punta a punta sin intervención manual.

---

## 3. Errores corregidos

### Encontrados y corregidos en esta fase
1. **Banco de preguntas sin pipeline de publicación**: existía el comando para importar lotes, pero ninguno para activarlos ni para conectarlos a un `Simulacro` — los 21 simulacros reales estaban inactivos con 0 preguntas.
2. **Causa raíz de duplicación de `academics.Module`**: `repair_text_quality` aplicaba corrección de tildes también a los `slug` (identificadores técnicos), generando un módulo duplicado en cada deploy.
3. **`IntegrityError` que tumbaba el build completo**: el auto-arreglo de `Modulo.tipo` no contemplaba el caso en que ya coexistían la fila corrupta y la canónica (violaba el `UNIQUE`).
4. **Fixture de prueba expuesto sin pago**: el simulacro de prueba de `test_smpi_e2e` quedaba visible y accesible gratis en el catálogo real.
5. **Build roto por finales de línea CRLF**: causa de dos fallos de deploy consecutivos en Render.
6. **Sin recuperación de contraseña**: usuarios con login local quedaban bloqueados permanentemente si la olvidaban.

### Ya corregidos antes de esta fase (verificados, no re-trabajados)
Dashboard sin mostrar módulos, `Modulo.TIPOS` desactualizado, acciones de carrito/pago por GET sin CSRF, envío de correo dentro de una transacción de BD, fuga de excepciones en el webhook de Wompi, admin sin `ModelAdmin` real, páginas 404/500 genéricas de Django, app `evaluaciones` y sus 10 comandos rotos, órdenes de compra duplicadas.

---

## 4. Módulos terminados

- Los 11 módulos de la ruta formativa (Diagnóstico Inicial, Lectura Crítica, Normatividad Educativa, Inclusión Educativa, Competencias Pedagógicas, Análisis de Casos, Gestión Escolar, Competencias Disciplinares, Simulacro Integral, Análisis del Desempeño, Plan de Fortalecimiento).
- Comercio y pagos (Wompi).
- Autenticación completa (local, Google, recuperación de contraseña).
- Administración.
- Pipeline técnico para recibir el Banco Oficial de Preguntas (infraestructura lista; sin contenido cargado — eso corresponde al proyecto en pausa).

---

## 5. Funcionalidades pendientes

Ninguna es bloqueante para producción. En orden de relevancia:

1. **Confirmar el deploy en Render del commit `a63169a`** (recuperación de contraseña) — el push a GitHub ya se hizo; falta confirmar en la pestaña Events que quedó "Live".
2. **Repetición espaciada** (priorizar subtemas con peor desempeño histórico del estudiante): documentada explícitamente como mejora de fase futura, hoy el sistema selecciona de forma neutral. No bloquea el uso actual.
3. **Simulacros legacy de áreas disciplinares** (`area-ingles`, `area-matematicas`, etc.) conviven inactivos junto a los vigentes (`simulacros-por-area`): sin riesgo, candidatos a limpieza de higiene en un futuro paso, no urgente.
4. **`SECURE_HSTS_SECONDS` / `SECURE_SSL_REDIRECT`** no configurados explícitamente a nivel de Django (hoy depende de que Render fuerce HTTPS en el borde): hardening menor, no bloqueante.

---

## Estado general

La plataforma está técnicamente terminada y verificada de punta a punta. El Banco Oficial de Preguntas queda como proyecto independiente, en pausa, a la espera de que decidas retomarlo.
