from __future__ import annotations

import json
from pathlib import Path

from banco.models import BancoPregunta, Categoria, Subcategoria
from simulacros.models import Simulacro

BASE_DIR = Path(__file__).resolve().parents[2]
BANK_PATH = BASE_DIR / "_resources" / "tjs_import" / "tjs_bank_final.json"
CATEGORY_NAME = "Test de Juicios Situacionales (TJS)"
FULL_SIM_NAME = "TJS Concurso Docente CNSC - Banco completo 90 preguntas"


def normalize_title(item: dict) -> str:
    return f"{item['codigo']} - {item['competencia']}"


def run() -> None:
    payload = json.loads(BANK_PATH.read_text(encoding="utf-8"))
    category, _ = Categoria.objects.get_or_create(nombre=CATEGORY_NAME)

    subcategories = {}
    for name in payload["counts"].keys():
        subcategories[name], _ = Subcategoria.objects.get_or_create(
            categoria=category,
            nombre=name,
        )

    created = 0
    updated = 0
    questions_by_competency = {name: [] for name in payload["counts"].keys()}
    all_questions = []

    for item in payload["questions"]:
        question, was_created = BancoPregunta.objects.update_or_create(
            titulo=normalize_title(item),
            defaults={
                "categoria": category,
                "subcategoria": subcategories[item["competencia"]],
                "contexto": item["contexto"],
                "enunciado": item["enunciado"],
                "opcion_a": item["opcion_a"],
                "opcion_b": item["opcion_b"],
                "opcion_c": item["opcion_c"],
                "opcion_d": item["opcion_d"],
                "respuesta_correcta": item["respuesta_correcta"],
                "justificacion": item["justificacion"],
                "fuente_normativa": "CNSC - Competencias comportamentales docentes / Test de Juicios Situacionales",
                "dificultad": "elite",
                "activa": True,
            },
        )
        created += int(was_created)
        updated += int(not was_created)
        questions_by_competency[item["competencia"]].append(question)
        all_questions.append(question)

    full, _ = Simulacro.objects.update_or_create(
        nombre=FULL_SIM_NAME,
        defaults={
            "descripcion": "Banco completo y balanceado de Test de Juicios Situacionales para Concurso Docente CNSC. Incluye 15 items por competencia comportamental.",
            "tipo": "simulacro",
            "tiempo_limite_minutos": 180,
            "puntaje_minimo_aprobacion": 70,
            "activo": True,
        },
    )
    full.preguntas.set(all_questions)

    for competency, questions in sorted(questions_by_competency.items()):
        sim, _ = Simulacro.objects.update_or_create(
            nombre=f"TJS - {competency} - 15 preguntas",
            defaults={
                "descripcion": f"Seccion TJS de nivel avanzado enfocada en {competency}.",
                "tipo": "simulacro",
                "tiempo_limite_minutos": 35,
                "puntaje_minimo_aprobacion": 70,
                "activo": True,
            },
        )
        sim.preguntas.set(questions)

    print(json.dumps({"created": created, "updated": updated, "total": len(all_questions)}, ensure_ascii=False, indent=2))


run()
