from django.contrib import admin
from .models import Consulta


@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_display = ['nombre_apellido', 'email', 'whatsapp', 'destino', 'fecha_salida', 'creado_en', 'leido']
    list_filter = ['destino', 'leido', 'flexibilidad_fechas']
    search_fields = ['nombre_apellido', 'email', 'whatsapp']
    list_editable = ['leido']
    readonly_fields = ['creado_en']