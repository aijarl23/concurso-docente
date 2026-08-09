from django.conf import settings
from django.shortcuts import render

# Fecha de "ultima actualizacion" mostrada en las paginas legales. Se
# actualiza a mano cada vez que se edite el contenido de una de estas
# paginas (no hay necesidad de un campo en base de datos para 3 paginas
# estaticas).
FECHA_ACTUALIZACION_LEGAL = '9 de agosto de 2026'


def _contexto_legal():
    return {
        'fecha_actualizacion': FECHA_ACTUALIZACION_LEGAL,
        'correo_contacto': settings.LEGAL_CONTACT_EMAIL,
        'responsable_nombre': settings.LEGAL_RESPONSABLE_NOMBRE,
    }


def terminos(request):
    return render(request, 'landing/terminos.html', _contexto_legal())


def privacidad(request):
    return render(request, 'landing/privacidad.html', _contexto_legal())


def reembolsos(request):
    return render(request, 'landing/reembolsos.html', _contexto_legal())
