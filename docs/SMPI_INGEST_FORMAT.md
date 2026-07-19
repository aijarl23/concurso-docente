# Formato de Ingesta SMPI (Banco Oficial de Ítems)

Este documento especifica el formato JSON esperado por el comando `python manage.py ingest_smpi` para importar preguntas del Banco Oficial de Ítems.

## Estructura General

```json
[
  {
    "titulo": "Situación contextual (opcional)",
    "contexto": "Enunciado largo o descripción del caso",
    "enunciado": "La pregunta específica",
    "opcion_a": "Alternativa A",
    "opcion_b": "Alternativa B",
    "opcion_c": "Alternativa C",
    "opcion_d": "Alternativa D",
    "respuesta_correcta": "A",
    "area": "lectura_critica",
    "competencia": "Lectura crítica",
    "dificultad": "alto",
    "tipo_item": "estandar",
    "justificacion": "Explicación de por qué A es correcta",
    "fuente_normativa": "Decreto 1278, Art. 5",
    "proceso_cognitivo": "comprension_aplicada",
    "puntaje_validacion": 95
  }
]
```

## Campos Requeridos

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `contexto` o `titulo` | string | Al menos uno debe estar presente. Contexto de la pregunta o situación. |
| `enunciado` | string | La pregunta en sí. |
| `opcion_a` | string | Primera alternativa. |
| `opcion_b` | string | Segunda alternativa. |
| `opcion_c` | string | Tercera alternativa. |
| `opcion_d` | string | Cuarta alternativa. |
| `respuesta_correcta` | string | Una de: `A`, `B`, `C`, `D` |

## Campos Recomendados

| Campo | Tipo | Valores | Descripción |
|-------|------|--------|-------------|
| `area` | string | `general`, `ingles`, `tecnologia`, `matematicas`, `ciencias_naturales`, `ciencias_sociales`, `lectura_critica`, `perfil_docente`, `componente_pedagogico`, `psicotecnico` | Área de conocimiento. Default: `general` |
| `competencia` | string | Texto libre | Competencia evaluada, ej. "Lectura crítica", "Normativa educativa aplicada" |
| `dificultad` | string | `facil`, `medio`, `alto`, `muy_alto` | Nivel de complejidad. Default: `alto` |
| `tipo_item` | string | `estandar`, `mas_adecuada`, `menos_adecuada` | Tipo de pregunta. Default: `estandar` |

## Campos Opcionales

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `titulo` | string | Contexto corto o situación (se concatena con `contexto`) |
| `justificacion` | string | Explicación técnica de la respuesta correcta. |
| `fuente_normativa` | string | Referencias normativas, ej. "Ley 115, Art. 1" |
| `proceso_cognitivo` | string | Nivel cognitivo: `identificacion`, `comprension_aplicada`, `analisis_situacional`, `evaluacion_juicio` |
| `puntaje_validacion` | number | 0-100, score de calidad del ítem. |

## Campos de Idoneidad Graduada (Solo para tipo_item != estandar)

Para preguntas de Tratamiento de Situaciones (TJS) con respuestas graduadas:

```json
{
  "tipo_item": "mas_adecuada",
  "idoneidad_a": 2,
  "idoneidad_b": 4,
  "idoneidad_c": 1,
  "idoneidad_d": 3
}
```

- Rango: 0-4
- 0 = Completamente inadecuada
- 4 = Completamente adecuada
- Para `tipo_item: "menos_adecuada"`, el scoring se invierte: elegir la opción con idoneidad más baja es correcto.

## Validaciones

El comando `ingest_smpi` aplica las siguientes validaciones:

1. **Estructura**: Verifica que sea un array JSON válido.
2. **Campos requeridos**: `contexto` o `titulo`, `enunciado`, opciones A-D, `respuesta_correcta`.
3. **Valores de choices**: `area`, `dificultad`, `tipo_item` deben ser de la lista permitida.
4. **Idoneidad**: Si se especifican, deben ser números 0-4.
5. **Deduplicación**: Identifica enunciados similares (Jaccard ≥ 0.92) y excluye duplicados.

## Detalles Técnicos

### Similitud Jaccard

La deduplicación usa similitud Jaccard de tokens:
- Palabras < 3 caracteres se ignoran
- Se normalizan tildes y puntuación
- Stop words comunes se excluyen: "que", "para", "con", "una", "del", "los", etc.
- Umbral configurable: `--threshold 0.92` (default)

### Estado al Insertar

