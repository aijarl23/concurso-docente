from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.db.models import Avg

from .models import Modulo
from banco.models import BancoPregunta
from simulacros.models import Simulacro
from seguimiento.analitica import analizar_historial
from seguimiento.models import Intento

# Estos dos tipos de modulo se venden en el catalogo pero no tienen
# contenido de ruta tematica (temas/subtemas) - su "contenido" es el
# analisis en vivo del historial del usuario, no texto estatico.
TIPOS_CON_ANALISIS = {'analisis_desempeno', 'plan_fortalecimiento'}


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


def _resolver_simulacro_del_modulo(modulo):
    """Encuentra el/los Simulacro que corresponden a este Modulo, usando
    dashboard.question_generator.MODULES como fuente de verdad para pasar de
    Modulo.tipo (contenidos) a academics.Module.slug (con el que Simulacro.module
    esta enlazado; ver banco/management/commands/sync_banco_simulacros.py).

    No asume nada sobre que modulos existen: cualquier modulo nuevo agregado a
    MODULES queda resuelto automaticamente, sin tocar esta funcion.

    Devuelve (simulacro_unico_o_None, hay_varios_simulacros_bool):
    - 1 Simulacro activo para el slug -> ese es "el" simulacro del modulo.
    - 0 -> el modulo todavia no tiene banco de preguntas propio (banco oficial
      pendiente, o es un modulo de solo-analisis que nunca tiene Simulacro).
    - >1 -> modulo con varios simulacros propios (hoy: Competencias
      Disciplinares, uno por area); se resuelve aparte via seleccionar_area.
    """
    from dashboard.question_generator import MODULES

    entry = next((m for m in MODULES if m['tipo'] == modulo.tipo), None)
    if not entry:
        return None, False

    simulacros_modulo = list(
        Simulacro.objects.filter(module__slug=entry['slug'], activo=True).order_by('id')
    )
    if len(simulacros_modulo) == 1:
        return simulacros_modulo[0], False
    if len(simulacros_modulo) > 1:
        return None, True
    return None, False


@login_required
def detalle_modulo(request, modulo_id):
    modulo = get_object_or_404(Modulo.objects.prefetch_related('temas'), id=modulo_id, activo=True)
    analisis = None
    if modulo.tipo in TIPOS_CON_ANALISIS:
        analisis = analizar_historial(request.user)
    simulacro_propio, simulacros_multiples = _resolver_simulacro_del_modulo(modulo)
    return render(request, 'contenidos/detalle_modulo.html', {
        'modulo': modulo,
        'analisis': analisis,
        'simulacro_propio': simulacro_propio,
        'simulacros_multiples': simulacros_multiples,
    })