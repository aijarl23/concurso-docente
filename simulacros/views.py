import random
from collections import defaultdict

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone

from access_control.services import user_has_module_access
from banco.models import BancoPregunta
from commerce.models import Product
from seguimiento.models import Intento, RespuestaIntento
from .models import Simulacro


AREAS_DISCIPLINARES = [
    ('ingles', 'Ingles'),
    ('tecnologia', 'Tecnologia e Informatica'),
    ('matematicas', 'Matematicas'),
    ('ciencias_naturales', 'Ciencias Naturales'),
    ('ciencias_sociales', 'Ciencias Sociales'),
]


def _checkout_for_simulacro(simulacro):
    if not simulacro.module:
        return reverse('commerce:product_list')
    product = Product.objects.filter(module=simulacro.module, active=True).first()
    if product:
        return reverse('payments:buy_module', args=[product.id])
    return reverse('commerce:product_list')


def _send_result_email(intento):
    user = intento.usuario
    if not user.email:
        return False

    por_competencia = defaultdict(lambda: {'total': 0, 'correctas': 0})
    for respuesta in intento.respuestas.select_related('pregunta__subcategoria'):
        pregunta = respuesta.pregunta
        competencia = pregunta.competencia or (pregunta.subcategoria.nombre if pregunta.subcategoria else pregunta.area)
        por_competencia[competencia]['total'] += 1
        if respuesta.es_correcta:
            por_competencia[competencia]['correctas'] += 1

    detalle = '\n'.join(
        f"- {nombre}: {datos['correctas']}/{datos['total']}"
        for nombre, datos in sorted(por_competencia.items())
    )
    subject = f'Resultado de simulacro - {intento.simulacro.nombre}'
    body = (
        f'Hola {user.nombre},\n\n'
        f'Finalizaste el simulacro: {intento.simulacro.nombre}.\n'
        f'Puntaje: {intento.puntaje_obtenido}%\n'
        f'Aciertos: {intento.total_correctas}\n'
        f'Errores: {intento.total_incorrectas}\n'
        f'Sin responder: {intento.total_sin_responder}\n'
        f'Tiempo usado: {intento.tiempo_usado_segundos} segundos\n\n'
        f'Desempeño por competencia:\n{detalle}\n\n'
        'Revisa las justificaciones en la plataforma para orientar tu plan de mejora.'
    )
    sent = send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=True)
    return bool(sent)


@login_required
def lista_simulacros(request):
    simulacros = Simulacro.objects.filter(activo=True).select_related('module').prefetch_related('preguntas').order_by('nombre')
    cards = []
    for simulacro in simulacros:
        has_access = not simulacro.es_premium or user_has_module_access(request.user, simulacro.module)
        cards.append({
            'simulacro': simulacro,
            'has_access': has_access,
            'checkout_url': None if has_access else _checkout_for_simulacro(simulacro),
        })
    return render(request, 'simulacros/lista_simulacros.html', {'simulacro_cards': cards, 'areas': AREAS_DISCIPLINARES})


@login_required
def seleccionar_area(request):
    area = request.GET.get('area') or request.user.area_concurso or 'matematicas'
    simulacros = Simulacro.objects.filter(activo=True, tipo='area', area=area).select_related('module')
    return render(request, 'simulacros/seleccionar_area.html', {
        'areas': AREAS_DISCIPLINARES,
        'area_actual': area,
        'simulacros': simulacros,
    })


@login_required
def iniciar_simulacro(request, simulacro_id):
    simulacro = get_object_or_404(Simulacro, id=simulacro_id, activo=True)
    if simulacro.es_premium and not user_has_module_access(request.user, simulacro.module):
        messages.warning(request, 'Este simulacro es premium. Debes comprar el módulo o paquete Elite para ingresar.')
        return redirect(_checkout_for_simulacro(simulacro))

    if request.method != 'POST':
        return render(request, 'simulacros/configurar_simulacro.html', {'simulacro': simulacro})

    try:
        seconds_per_question = int(request.POST.get('seconds_per_question') or simulacro.tiempo_por_pregunta_segundos or 180)
    except (TypeError, ValueError):
        seconds_per_question = 180
    seconds_per_question = min(max(seconds_per_question, 60), 600)

    intento = Intento.objects.create(usuario=request.user, simulacro=simulacro)
    request.session[f'simulacro_seconds_per_question_{intento.id}'] = seconds_per_question
    return redirect('simulacros:realizar_simulacro', intento_id=intento.id)


@login_required
def realizar_simulacro(request, intento_id):
    intento = get_object_or_404(Intento, id=intento_id, usuario=request.user)
    if intento.estado == 'completado':
        return redirect('simulacros:resultado_simulacro', intento_id=intento.id)

    preguntas = list(intento.simulacro.preguntas.filter(activa=True).order_by('id'))
    random.Random(intento.id).shuffle(preguntas)
    seconds_per_question = int(
        request.session.get(
            f'simulacro_seconds_per_question_{intento.id}',
            intento.simulacro.tiempo_por_pregunta_segundos or 180,
        )
    )
    seconds_per_question = min(max(seconds_per_question, 60), 600)
    total_time_limit = seconds_per_question * max(len(preguntas), 1)

    if request.method == 'POST':
        with transaction.atomic():
            intento.respuestas.all().delete()
            correctas = 0
            sin_responder = 0
            tiempo_total = int(request.POST.get('tiempo_total_prueba') or 0)
            respondida_en_tiempo = tiempo_total <= total_time_limit

            for pregunta in preguntas:
                respuesta = request.POST.get(f'pregunta_{pregunta.id}')
                es_correcta = respuesta == pregunta.respuesta_correcta and respondida_en_tiempo

                if not respuesta:
                    sin_responder += 1
                elif es_correcta:
                    correctas += 1

                RespuestaIntento.objects.create(
                    intento=intento,
                    pregunta=pregunta,
                    respuesta_seleccionada=respuesta,
                    es_correcta=es_correcta,
                    respondida_en_tiempo=respondida_en_tiempo,
                    tiempo_usado_segundos=0,
                )

            total = len(preguntas) or 1
            intento.total_correctas = correctas
            intento.total_sin_responder = sin_responder
            intento.total_incorrectas = total - correctas - sin_responder
            intento.estado = 'completado'
            intento.fecha_finalizacion = timezone.now()
            intento.tiempo_usado_segundos = tiempo_total
            intento.puntaje_obtenido = round((correctas / total) * 100, 2)
            intento.reporte_enviado = _send_result_email(intento)
            intento.save()

        return redirect('simulacros:resultado_simulacro', intento_id=intento.id)

    return render(request, 'simulacros/realizar_simulacro.html', {
        'intento': intento,
        'preguntas': preguntas,
        'seconds_per_question': seconds_per_question,
        'total_time_limit': total_time_limit,
    })


@login_required
def resultado_simulacro(request, intento_id):
    intento = get_object_or_404(Intento, id=intento_id, usuario=request.user)
    respuestas = intento.respuestas.select_related('pregunta', 'pregunta__subcategoria')
    resumen = defaultdict(lambda: {'total': 0, 'correctas': 0})
    for respuesta in respuestas:
        pregunta = respuesta.pregunta
        competencia = pregunta.competencia or (pregunta.subcategoria.nombre if pregunta.subcategoria else pregunta.area)
        resumen[competencia]['total'] += 1
        if respuesta.es_correcta:
            resumen[competencia]['correctas'] += 1
    return render(request, 'simulacros/resultado_simulacro.html', {
        'intento': intento,
        'respuestas': respuestas,
        'resumen_competencias': dict(resumen),
    })