Las preguntas importadas reciben `estado='publicado'` y `autor='SMPI'`, haciéndolas inmediatamente disponibles para construcción de simulacros.

## Uso

```bash
# Desde archivo JSON
python manage.py ingest_smpi banco_oficial_2026.json

# Desde stdin (útil para integración CI/CD)
cat banco_oficial.json | python manage.py ingest_smpi --stdin

# Validar sin insertar (dry-run)
python manage.py ingest_smpi banco_oficial.json --dry-run

# Cambiar categoría de agrupación
python manage.py ingest_smpi banco_oficial.json --categoria "Banco CNSC 2026"

# Ajustar umbral de similitud
python manage.py ingest_smpi banco_oficial.json --threshold 0.95
```

## Ejemplo Completo

```json
[
  {
    "titulo": "Normas de Convivencia Escolar",
    "contexto": "La Ley 1620 de 2013 establece el Sistema Nacional de Convivencia Escolar. En una institución, se presentó un conflicto entre estudiantes que debe ser mediado según los protocolos establecidos.",
    "enunciado": "¿Cuál de las siguientes acciones se alinea mejor con los principios de la Ley 1620?",
    "opcion_a": "Aplicar sanciones disciplinarias inmediatas sin escuchar a las partes.",
    "opcion_b": "Mediar el conflicto garantizando el derecho a la defensa de ambas partes.",
    "opcion_c": "Reportar directamente al Ministerio sin agotar instancias internas.",
    "opcion_d": "Ignorar el conflicto esperando que se resuelva por sí solo.",
    "respuesta_correcta": "B",
    "area": "general",
    "competencia": "Normativa educativa aplicada",
    "dificultad": "medio",
    "tipo_item": "estandar",
    "justificacion": "La Ley 1620 garantiza el derecho al debido proceso en casos de convivencia escolar.",
    "fuente_normativa": "Ley 1620 de 2013, Art. 2",
    "proceso_cognitivo": "comprension_aplicada",
    "puntaje_validacion": 98
  },
  {
    "contexto": "En una clase de matemáticas, un docente observa que los estudiantes tienen dificultades para aplicar el pensamiento crítico al resolver problemas contextualizados.",
    "enunciado": "¿Cuál estrategia didáctica favorece el desarrollo del pensamiento crítico?",
    "opcion_a": "Memorizar procedimientos sin comprensión.",
    "opcion_b": "Analizar casos reales donde aplica el concepto.",
    "opcion_c": "Resolver ejercicios repetitivos del libro de texto.",
    "opcion_d": "Evitar conexiones con la vida real.",
    "respuesta_correcta": "B",
    "area": "matematicas",
    "competencia": "Didáctica situada",
    "dificultad": "medio",
    "tipo_item": "estandar",
    "proceso_cognitivo": "analisis_situacional"
  },
  {
    "contexto": "Un docente debe elegir cómo responder a una situación de estudiante desconectado de la clase.",
    "enunciado": "¿Qué sería lo MÁS ADECUADO hacer?",
    "opcion_a": "Enviar al estudiante a dirección.",
    "opcion_b": "Etiquetar al estudiante como desinteresado.",
    "opcion_c": "Investigar posibles barreras de aprendizaje y ajustar la estrategia.",
    "opcion_d": "Ignorar la situación y continuar la clase.",
    "respuesta_correcta": "C",
    "area": "general",
    "competencia": "Inclusión y atención a la diversidad",
    "dificultad": "alto",
    "tipo_item": "mas_adecuada",
    "idoneidad_a": 0,
    "idoneidad_b": 1,
    "idoneidad_c": 4,
    "idoneidad_d": 0,
    "proceso_cognitivo": "evaluacion_juicio",
    "puntaje_validacion": 97
  }
]
```

## Integración CI/CD

Para despliegues automáticos del Banco Oficial:

```bash
#!/bin/bash
# deploy_smpi.sh
SMPI_JSON=$(curl -s https://banco-oficial.mineducacion.gov.co/export/items.json)
echo "$SMPI_JSON" | python manage.py ingest_smpi --stdin --categoria "Banco Oficial MEN 2026"
```

## Compatibilidad Futura (CAT/IRT)

El formato está diseñado para ser agnóstico al algoritmo de selección de preguntas:
- **Hoy**: Simulacros con banco fijo (admin manual)
- **Mañana**: Adaptive testing que selecciona preguntas dinámicamente
- El comando de ingesta y el motor de análisis no necesitan cambios
