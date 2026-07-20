"""fuente_normativa pasa de CharField(max_length=300) a TextField.

Causa raiz del DataError en produccion ("value too long for type character
varying(300)"): el campo se diseno originalmente para citas normativas
cortas (ej. "Decreto 1290 de 2009, art. X"), pero la rubrica CNSC del Banco
Oficial de Preguntas exige fundamentacion normativa/pedagogica completa, que
legitimamente combina varias referencias con una breve explicacion de cada
una (ej. "Decreto 1290 de 2009 (la evaluacion como proceso permanente...) y
los Lineamientos Curriculares de Matematicas del MEN sobre..."). 4 de los primeros
30 items ya superan los 300 caracteres (hasta 357) sin ser un caso atipico -
es el patron esperado de este contenido, y modulos/temas futuros lo repetiran.
No hay ninguna razon de negocio para limitar esta cita a 300 caracteres, asi
que se usa TextField (igual que justificacion, contexto y enunciado) en vez
de ampliar el limite a un numero arbitrario mayor.
"""
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banco', '0006_alter_bancopregunta_dificultad_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bancopregunta',
            name='fuente_normativa',
            field=models.TextField(blank=True),
        ),
    ]
