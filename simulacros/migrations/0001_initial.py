# Generated manually to restore the missing initial migration for simulacros.

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('banco', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Simulacro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=250)),
                ('descripcion', models.TextField()),
                ('tipo', models.CharField(choices=[('simulacro', 'Simulacro'), ('diagnostico', 'Diagnostico'), ('tematico', 'Tematico'), ('tjs', 'TJS Premium'), ('elite', 'CNSC Elite')], default='simulacro', max_length=20)),
                ('tiempo_limite_minutos', models.PositiveIntegerField(default=120)),
                ('puntaje_minimo_aprobacion', models.PositiveIntegerField(default=70)),
                ('activo', models.BooleanField(default=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('preguntas', models.ManyToManyField(related_name='simulacros', to='banco.bancopregunta')),
            ],
            options={
                'ordering': ['nombre'],
            },
        ),
    ]
