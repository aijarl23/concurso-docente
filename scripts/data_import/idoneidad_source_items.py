# -*- coding: utf-8 -*-
"""Idoneidad graduada (0-4) para los 55 items TJS "fuente" (extraidos de
referencias reales), asignada leyendo la justificacion propia de cada item.
Tambien corrige un bug real detectado: CA-002 tenia respuesta_correcta='B'
pero su propia justificacion describe la opcion A como la correcta y la B
como la que expone informacion confidencial - se corrige a 'A'.
"""

CORRECCIONES_RESPUESTA = {
    "CA-002": "A",
    "OL-001": "B",
    # OL-COM-012 es uno de los 35 items reescritos (rewritten_tjs_items.py),
    # no un item "fuente", pero la correccion de respuesta_correcta se
    # centraliza aqui por simplicidad: el contenido reescrito marca la
    # opcion B como la menos adecuada, pero la plantilla original tenia
    # 'C' fijo para todo item tipo MENOS-ADECUADA del mismo grupo.
    "OL-COM-012": "B",
}

IDONEIDAD = {
    "CA-001": {"a": 1, "b": 4, "c": 3, "d": 0},
    "CA-002": {"a": 4, "b": 0, "c": 1, "d": 2},
    "CA-003": {"a": 0, "b": 4, "c": 2, "d": 2},
    "CA-B1-001": {"a": 1, "b": 4, "c": 2, "d": 3},
    "CA-B1-002": {"a": 3, "b": 4, "c": 0, "d": 4},
    "CA-B1-003": {"a": 0, "b": 4, "c": 2, "d": 2},
    "CA-B1-004": {"a": 0, "b": 4, "c": 0, "d": 1},
    "CA-B2-001": {"a": 2, "b": 4, "c": 1, "d": 2},
    "CA-B2-002": {"a": 2, "b": 4, "c": 2, "d": 1},
    "CA-B2-003": {"a": 0, "b": 4, "c": 4, "d": 4},
    "CA-B2-004": {"a": 1, "b": 4, "c": 3, "d": 2},
    "CA-B2-005": {"a": 3, "b": 4, "c": 3, "d": 1},
    "CA-B2-006": {"a": 0, "b": 4, "c": 4, "d": 4},
    "CA-B2-007": {"a": 0, "b": 4, "c": 2, "d": 1},
    "CA-B2-008": {"a": 0, "b": 4, "c": 1, "d": 2},
    "INI-001": {"a": 0, "b": 1, "c": 4, "d": 2},
    "INI-002": {"a": 0, "b": 4, "c": 1, "d": 1},
    "INI-003": {"a": 0, "b": 4, "c": 3, "d": 1},
    "INI-B1-001": {"a": 0, "b": 4, "c": 2, "d": 2},
    "INI-B1-002": {"a": 0, "b": 4, "c": 4, "d": 4},
    "INI-B1-003": {"a": 0, "b": 4, "c": 1, "d": 2},
    "INI-B2-001": {"a": 0, "b": 4, "c": 2, "d": 1},
    "LID-001": {"a": 0, "b": 4, "c": 2, "d": 1},
    "LID-002": {"a": 0, "b": 4, "c": 4, "d": 3},
    "LID-B1-001": {"a": 0, "b": 4, "c": 2, "d": 1},
    "LID-B1-002": {"a": 0, "b": 4, "c": 4, "d": 4},
    "LID-B1-003": {"a": 0, "b": 4, "c": 2, "d": 1},
    "LID-B1-004": {"a": 0, "b": 4, "c": 2, "d": 2},
    "LID-B2-001": {"a": 1, "b": 4, "c": 1, "d": 2},
    "LID-B2-002": {"a": 1, "b": 4, "c": 2, "d": 0},
    "LID-B2-003": {"a": 0, "b": 4, "c": 4, "d": 4},
    "LID-B2-004": {"a": 0, "b": 4, "c": 1, "d": 2},
    "LID-B2-005": {"a": 0, "b": 4, "c": 2, "d": 1},
    "LID-B2-006": {"a": 0, "b": 4, "c": 1, "d": 1},
    "LID-B2-007": {"a": 1, "b": 4, "c": 2, "d": 1},
    "MI-001": {"a": 0, "b": 4, "c": 3, "d": 1},
    "MI-002": {"a": 0, "b": 4, "c": 3, "d": 3},
    "MI-B1-001": {"a": 1, "b": 4, "c": 0, "d": 1},
    "MI-B1-002": {"a": 0, "b": 4, "c": 2, "d": 2},
    "MI-B1-003": {"a": 1, "b": 4, "c": 0, "d": 3},
    "MI-B2-001": {"a": 0, "b": 4, "c": 2, "d": 1},
    "OL-001": {"a": 0, "b": 4, "c": 3, "d": 3},
    "OL-002": {"a": 1, "b": 4, "c": 1, "d": 0},
    "OL-003": {"a": 2, "b": 1, "c": 4, "d": 2},
    "OL-B1-001": {"a": 0, "b": 4, "c": 1, "d": 2},
    "OL-B1-002": {"a": 0, "b": 4, "c": 3, "d": 3},
    "OL-B1-003": {"a": 1, "b": 4, "c": 1, "d": 2},
    "OL-B2-001": {"a": 0, "b": 4, "c": 2, "d": 2},
    "TE-001": {"a": 1, "b": 4, "c": 1, "d": 1},
    "TE-002": {"a": 4, "b": 0, "c": 3, "d": 3},
    "TE-B1-001": {"a": 0, "b": 4, "c": 1, "d": 1},
    "TE-B1-002": {"a": 0, "b": 4, "c": 2, "d": 1},
    "TE-B1-003": {"a": 0, "b": 4, "c": 3, "d": 3},
    "TE-B2-001": {"a": 1, "b": 4, "c": 1, "d": 2},
    "TE-B2-002": {"a": 0, "b": 4, "c": 4, "d": 3},
}
