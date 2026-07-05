from django.contrib import admin
from .models import Intento, RespuestaIntento, ProgresoModulo

admin.site.register(Intento)
admin.site.register(RespuestaIntento)
admin.site.register(ProgresoModulo)