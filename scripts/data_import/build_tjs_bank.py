from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


COMPETENCIES = {
    "Comunicación asertiva": "CA",
    "Liderazgo": "LID",
    "Trabajo en equipo": "TE",
    "Orientación al logro": "OL",
    "Iniciativa": "INI",
    "Manejo de la información": "MI",
}

TARGET_PER_COMPETENCY = 15


def normalize_prompt(tipo: str) -> str:
    tipo_norm = tipo.upper()
    if "MENOS" in tipo_norm:
        return "¿Cuál es la respuesta MENOS adecuada ante esta situación?"
    return "¿Cuál es la respuesta MÁS adecuada ante esta situación?"


def build_generated_item(competencia: str, ordinal: int, seed: dict) -> dict:
    prefix = COMPETENCIES[competencia]
    menos = seed.get("menos", False)
    tipo = "Respuesta MENOS ADECUADA" if menos else "Respuesta MÁS ADECUADA"
    code = f"{prefix}-COM-{ordinal:03d}"
    contexto = (
        f"PERFIL DEL DOCENTE: {seed['perfil']} "
        f"SITUACIÓN {seed['situacion']} "
        f"El caso exige valorar simultáneamente el efecto pedagógico inmediato, "
        f"la legitimidad institucional de la actuación y las consecuencias éticas "
        f"de la decisión ante estudiantes, familias y equipo docente."
    )
    if menos:
        respuesta = seed["mala_letra"]
        opciones = seed["opciones_menos"]
        justificacion = (
            f"La opción {respuesta} es la menos adecuada porque {seed['razon_mala']} "
            f"En un TJS de alta exigencia no basta con elegir una respuesta formalmente "
            f"defendible: se debe identificar la actuación que preserva derechos, evidencia, "
            f"clima institucional y responsabilidad profesional. Las demás opciones, aunque "
            f"perfectibles, contienen mecanismos de diálogo, verificación o mitigación."
        )
    else:
        respuesta = seed["buena_letra"]
        opciones = seed["opciones_mas"]
        justificacion = (
            f"La opción {respuesta} es la más adecuada porque {seed['razon_buena']} "
            f"Responde al dilema con proporcionalidad, lectura del contexto, uso de evidencia "
            f"y cuidado de las relaciones pedagógicas. Las demás opciones son insuficientes "
            f"por ser evasivas, reactivas, autoritarias o por trasladar la responsabilidad sin "
            f"agotar la actuación profesional esperada."
        )

    return {
        "source_file": "Ítem generado para completar matriz TJS",
        "numero": ordinal,
        "codigo": code,
        "competencia": competencia,
        "tipo_item": tipo,
        "nivel": seed.get("nivel", "Avanzado TJS Concurso Docente"),
        "contexto": contexto,
        "enunciado": normalize_prompt(tipo),
        "opcion_a": opciones["A"],
        "opcion_b": opciones["B"],
        "opcion_c": opciones["C"],
        "opcion_d": opciones["D"],
        "respuesta_correcta": respuesta,
        "justificacion": justificacion,
        "generated": True,
    }


def base_options(competencia: str, focus: str) -> dict:
    return {
        "A": f"Actuar de inmediato con una intervención técnica, reconocer los hechos verificables, abrir un espacio de diálogo y proponer un acuerdo de seguimiento centrado en {focus}.",
        "B": "Evitar intervenir para no aumentar la tensión, esperar a que la coordinación defina el procedimiento y limitarse a cumplir las instrucciones posteriores.",
        "C": "Imponer una decisión unilateral ante el grupo, dejando claro que la autoridad docente prevalece cuando hay presión institucional o desacuerdo entre actores.",
        "D": "Trasladar el caso completo a rectoría mediante un informe extenso, sin realizar ninguna acción pedagógica inicial ni recoger información adicional.",
    }


def menos_options(competencia: str, focus: str) -> dict:
    return {
        "A": f"Reconocer la tensión, proteger a los estudiantes involucrados, contrastar información y acordar una respuesta pedagógica proporcional centrada en {focus}.",
        "B": "Pedir apoyo institucional cuando el caso exceda la competencia individual, dejando evidencia de los hechos y de las acciones pedagógicas realizadas.",
        "C": "Actuar solo con base en impresiones personales, desestimar las voces que contradicen la primera versión y cerrar el caso para evitar desgaste institucional.",
        "D": "Convocar un diálogo breve con los actores pertinentes, diferenciar hechos de interpretaciones y definir un seguimiento verificable.",
    }


