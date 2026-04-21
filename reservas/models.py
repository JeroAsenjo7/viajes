from django.db import models


class Consulta(models.Model):

    # ── Información de contacto
    nombre_apellido = models.CharField(max_length=150, verbose_name="Nombre y apellido")
    whatsapp = models.CharField(max_length=30, verbose_name="WhatsApp / Teléfono")
    email = models.EmailField(verbose_name="Correo electrónico")
    pais_ciudad = models.CharField(max_length=120, verbose_name="País y ciudad de residencia")
    tiene_visa = models.CharField(
        max_length=20,
        choices=[
            ('visa_usa', 'Visa USA'),
            ('ciudadania', 'Ciudadanía'),
            ('ninguna', 'Ninguna'),
            ('otro', 'Otro'),
        ],
        verbose_name="¿Tenés visa o ciudadanía?"
    )

    # ── Definición del destino
    DESTINO_CHOICES = [
        ('disney_orlando', 'Disney Orlando'),
        ('disney_paris', 'Disney París'),
        ('disney_tokio', 'Disney Tokio'),
        ('universal', 'Universal Orlando'),
        ('miami', 'Miami'),
        ('europa', 'Europa'),
        ('crucero', 'Crucero'),
        ('otro', 'Otro'),
    ]
    destino = models.CharField(max_length=30, choices=DESTINO_CHOICES, verbose_name="¿A dónde pensás viajar?")
    destino_otro = models.CharField(max_length=120, blank=True, verbose_name="Otro destino (especificar)")
    multidestino = models.CharField(max_length=200, blank=True, verbose_name="¿Querés más de un destino?")
    preferencia_hotel = models.TextField(blank=True, verbose_name="Preferencia de hotel (Disney/Universal)")

    # ── Fechas y duración
    fecha_salida = models.DateField(verbose_name="Fecha tentativa de salida")
    flexibilidad_fechas = models.CharField(
        max_length=20,
        choices=[
            ('flexible', 'Sí, una semana antes/después'),
            ('fija', 'No, son fechas fijas'),
        ],
        verbose_name="¿Tenés flexibilidad de fechas?"
    )
    cantidad_noches = models.PositiveSmallIntegerField(verbose_name="Cantidad de noches previstas")

    # ── Composición del grupo
    adultos = models.PositiveSmallIntegerField(verbose_name="Cantidad de adultos (18+)")
    menores = models.PositiveSmallIntegerField(default=0, verbose_name="Cantidad de menores")
    edades_menores = models.CharField(max_length=200, blank=True, verbose_name="Edades de los menores")

    # ── Logística
    incluir_vuelos = models.BooleanField(default=False, verbose_name="¿Incluir vuelos en el presupuesto?")
    necesita_traslados = models.BooleanField(default=False, verbose_name="¿Necesita auto/traslados privados?")

    # ── Opcionales
    dias_parques = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Días de parques en Orlando")
    asesoria_visa = models.BooleanField(default=False, verbose_name="¿Necesita asesoría de visa/ESTA/ETIAS?")

    # ── Presupuesto y observaciones
    presupuesto = models.CharField(max_length=100, blank=True, verbose_name="Presupuesto estimado")
    observaciones = models.TextField(blank=True, verbose_name="Contanos más sobre tu viaje ideal")

    # ── Turno ────────────────────────────────────────────────────
    fecha_turno = models.DateField(verbose_name="Día del turno")
    hora_turno = models.TimeField(verbose_name="Horario del turno")

    ETIQUETA_CHOICES = [
        ('cotizacion', 'Cotización'),
        ('confirmacion', 'Confirmación'),
        ('reserva', 'Reserva'),
        ('pago_completado', 'Pago completado'),
        ('filas_rapidas', 'Sacar filas rápidas'),
        ('itinerario', 'Hacer itinerario'),
        ('reunion_pre', 'Reunión pre viaje'),
        ('en_viaje', 'En destino / En viaje'),
    ]
    etiqueta = models.CharField(
        max_length=20,
        choices=ETIQUETA_CHOICES,
        blank=True,
        null=True,
        verbose_name="Etiqueta"
    )

    # ── Meta
    creado_en = models.DateTimeField(auto_now_add=True)
    leido = models.BooleanField(default=False, verbose_name="Leído")

    class Meta:
        verbose_name = "Consulta"
        verbose_name_plural = "Consultas"
        ordering = ['-creado_en']

    def __str__(self):
        return f"{self.nombre_apellido} — {self.get_destino_display()} ({self.creado_en:%d/%m/%Y})"