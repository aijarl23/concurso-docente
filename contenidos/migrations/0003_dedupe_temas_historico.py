"""Limpieza de datos, una sola vez: elimina Tema duplicados que ya existan en
la base de datos antes de poder agregar la restriccion UNIQUE(modulo, orden)
en la migracion siguiente (0004). Sin esto, 0004 fallaria al aplicarse contra
cualquier base de datos que ya tenga duplicados (el caso real de produccion,
originado por una fusion de Modulo que reasignaba Tema sin revisar 'orden' -
ver dashboard/management/commands/repair_text_quality.py, ya corregido).

Agrupa por (modulo, orden), que es la clave logica real que usa
seed_modulos.update_or_create(modulo=modulo, orden=topic_order, ...), y por
(modulo, titulo) como red de seguridad adicional. Conserva el registro con
descripcion no vacia / activo=True / id mas antiguo (en ese orden de
prioridad) y borra el resto. Tema no tiene ningun modelo que le apunte por
FK en este proyecto, asi que no hay relaciones que reasignar antes de borrar.
"""
from collections import defaultdict

from django.db import migrations


def _score(tema):
    return (bool((tema.descripcion or '').strip()), tema.activo, -tema.id)


def _planear_y_borrar(apps, grupos_por_clave):
    borrados = 0
    vistos_para_eliminar = set()
    for temas in grupos_por_clave.values():
        grupo = [t for t in temas if t.id not in vistos_para_eliminar]
        if len(grupo) < 2:
            continue
        grupo.sort(key=_score, reverse=True)
        eliminar = grupo[1:]
        vistos_para_eliminar.update(t.id for t in eliminar)
        for tema in eliminar:
            tema.delete()
            borrados += 1
    return borrados


def dedupe_temas(apps, schema_editor):
    Tema = apps.get_model('contenidos', 'Tema')

    por_orden = defaultdict(list)
    for tema in Tema.objects.all():
        por_orden[(tema.modulo_id, tema.orden)].append(tema)
    _planear_y_borrar(apps, por_orden)

    # Segunda pasada tras la primera, por si quedaron duplicados con el
    # mismo titulo pero 'orden' distinto.
    por_titulo = defaultdict(list)
    for tema in Tema.objects.all():
        por_titulo[(tema.modulo_id, tema.titulo)].append(tema)
    _planear_y_borrar(apps, por_titulo)


def noop_reverse(apps, schema_editor):
    # No hay forma (ni necesidad) de recrear duplicados al revertir.
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('contenidos', '0002_alter_modulo_tipo'),
    ]

    operations = [
        migrations.RunPython(dedupe_temas, noop_reverse),
    ]
