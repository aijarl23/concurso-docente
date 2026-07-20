import random
from collections import defaultdict

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone

from access_control.services import user_has_full_access, user_has_module_access
from contenidos.models import Modulo
from seguimiento.analitica import analizar_intento
from seguimiento.models import Intento, ProgresoModulo, RespuestaIntento
from .models import Simulacro

AREAS_DISCIPLINARES = [
    ('ingles', 'Inglés'),
    ('tecnologia', 'Tecnología e Informática'),
    ('matematicas', 'Matemáticas'),
    ('ciencias_naturales', 'Ciencias Naturales'),
    ('ciencias_sociales', 'Ciencias Sociales'),
]

MODULE_SLUG_TO_CONTENT_TYPE = {
    'diagnostico-inicial': 'diagnostico_inicial',
    'lectura-critica-aplicada': 'lectura_critica_aplicada',
    'competencias-pedagogicas': 'competencias_pedagogicas',
    'competencias-comportamentales-tjs': 'competencias_tjs',
    'normativa-contexto-docente': 'normativa_contexto',
    'simulacros-por-area': 'simulacros_area',
    'simulacro-final-concurso': 'simulacro_final',
    'reporte-progreso-plan-mejora': 'reporte_mejora',
}


def _checkout_for_simulacro(simulacro):
    # payments:buy_module solo acepta POST (@require_POST, agregado en la
    # auditoria tecnica del 2026-07-19 para no crear una Order en un GET).
    # Este helper se usa desde un redirect() de vista (iniciar_simulacro) y
    # desde un <a href> en lista_simulacros.html - ambos son navegaciones GET,
    # asi que enlazar directo a buy_module siempre respondia 405 Method Not
    # Allowed, dejando el flujo de pago inaccesible desde cualquier simulacro
    # premium. commerce:product_list es la pagina real de matricula: renderiza
    # el mismo producto dentro de un <form method="post"> con csrf_token, asi
    # que sigue siendo GET-seguro y termina en el mismo botón de pago.
    return reverse('commerce:product_list')


def _option_text(pregunta, option):
    return {
        'A': pregunta.opcion_a,
        'B': pregunta.opcion_b,
        'C': pregunta.opcion_c,
        'D': pregunta.opcion_d,
    }.get(option or '', '')


def _sync_module_progress(intento):
    module = getattr(intento.simulacro, 'module', None)
    if not module:
        return
    content_type = MODULE_SLUG_TO_CONTENT_TYPE.get(module.slug)
    if not content_type:
        return
    content_module = Modulo.objects.filter(tipo=content_type, activo=True).first()
    if not content_module:
        return
    progress, _ = ProgresoModulo.objects.get_or_create(usuario=intento.usuario, modulo=content_module)
    if progress.porcentaje < 100:
        progress.porcentaje = 100
        progress.save(update_fields=['porcentaje'])


def _send_result_email(intento):
    user = intento.usuario
    if not user.email:
        return False
    if 'console' in getattr(settings, 'EMAIL_BACKEND', '').lower():
        return False

    por_competencia = defaultdict(lambda: {'total': 0, 'correctas': 0})
    for respuesta in intento.respuestas.select_related('pregunta__subcategoria'):
        pregunta = respuesta.pregunta
        competencia = pregunta.competencia or (pregunta.subcategoria.nombre if pregunta.subcategoria else pregunta.area)
        por_competencia[competencia]['total'] += 1
        if respuesta.es_correcta:
            por_competencia[competencia]['correctas'] += 1

    detalle = '\n'.join(
        f'- {nombre}: {datos["correctas"]}/{datos["total"]}'
        for nombre, datos in sorted(por_competencia.items())
    )
    detalle_preguntas = []
    for idx, respuesta in enumerate(intento.respuestas.select_related('pregunta').order_by('id'), 1):
        pregunta = respuesta.pregunta
        seleccion = respuesta.respuesta_seleccionada or 'Sin responder'
        detalle_preguntas.append(
            f'{idx}. {pregunta.enunciado}\n'
            f'   Tu respuesta: {seleccion} {_option_text(pregunta, respuesta.respuesta_seleccionada)}\n'
            f'   Respuesta correcta: {pregunta.respuesta_correcta} {_option_text(pregunta, pregunta.respuesta_correcta)}\n'
            f'   Justificacion: {pregunta.justificacion or "No disponible."}'
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
        f'Desempeno por competencia:\n{detalle}\n\n'
        f'Retroalimentación por pregunta:\n' + '\n\n'.join(detalle_preguntas)
    )
    sent = send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=True)
    return bool(sent)


@login_required
def lista_simulacros(request):
    simulacros = Simulacro.objects.filter(activo=True).select_related('module').prefetch_related('preguntas').order_by('nombre')
    paginator = Paginator(simulacros, 20)
    page_obj = paginator.get_page(request.GET.get('page'))

    # user_has_module_access siempre resuelve contra el mismo bundle 'elite'
    # (acceso todo-o-nada) salvo que module sea None, asi que calcular el
    # acceso una sola vez evita una query de UserAccess por cada fila.
    has_full_access = user_has_full_access(request.user)
    cards = []
    for simulacro in page_obj:
        has_access = not simulacro.es_premium or simulacro.module_id is None or has_full_access
        cards.append({
            'simulacro': simulacro,
            'has_access': has_access,
            'checkout_url': None if has_access else _checkout_for_simulacro(simulacro),
        })
    return render(request, 'simulacros/lista_simulacros.html', {
        'simulacro_cards': cards,
        'areas': AREAS_DISCIPLINARES,
        'page_obj': page_obj,
    })


