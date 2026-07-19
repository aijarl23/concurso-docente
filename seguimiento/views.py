from django.shortcuts import render
from .models import ProgresoModulo


def mi_progreso(request):
    progresos = []

    if request.user.is_authenticated:
        progresos = ProgresoModulo.objects.filter(
            usuario=request.user
        ).select_related('modulo').order_by('modulo__orden')

    chart_data = {
        'labels': [p.modulo.titulo for p in progresos],
        'valores': [p.porcentaje for p in progresos],
    }

    return render(
        request,
        'seguimiento/mi_progreso.html',
        {
            'progresos': progresos,
            'chart_data': chart_data,
        }
    )