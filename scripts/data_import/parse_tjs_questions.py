from __future__ import annotations

import json
import re
from pathlib import Path


INDEX_RE = re.compile(r"^(?:PREGUNTA|Pregunta)\s+(\d+)\s+([A-Z]{2,4}(?:-[A-Z0-9]+)+)$")
COMP_RE = re.compile(
    r"^COMPETENCIA(?: EVALUADA)?:\s*(.*?)\s*\|\s*TIPO:\s*(.*?)(?:\s*\|\s*NIVEL:\s*(.*))?$",
    re.I,
)
OPTION_RE = re.compile(r"^([A-D])\s*\|\s*(.+)$")
ANSWER_RE = re.compile(r"^(?:RESPUESTA CORRECTA|Respuesta correcta|Clave|Respuesta)\s*\|?\s*:?\s*([A-D])\b", re.I)
CODE_IN_TABLE_RE = re.compile(r"^(\d+)\s*\|\s*([A-Z]{2,4}(?:-[A-Z0-9]+)+)\s*\|\s*(.*?)\s*\|\s*(.*)$")


def normalize(text: str) -> str:
    return " ".join(text.split())


def parse_record(record: dict) -> list[dict]:
    blocks = record["blocks"]
    table_codes: list[tuple[int, str]] = []
    for block in blocks:
        clean = normalize(block)
        row = CODE_IN_TABLE_RE.match(clean)
        if row:
            table_codes.append((int(row.group(1)), row.group(2)))
            continue
        index = INDEX_RE.match(clean)
        if index:
            table_codes.append((int(index.group(1)), index.group(2)))

    questions: list[dict] = []
    current: dict | None = None
    current_field = "contexto"
    next_code_index = 0

    def flush() -> None:
        nonlocal current
        if current:
            for key in ["contexto", "enunciado", "justificacion"]:
                current[key] = normalize(current.get(key, ""))
            for key in ["opcion_a", "opcion_b", "opcion_c", "opcion_d"]:
                current[key] = normalize(current.get(key, ""))
            questions.append(current)
        current = None

    for block in blocks:
        text = normalize(block)
        comp = COMP_RE.match(text)
        if comp:
            flush()
            numero = table_codes[next_code_index][0] if next_code_index < len(table_codes) else len(questions) + 1
            codigo = table_codes[next_code_index][1] if next_code_index < len(table_codes) else f"{record['name']}#{numero}"
            next_code_index += 1
            current = {
                "source_file": record["name"],
                "numero": numero,
                "codigo": codigo,
                "competencia": normalize(comp.group(1)),
                "tipo_item": normalize(comp.group(2)),
                "nivel": normalize(comp.group(3) or "Avanzado TJS Concurso Docente"),
                "contexto": "",
                "enunciado": "",
                "opcion_a": "",
                "opcion_b": "",
                "opcion_c": "",
                "opcion_d": "",
                "respuesta_correcta": "",
                "justificacion": "",
            }
            current_field = "contexto"
            continue

        if INDEX_RE.match(text) or CODE_IN_TABLE_RE.match(text):
            continue

        if not current:
            continue

        answer = ANSWER_RE.match(text)
        if answer:
            current["respuesta_correcta"] = answer.group(1).upper()
            tail = text[answer.end():].strip(" :-")
            if tail:
                current["justificacion"] += " " + tail
            current_field = "justificacion"
            continue

        opt = OPTION_RE.match(text)
        if opt:
            option_letter = opt.group(1).upper()
            option_text = opt.group(2)
            if "✓" in option_text or "CORRECTA" in option_text.upper():
                current["respuesta_correcta"] = option_letter
                option_text = (
                    option_text.replace("✓", "")
                    .replace("CORRECTA", "")
                    .replace("Correcta", "")
                    .strip(" .;-")
                )
            current[f"opcion_{option_letter.lower()}"] = option_text
            current_field = f"opcion_{opt.group(1).lower()}"
            continue

        lower = text.lower()
        if lower.startswith("perfil del docente"):
            current["contexto"] += " " + text
            current_field = "contexto"
            continue
        if lower.startswith("situación") or lower.startswith("situacion") or lower.startswith("contexto"):
            current["contexto"] += " " + re.sub(r"^(SITUACIÓN|SITUACION|Contexto)[:\s]+", "", text, flags=re.I)
            current_field = "contexto"
            continue
        if lower.startswith("pregunta") or lower.startswith("¿cuál") or lower.startswith("cual"):
            current["enunciado"] += " " + text
            current_field = "enunciado"
            continue
        if (
            lower.startswith("justificación")
            or lower.startswith("justificacion")
            or lower.startswith("retroalimentación")
            or lower.startswith("explicación pedagógica")
            or lower.startswith("explicacion pedagogica")
            or lower.startswith("análisis pedagógico")
            or lower.startswith("analisis pedagogico")
        ):
            current["justificacion"] += " " + re.sub(r"^[^:]+:\s*", "", text)
            current_field = "justificacion"
            continue

        if current_field in current:
            current[current_field] += " " + text

    flush()
    return questions


def main() -> int:
    data = json.loads(Path("work/tjs_docx_extract.json").read_text(encoding="utf-8"))
    parsed = []
    seen_texts = set()
    duplicate_files = []
    for record in data:
        signature = record["text"]
        if signature in seen_texts:
            duplicate_files.append(record["name"])
            continue
        seen_texts.add(signature)
        parsed.extend(parse_record(record))

    out = {
        "duplicate_files_skipped": duplicate_files,
        "questions": parsed,
    }
    Path("work/tjs_questions_parsed.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"questions={len(parsed)} duplicates_skipped={len(duplicate_files)}")
    missing = [
        q["codigo"]
        for q in parsed
        if not all(q.get(k) for k in ["competencia", "contexto", "opcion_a", "opcion_b", "opcion_c", "opcion_d", "respuesta_correcta"])
    ]
    print("missing_required=", missing[:30], "count=", len(missing))
    by_prefix: dict[str, int] = {}
    for q in parsed:
        prefix = q["codigo"].split("-")[0]
        by_prefix[prefix] = by_prefix.get(prefix, 0) + 1
    print("by_prefix=", dict(sorted(by_prefix.items())))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