@login_required
def seleccionar_area(request):
    area = request.GET.get('area') or request.user.area_concurso or 'matematicas'
    simulacros = Simulacro.objects.filter(activo=True, tipo='area', area=area).select_related('module')
    has_full_access = user_has_full_access(request.user)
    simulacro_cards = [
        {
            'simulacro': simulacro,
            'has_access': not simulacro.es_premium or simulacro.module_id is None or has_full_access,
        }
        for simulacro in simulacros
    ]
    return render(request, 'simulacros/seleccionar_area.html', {
        'simulacro_cards': simulacro_cards,
        'areas': AREAS_DISCIPLINARES,
        'area_actual': area,
        'simulacros': simulacros,
    })


@login_required
def iniciar_simulacro(request, simulacro_id):
    simulacro = get_object_or_404(Simulacro, id=simulacro_id, activo=True)
    if simulacro.es_premium and not user_has_module_access(request.user, simulacro.module):
        messages.warning(request, 'Este simulacro hace parte del curso completo. Compra el acceso único para ingresar a todos los módulos y simulacros.')
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
    seconds_per_question = int(request.session.get(f'simulacro_seconds_per_question_{intento.id}', intento.simulacro.tiempo_por_pregunta_segundos or 180))
    seconds_per_question = min(max(seconds_per_question, 60), 600)
    total_time_limit = seconds_per_question * max(len(preguntas), 1)

    if request.method == 'POST':
        with transaction.atomic():
            intento.respuestas.all().delete()
            correctas = 0
            sin_responder = 0
            puntos_obtenidos = []
            tiempo_total = int(request.POST.get('tiempo_total_prueba') or 0)
            respondida_en_tiempo = tiempo_total <= total_time_limit

            respuestas_a_crear = []
            for pregunta in preguntas:
                respuesta = request.POST.get(f'pregunta_{pregunta.id}')
                es_correcta = respuesta == pregunta.respuesta_correcta and respondida_en_tiempo
                if not respuesta:
                    sin_responder += 1
                    puntos_obtenidos.append(0)
                else:
                    if es_correcta:
                        correctas += 1
                    if respondida_en_tiempo:
                        # Idoneidad graduada (TJS): puntaje por cercania al
                        # mejor juicio posible, no solo acierto binario. Cae
                        # al esquema binario si la pregunta no tiene
                        # idoneidad definida (ver BancoPregunta.puntos_por_respuesta).
                        puntos_obtenidos.append(pregunta.puntos_por_respuesta(respuesta))
                    else:
                        puntos_obtenidos.append(0)
                respuestas_a_crear.append(RespuestaIntento(
                    intento=intento,
                    pregunta=pregunta,
                    respuesta_seleccionada=respuesta,
                    es_correcta=es_correcta,
                    respondida_en_tiempo=respondida_en_tiempo,
                    tiempo_usado_segundos=0,
                ))
            RespuestaIntento.objects.bulk_create(respuestas_a_crear)

            total = len(preguntas) or 1
            intento.total_correctas = correctas
            intento.total_sin_responder = sin_responder
            intento.total_incorrectas = total - correctas - sin_responder
            intento.estado = 'completado'
            intento.fecha_finalizacion = timezone.now()
            intento.tiempo_usado_segundos = tiempo_total
            intento.puntaje_obtenido = round((sum(puntos_obtenidos) / total) * 100, 2)
            intento.save()
            _sync_module_progress(intento)

        # El envio de correo queda fuera de la transaccion: es una llamada
        # SMTP bloqueante y no debe mantener abiertos los locks de
        # Intento/RespuestaIntento mientras dura el round-trip de red.
        intento.reporte_enviado = _send_result_email(intento)
        intento.save(update_fields=['reporte_enviado'])

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
    respuestas = intento.respuestas.select_related('pregunta', 'pregunta__subcategoria').order_by('id')
    resumen = defaultdict(lambda: {'total': 0, 'correctas': 0})
    revision = []
    for respuesta in respuestas:
        pregunta = respuesta.pregunta
        competencia = pregunta.competencia or (pregunta.subcategoria.nombre if pregunta.subcategoria else pregunta.area)
        resumen[competencia]['total'] += 1
        if respuesta.es_correcta:
            resumen[competencia]['correctas'] += 1
        revision.append({
            'respuesta': respuesta,
            'pregunta': pregunta,
            'seleccion': respuesta.respuesta_seleccionada or 'Sin responder',
            'seleccion_texto': _option_text(pregunta, respuesta.respuesta_seleccionada),
            'correcta': pregunta.respuesta_correcta,
            'correcta_texto': _option_text(pregunta, pregunta.respuesta_correcta),
        })

    email_console_mode = 'console' in getattr(settings, 'EMAIL_BACKEND', '').lower()

    diagnostico = None
    if intento.simulacro.tipo == 'diagnostico':
        diagnostico = analizar_intento(intento)

    return render(request, 'simulacros/resultado_simulacro.html', {
        'intento': intento,
        'respuestas': respuestas,
        'revision_preguntas': revision,
        'resumen_competencias': dict(resumen),
        'email_console_mode': email_console_mode,
        'diagnostico': diagnostico,
    })
