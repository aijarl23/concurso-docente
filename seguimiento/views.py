from django.shortcuts import render
from .models import ProgresoModulo


def mi_progreso(request):
    progresos = []

    if request.user.is_authenticated:
        progresos = ProgresoModulo.objects.filter(
            usuario=request.user
        )

    return render(
        request,
        'seguimiento/mi_progreso.html',
        {
            'progresos': progresos
        }
    )