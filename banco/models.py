from django.db import models


class Categoria(models.Model):
    nombre = models.CharField(max_length=120, unique=True)

    def __str__(self):
        return self.nombre


class Subcategoria(models.Model):
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        related_name='subcategorias'
    )
    nombre = models.CharField(max_length=120)

    def __str__(self):
        return f"{self.categoria.nombre} - {self.nombre}"


class BancoPregunta(models.Model):
    DIFICULTAD_CHOICES = [
        ('basico', 'Basico'),
        ('intermedio', 'Intermedio'),
        ('avanzado', 'Avanzado'),
        ('intermedia', 'Intermedia'),
        ('alta', 'Alta'),
        ('premium', 'Premium'),
        ('elite', 'Elite'),
    ]

    AREA_CHOICES = [
        ('general', 'General'),
        ('ingles', 'Ingles'),
        ('tecnologia', 'Tecnologia e Informatica'),
        ('matematicas', 'Matematicas'),
        ('ciencias_naturales', 'Ciencias Naturales'),
        ('ciencias_sociales', 'Ciencias Sociales'),
        ('lectura_critica', 'Lectura Critica'),
        ('perfil_docente', 'Perfil Docente'),
        ('componente_pedagogico', 'Componente Pedagogico'),
        ('psicotecnico', 'Psicotecnico'),
    ]

    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    subcategoria = models.ForeignKey(
        Subcategoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    titulo = models.CharField(max_length=250, blank=True)
    contexto = models.TextField()
    enunciado = models.TextField()
    opcion_a = models.TextField()
    opcion_b = models.TextField()
    opcion_c = models.TextField()
    opcion_d = models.TextField()
    respuesta_correcta = models.CharField(
        max_length=1,
        choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')]
    )
    justificacion = models.TextField()
    fuente_normativa = models.CharField(max_length=300, blank=True)
    dificultad = models.CharField(
        max_length=20,
        choices=DIFICULTAD_CHOICES,
        default='alta'
    )
    area = models.CharField(max_length=40, choices=AREA_CHOICES, default='general')
    competencia = models.CharField(max_length=120, blank=True)
    nivel_dificultad = models.CharField(max_length=20, choices=DIFICULTAD_CHOICES, default='avanzado')
    hash_contenido = models.CharField(max_length=40, blank=True, db_index=True)
    tiempo_limite_segundos = models.PositiveIntegerField(default=120)
    es_premium = models.BooleanField(default=True)
    activa = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['categoria__nombre', 'subcategoria__nombre', 'id']

    def __str__(self):
        return self.enunciado[:100]