SEEDS = {
    "Liderazgo": [
        ("Docente líder de área sin cargo directivo", "un equipo de docentes rechaza implementar ajustes razonables porque considera que aumentan la carga laboral, aunque hay evidencias de estudiantes que no acceden plenamente a la evaluación.", "acuerdos inclusivos verificables"),
        ("Docente provisional con alto reconocimiento estudiantil", "el consejo académico evita discutir resultados críticos de convivencia porque teme afectar la imagen institucional ante la Secretaría de Educación.", "mejora institucional basada en evidencia"),
    ],
    "Trabajo en equipo": [
        ("Docente nuevo en una institución rural", "dos áreas deben diseñar una secuencia interdisciplinar, pero cada una defiende sus contenidos y acusa a la otra de no comprender las necesidades del contexto.", "integración curricular realista"),
        ("Docente de secundaria con experiencia", "un proyecto transversal está atrasado porque los responsables no comparten avances y cada equipo maneja criterios distintos de calidad.", "coordinación y corresponsabilidad"),
        ("Docente orientador de semillero académico", "un colega se apropia de productos elaborados por el equipo y presenta los avances como logro individual ante directivos.", "reconocimiento del trabajo colectivo"),
        ("Docente de matemáticas en jornada única", "el equipo acuerda una estrategia común, pero varios docentes la aplican de forma fragmentada y los estudiantes reciben mensajes contradictorios.", "consistencia pedagógica"),
        ("Docente encargado de feria institucional", "faltan dos días para el evento y un área informa que no entregará evidencias porque considera que la planeación inicial fue deficiente.", "recuperación colaborativa del proceso"),
        ("Docente de media técnica", "un conflicto entre docentes antiguos y nuevos paraliza una decisión sobre criterios de evaluación común.", "mediación entre perspectivas"),
        ("Docente de aula multigrado", "el equipo rural debe distribuir materiales escasos, pero cada sede prioriza sus propias urgencias sin mirar el impacto global.", "equidad en el uso de recursos"),
        ("Docente coordinador de proyecto lector", "la estrategia depende de aportes de varias áreas, pero solo una ha cumplido y empieza a reclamar control total del proceso.", "corresponsabilidad sin ruptura del equipo"),
    ],
    "Orientación al logro": [
        ("Docente de grado once", "los resultados de simulacros muestran mejora en memorización, pero bajo desempeño en lectura inferencial y uso de evidencia.", "metas de aprendizaje medibles"),
        ("Docente de básica secundaria", "la institución celebra una mejora leve en promedios, aunque los estudiantes con mayor rezago siguen sin avances significativos.", "progreso de todos los grupos"),
        ("Docente de ciencias", "un plan de mejoramiento tiene muchas actividades, pero no define indicadores ni momentos de revisión.", "seguimiento de resultados"),
        ("Docente de lenguaje", "el grupo obtiene buenos resultados en tareas de baja complejidad, pero falla cuando debe justificar decisiones con información del texto.", "desempeño transferible"),
        ("Docente de primaria", "la presión por subir indicadores lleva al equipo a entrenar solo preguntas tipo prueba y abandonar procesos formativos de fondo.", "aprendizaje sostenible"),
        ("Docente de educación media", "un estudiante con alto potencial baja su rendimiento porque las tareas no le exigen análisis ni producción argumentativa.", "retos diferenciados"),
        ("Docente de matemáticas", "la institución tiene metas ambiciosas, pero los docentes no usan datos por grupo ni por habilidad para ajustar la enseñanza.", "uso pedagógico de datos"),
        ("Docente jefe de área", "una estrategia exitosa se aplica igual en todos los cursos sin considerar diferencias de contexto, ritmo y prerrequisitos.", "adaptación de la mejora"),
    ],
    "Iniciativa": [
        ("Docente provisional en zona urbana", "detecta que los estudiantes nuevos no reciben inducción académica y por eso repiten errores administrativos y pedagógicos durante semanas.", "soluciones viables de bajo costo"),
        ("Docente de escuela rural dispersa", "observa que la conectividad irregular impide sostener tareas digitales, pero hay recursos impresos subutilizados en biblioteca.", "respuesta creativa al contexto"),
        ("Docente de ciencias sociales", "nota que las familias desconocen el SIEE y esto genera reclamos tardíos que podrían prevenirse con orientación oportuna.", "prevención de conflictos"),
        ("Docente de aula inclusiva", "un estudiante con barreras de aprendizaje depende de adaptaciones informales que solo conoce un docente.", "continuidad pedagógica"),
        ("Docente de jornada tarde", "los estudiantes llegan tarde de forma recurrente por problemas de transporte y el equipo solo registra sanciones sin analizar causas.", "análisis proactivo de causas"),
        ("Docente de tecnología", "la institución tiene datos dispersos de asistencia, desempeño y convivencia, pero nadie los cruza para anticipar riesgo escolar.", "alertas tempranas"),
        ("Docente de educación artística", "un grupo con baja participación mejora cuando las tareas se conectan con problemas de la comunidad, pero la estrategia no se documenta.", "innovación documentada"),
        ("Docente de lengua castellana", "varios estudiantes talentosos no participan en eventos académicos porque nadie sistematiza convocatorias ni acompaña postulaciones.", "gestión de oportunidades"),
    ],
    "Manejo de la información": [
        ("Docente director de grupo", "recibe versiones contradictorias sobre una agresión verbal entre estudiantes y una familia exige sanción inmediata antes de escuchar a todos.", "verificación responsable de información"),
        ("Docente de ciencias naturales", "un informe institucional usa promedios generales para concluir que no hay rezago, pero usted observa brechas fuertes por subgrupos.", "lectura crítica de datos"),
        ("Docente de matemáticas", "la coordinación solicita publicar una lista de estudiantes con bajo desempeño para presionar asistencia a refuerzos.", "protección de datos sensibles"),
        ("Docente de humanidades", "un colega comparte por chat capturas de calificaciones y comentarios sobre estudiantes para pedir opinión rápida al equipo.", "confidencialidad y uso pertinente"),
        ("Docente de grado noveno", "una herramienta digital genera reportes automáticos, pero varios datos aparecen duplicados o sin fecha de actualización.", "calidad de la información"),
        ("Docente encargado de seguimiento", "debe decidir si un estudiante requiere apoyo adicional con base en observaciones docentes, registros de asistencia y resultados de evaluación.", "triangulación de evidencia"),
        ("Docente de media", "un directivo solicita una explicación simple de bajos resultados, pero los datos muestran causas múltiples: asistencia, lectura y cambios docentes.", "interpretación no reduccionista"),
        ("Docente de primaria", "una madre pide conocer los resultados comparativos de otros estudiantes para demostrar que su hijo fue evaluado injustamente.", "reserva de información de terceros"),
        ("Docente de ética", "un rumor en redes sociales señala a un estudiante como responsable de daño institucional y varios compañeros exigen expulsión.", "distinción entre rumor y evidencia"),
    ],
}


