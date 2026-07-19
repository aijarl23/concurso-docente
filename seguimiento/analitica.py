"""Motor de analisis de desempeno y recomendacion de ruta de estudio.

Diseno pensado para sobrevivir la llegada de un motor adaptativo (CAT/IRT)
sobre el Banco Oficial de Items: las funciones de aqui consumen unicamente
`RespuestaIntento` ya respondidas, sin ninguna suposicion sobre como se
seleccionaron esas preguntas (hoy: banco fijo por simulacro; manana:
podria ser una secuencia adaptativa). El dia que exista seleccion
adaptativa, estas funciones no cambian - solo cambia quien las alimenta.
"""

from collections import defaultdict

from django.db.models import Count, Q

FORTALEZA_MIN_PORCENTAJE = 75
BRECHA_MAX_PORCENTAJE = 60


def _modulo_para_competencia(competencia):
    from contenidos.models import Modulo
    from dashboard.question_generator import MODULES

    tipo = None
    competencia_normalizada = (competencia or '').strip().lower()
    for modulo_meta in MODULES:
        if modulo_meta.get('competencia', '').strip().lower() == competencia_normalizada:
            tipo = modulo_meta['tipo']
            break
    if not tipo:
        return None
    return Modulo.objects.filter(tipo=tipo, activo=True).first()


def analizar_respuestas(respuestas_qs):
    """Agrega un queryset de RespuestaIntento (de uno o varios intentos)
    por competencia declarada en cada pregunta."""
    agregado = (
        respuestas_qs.exclude(pregunta__competencia='')
        .values('pregunta__competencia')
        .annotate(total=Count('id'), correctas=Count('id', filter=Q(es_correcta=True)))
    )

    por_competencia = []
    for fila in agregado:
        total = fila['total']
        correctas = fila['correctas']
        porcentaje = round(correctas / total * 100, 1) if total else 0.0
        por_competencia.append({
            'competencia': fila['pregunta__competencia'],
            'correctas': correctas,
            'total': total,
            'porcentaje': porcentaje,
        })
    por_competencia.sort(key=lambda c: c['porcentaje'])

    fortalezas = [c for c in por_competencia if c['porcentaje'] >= FORTALEZA_MIN_PORCENTAJE]
    brechas = [c for c in por_competencia if c['porcentaje'] < BRECHA_MAX_PORCENTAJE]

    ruta_recomendada = []
    modulos_vistos = set()
    for competencia in brechas:
        modulo = _modulo_para_competencia(competencia['competencia'])
        if modulo and modulo.id not in modulos_vistos:
            modulos_vistos.add(modulo.id)
            ruta_recomendada.append({
                'modulo': modulo,
                'competencia': competencia['competencia'],
                'porcentaje': competencia['porcentaje'],
            })

    return {
        'por_competencia': por_competencia,
        'fortalezas': fortalezas,
        'brechas': brechas,
        'ruta_recomendada': ruta_recomendada,
    }


def analizar_intento(intento):
    return analizar_respuestas(intento.respuestas.all())


def analizar_historial(usuario):
    from .models import RespuestaIntento

    respuestas = RespuestaIntento.objects.filter(
        intento__usuario=usuario, intento__estado='completado'
    )
    return analizar_respuestas(respuestas)
