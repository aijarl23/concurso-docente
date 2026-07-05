import random
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db import transaction

from .models import Simulacro
from seguimiento.models import Intento, RespuestaIntento


@login_required
def lista_simulacros(request):
    simulacros = Simulacro.objects.filter(activo=True).order_by('nombre')

    for s in simulacros:
        s.mis_intentos = Intento.objects.filter(
            usuario=request.user,
            simulacro=s,
            estado='completado'
        ).count()

        mejor = Intento.objects.filter(
            usuario=request.user,
            simulacro=s,
            estado='completado'
        ).order_by('-puntaje_obtenido').first()

        s.mejor_puntaje = mejor.puntaje_obtenido if mejor else None

    return render(
        request,
        'evaluaciones/lista_simulacros.html',
        {'simulacros': simulacros}
    )


@login_required
def iniciar_simulacro(request, simulacro_id):
    simulacro = get_object_or_404(Simulacro, pk=simulacro_id, activo=True)

    intento = Intento.objects.create(
        usuario=request.user,
        simulacro=simulacro
    )

    return redirect('realizar_simulacro', intento_id=intento.id)


@login_required
def realizar_simulacro(request, intento_id):
    intento = get_object_or_404(
        Intento,
        pk=intento_id,
        usuario=request.user
    )

    preguntas = list(
        intento.simulacro.preguntas.filter(activa=True)
    )

    random.shuffle(preguntas)

    if request.method == 'POST':
        with transaction.atomic():
            correctas = 0

            for pregunta in preguntas:
                respuesta = request.POST.get(
                    f'pregunta_{pregunta.id}'
                )

                es_correcta = (
                    respuesta == pregunta.respuesta_correcta
                ) if respuesta else False

                RespuestaIntento.objects.create(
                    intento=intento,
                    pregunta=pregunta,
                    respuesta_seleccionada=respuesta,
                    es_correcta=es_correcta,
                    tiempo_respuesta_segundos=0
                )

                if es_correcta:
                    correctas += 1

            total = len(preguntas)

            intento.total_correctas = correctas
            intento.total_incorrectas = total - correctas
            intento.total_sin_responder = 0
            intento.puntaje_obtenido = round(
                (correctas / total) * 100,
                2
            )
            intento.estado = 'completado'
            intento.fecha_finalizacion = timezone.now()
            intento.save()

        return redirect(
            'resultado_simulacro',
            intento_id=intento.id
        )

    return render(
        request,
        'evaluaciones/realizar_simulacro.html',
        {
            'intento': intento,
            'preguntas': preguntas,
            'total_preguntas': len(preguntas),
        }
    )


@login_required
def resultado_simulacro(request, intento_id):
    intento = get_object_or_404(
        Intento,
        pk=intento_id,
        usuario=request.user
    )

    respuestas = RespuestaIntento.objects.filter(
        intento=intento
    ).select_related('pregunta')

    return render(
        request,
        'evaluaciones/resultado_simulacro.html',
        {
            'intento': intento,
            'respuestas': respuestas,
            'aprobado': intento.puntaje_obtenido >= 70,
        }
    )