def seed_to_item(competencia: str, ordinal: int, seed_tuple: tuple[str, str, str], menos: bool) -> dict:
    perfil, situacion, focus = seed_tuple
    seed = {
        "perfil": perfil,
        "situacion": situacion,
        "nivel": "Avanzado TJS Concurso Docente",
        "menos": menos,
        "buena_letra": "A",
        "mala_letra": "C",
        "opciones_mas": base_options(competencia, focus),
        "opciones_menos": menos_options(competencia, focus),
        "razon_buena": f"integra lectura del contexto, acción profesional y seguimiento sobre {focus}, sin evadir la responsabilidad ni sustituir el diálogo por imposición.",
        "razon_mala": f"reduce el caso a una impresión inicial, desconoce evidencia contradictoria y compromete {focus} al cerrar prematuramente el análisis.",
    }
    return build_generated_item(competencia, ordinal, seed)


def main() -> int:
    source = json.loads(Path("work/tjs_questions_parsed.json").read_text(encoding="utf-8"))["questions"]
    existing = []
    for item in source:
        tipo = item.get("tipo_item", "")
        item["enunciado"] = item.get("enunciado") or normalize_prompt(tipo)
        item["generated"] = False
        existing.append(item)

    counts = Counter(item["competencia"] for item in existing)
    generated = []
    for competencia, prefix in COMPETENCIES.items():
        current = counts[competencia]
        needed = TARGET_PER_COMPETENCY - current
        if needed <= 0:
            continue
        seeds = SEEDS[competencia]
        for offset in range(needed):
            ordinal = current + offset + 1
            generated.append(
                seed_to_item(
                    competencia,
                    ordinal,
                    seeds[offset],
                    menos=(offset % 3 == 1),
                )
            )

    bank = existing + generated
    final_counts = Counter(item["competencia"] for item in bank)
    out = {
        "target_per_competency": TARGET_PER_COMPETENCY,
        "counts": dict(sorted(final_counts.items())),
        "source_questions": len(existing),
        "generated_questions": len(generated),
        "total_questions": len(bank),
        "questions": bank,
    }
    Path("work/tjs_bank_final.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k: out[k] for k in ["source_questions", "generated_questions", "total_questions", "counts"]}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
