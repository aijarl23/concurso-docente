from django.shortcuts import render

from .analitica import analizar_historial
from .models import Intento, ProgresoModulo


def mi_progreso(request):
    progresos = []
    intentos = []
    analisis = None

    if request.user.is_authenticated:
        progresos = ProgresoModulo.objects.filter(
            usuario=request.user
        ).select_related('modulo').order_by('modulo__orden')

        intentos = list(
            Intento.objects.filter(usuario=request.user, estado='completado')
            .select_related('simulacro')
            .order_by('-fecha_finalizacion')[:50]
        )

        analisis = analizar_historial(request.user)

    chart_data = {
        'labels': [p.modulo.titulo for p in progresos],
        'valores': [p.porcentaje for p in progresos],
    }

    # El grafico de tendencia necesita orden cronologico ascendente
    # (mas antiguo -> mas reciente), al reves del historial en tabla.
    intentos_cronologicos = list(reversed(intentos))
    tendencia_data = {
        'labels': [i.fecha_finalizacion.strftime('%d/%m') for i in intentos_cronologicos],
        'valores': [float(i.puntaje_obtenido or 0) for i in intentos_cronologicos],
    }

    return render(
        request,
        'seguimiento/mi_progreso.html',
        {
            'progresos': progresos,
            'chart_data': chart_data,
            'intentos': intentos,
            'tendencia_data': tendencia_data,
            'analisis': analisis,
        }
    )
