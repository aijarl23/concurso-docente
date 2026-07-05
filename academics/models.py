from django.db import models


class Category(models.Model):
    CATEGORY_CHOICES = [
        ('pedagogia', 'Pedagogía'),
        ('evaluacion', 'Evaluación'),
        ('inclusion', 'Inclusión'),
        ('normatividad', 'Normatividad'),
        ('tic', 'TIC'),
        ('simulacros', 'Simulacros'),
    ]

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    category_type = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=100, blank=True)
    order = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'

    def __str__(self):
        return self.name


class Module(models.Model):
    DIFFICULTY_CHOICES = [
        ('medium', 'Media'),
        ('high', 'Alta'),
        ('very_high', 'Muy Alta'),
        ('cnsc_expert', 'CNSC Experto'),
    ]

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='modules'
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    short_description = models.CharField(max_length=300)
    description = models.TextField(blank=True)

    difficulty_level = models.CharField(
        max_length=20,
        choices=DIFFICULTY_CHOICES,
        default='high'
    )

    estimated_time_minutes = models.PositiveIntegerField(default=120)

    is_active = models.BooleanField(default=True)
    is_premium = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']
        verbose_name = 'Módulo'
        verbose_name_plural = 'Módulos'

    def __str__(self):
        return self.title


class NormativeResource(models.Model):
    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name='normative_resources'
    )

    title = models.CharField(max_length=200)
    reference = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    official_url = models.URLField(blank=True)

    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Recurso normativo'
        verbose_name_plural = 'Recursos normativos'

    def __str__(self):
        return self.title