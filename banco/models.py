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
        ('ingles', 'Inglés'),
        ('tecnologia', 'Tecnología e Informática'),
        ('matematicas', 'Matemáticas'),
        ('ciencias_naturales', 'Ciencias Naturales'),
        ('ciencias_sociales', 'Ciencias Sociales'),
        ('lectura_critica', 'Lectura Crítica'),
        ('perfil_docente', 'Rol Docente'),
        ('componente_pedagogico', 'Competencias Pedagógicas'),
        ('psicotecnico', 'Análisis de Casos'),
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
    TIPO_ITEM_CHOICES = [
        ('estandar', 'Pregunta estandar (correcto/incorrecto)'),
        ('mas_adecuada', 'TJS - Respuesta MAS adecuada'),
        ('menos_adecuada', 'TJS - Respuesta MENOS adecuada'),
    ]
    tipo_item = models.CharField(max_length=20, choices=TIPO_ITEM_CHOICES, default='estandar')
    idoneidad_a = models.PositiveSmallIntegerField(null=True, blank=True)
    idoneidad_b = models.PositiveSmallIntegerField(null=True, blank=True)
    idoneidad_c = models.PositiveSmallIntegerField(null=True, blank=True)
    idoneidad_d = models.PositiveSmallIntegerField(null=True, blank=True)
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

    # Trazabilidad (Constitucion Academica, Cap. 12 - Control de versiones)
    PROCESO_COGNITIVO_CHOICES = [
        ('identificacion', 'Nivel 1 - Identificacion'),
        ('comprension_aplicada', 'Nivel 2 - Comprension aplicada'),
        ('analisis_situacional', 'Nivel 3 - Analisis situacional'),
        ('evaluacion_juicio', 'Nivel 4 - Evaluacion y juicio'),
    ]
    ESTADO_CHOICES = [
        ('borrador', 'Borrador'),
        ('en_revision', 'En revision'),
        ('aprobado', 'Aprobado'),
        ('publicado', 'Publicado'),
        ('rechazado', 'Rechazado'),
    ]
    proceso_cognitivo = models.CharField(
        max_length=25, choices=PROCESO_COGNITIVO_CHOICES, blank=True
    )
    version = models.PositiveIntegerField(default=1)
    autor = models.CharField(max_length=60, default='IA')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='borrador')
    puntaje_validacion = models.PositiveSmallIntegerField(null=True, blank=True)

    class Meta:
        ordering = ['categoria__nombre', 'subcategoria__nombre', 'id']

    def __str__(self):
        return self.enunciado[:100]

    @property
    def usa_idoneidad_graduada(self):
        return self.idoneidad_a is not None

    def idoneidad_de(self, letra):
        if not letra or not self.usa_idoneidad_graduada:
            return None
        return getattr(self, f'idoneidad_{letra.lower()}', None)

    def puntos_por_respuesta(self, letra):
        """Fraccion 0-1 de credito por la opcion elegida.

        En items MAS_ADECUADA el credito crece con la idoneidad de la opcion
        elegida (se premia elegir la mejor accion). En items MENOS_ADECUADA
        el juicio correcto es identificar la opcion de MENOR idoneidad, asi
        que el credito se invierte: elegir la peor opcion (idoneidad 0) es
        el acierto pleno, elegir la mejor opcion es el fallo total.
        Si la pregunta no usa idoneidad graduada, cae al esquema binario
        (1.0 si coincide con respuesta_correcta, 0.0 si no).
        """
        idoneidad = self.idoneidad_de(letra)
        if idoneidad is None:
            return 1.0 if letra == self.respuesta_correcta else 0.0
        if self.tipo_item == 'menos_adecuada':
            return (4 - idoneidad) / 4
        return idoneidad / 4
