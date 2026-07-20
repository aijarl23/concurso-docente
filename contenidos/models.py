from django.db import models


class Modulo(models.Model):
    # Valores legacy (filas inactivas, se conservan solo para no romper el
    # admin sobre datos historicos) + los 11 tipos reales, sincronizados con
    # dashboard/question_generator.py:MODULES (fuente de verdad del catalogo).
    TIPOS = [
        ('lectura_tjs', 'Lectura Crítica (legacy)'),
        ('perfil_docente', 'Rol Docente (legacy)'),
        ('pedagogico', 'Competencias Pedagógicas (legacy)'),
        ('psicotecnico', 'Análisis de Casos (legacy)'),
        ('diagnostico_inicial', 'Diagnóstico Inicial'),
        ('lectura_critica_aplicada', 'Lectura Crítica'),
        ('normativa_contexto', 'Normatividad Educativa'),
        ('inclusion_educativa', 'Inclusión Educativa'),
        ('competencias_pedagogicas', 'Competencias Pedagógicas'),
        ('competencias_tjs', 'Análisis de Casos'),
        ('gestion_escolar', 'Gestión Escolar'),
        ('simulacros_area', 'Competencias Disciplinares'),
        ('simulacro_final', 'Simulacro Integral'),
        ('analisis_desempeno', 'Análisis del Desempeño'),
        ('plan_fortalecimiento', 'Plan de Fortalecimiento'),
    ]

    titulo = models.CharField(max_length=200)
    tipo = models.CharField(max_length=30, choices=TIPOS, unique=True)
    descripcion = models.TextField()
    orden = models.PositiveIntegerField(default=1)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ['orden']

    def __str__(self):
        return self.titulo


class Tema(models.Model):
    modulo = models.ForeignKey(
        Modulo,
        on_delete=models.CASCADE,
        related_name='temas'
    )

    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    orden = models.PositiveIntegerField(default=1)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ['orden']
        constraints = [
            models.UniqueConstraint(fields=['modulo', 'orden'], name='unique_tema_modulo_orden'),
        ]

    def __str__(self):
        return self.titulo
