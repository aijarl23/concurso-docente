from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.db.models import Avg

from .models import Modulo
from banco.models import BancoPregunta
from simulacros.models import Simulacro
from seguimiento.models import Intento


@login_required
def dashboard(request):
    modulos = Modulo.objects.filter(activo=True).prefetch_related('temas')
    total_modulos = modulos.count()
    intentos_usuario = Intento.objects.filter(usuario=request.user, estado='completado')
    simulacros_completados = intentos_usuario.values('simulacro_id').distinct().count()
    promedio = intentos_usuario.aggregate(valor=Avg('puntaje_obtenido'))['valor'] or 0
    total_simulacros = Simulacro.objects.filter(activo=True).count()
    progreso = int((simulacros_completados / total_simulacros) * 100) if total_simulacros else 0
    metricas = {
        'modulos': total_modulos,
        'preguntas': BancoPregunta.objects.filter(activa=True).count(),
        'simulacros': total_simulacros,
        'completados': simulacros_completados,
        'promedio': round(float(promedio), 1),
        'progreso': min(progreso, 100),
    }
    return render(request, 'contenidos/dashboard.html', {'modulos': modulos, 'metricas': metricas})


@login_required
def detalle_modulo(request, modulo_id):
    modulo = get_object_or_404(Modulo.objects.prefetch_related('temas'), id=modulo_id, activo=True)
    return render(request, 'contenidos/detalle_modulo.html', {'modulo': modulo})