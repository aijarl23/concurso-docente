"""Restriccion permanente a nivel de base de datos: nunca puede volver a
existir mas de un Tema con el mismo (modulo, orden). Esta es la clave logica
real que usa seed_modulos.update_or_create(modulo=modulo, orden=topic_order,
...) - antes de esta migracion, un bug en cualquier comando (o en un futuro
script) podia crear duplicados en silencio y el error solo aparecia semanas
despues, en un deploy no relacionado. Con este UNIQUE, cualquier intento de
crear un duplicado falla de inmediato con IntegrityError, en el mismo lugar
donde se origina el problema.

Depende de 0003_dedupe_temas_historico, que limpia los duplicados existentes
antes de que esta restriccion se intente aplicar.
"""
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenidos', '0003_dedupe_temas_historico'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='tema',
            constraint=models.UniqueConstraint(fields=['modulo', 'orden'], name='unique_tema_modulo_orden'),
        ),
    ]
