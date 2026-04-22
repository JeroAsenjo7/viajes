from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.conf import settings
from .forms import ConsultaForm
from .models import Consulta

import logging
logger = logging.getLogger(__name__)

DIAS_ES = {
    0: 'Lunes', 1: 'Martes', 2: 'Miércoles',
    3: 'Jueves', 4: 'Viernes', 5: 'Sábado', 6: 'Domingo'
}


# ── Formulario público ──────────────────────────────────────
def consulta_view(request):
    if request.method == 'POST':
        form = ConsultaForm(request.POST)
        if form.is_valid():
            consulta = form.save()
            mensaje = f"""
Nueva consulta recibida desde la web:

── TURNO RESERVADO ───────────────
Día:          {consulta.fecha_turno.strftime('%d/%m/%Y')}
Horario:      {consulta.hora_turno.strftime('%H:%M')}hs

── CONTACTO ──────────────────────
Nombre:       {consulta.nombre_apellido}
WhatsApp:     {consulta.whatsapp}
Email:        {consulta.email}
País/Ciudad:  {consulta.pais_ciudad}
Visa:         {consulta.get_tiene_visa_display()}

── DESTINO ───────────────────────
Destino:      {consulta.get_destino_display()}
Otro:         {consulta.destino_otro or '—'}
Multidestino: {consulta.multidestino or '—'}
Hotel:        {consulta.preferencia_hotel or '—'}

── FECHAS ────────────────────────
Salida:       {consulta.fecha_salida}
Flexibilidad: {consulta.get_flexibilidad_fechas_display()}
Noches:       {consulta.cantidad_noches}

── GRUPO ─────────────────────────
Adultos:      {consulta.adultos}
Menores:      {consulta.menores}
Edades:       {consulta.edades_menores or '—'}

── LOGÍSTICA ─────────────────────
Vuelos:       {'Sí' if consulta.incluir_vuelos else 'No'}
Traslados:    {'Sí' if consulta.necesita_traslados else 'No'}

── OPCIONALES ────────────────────
Días parques: {consulta.dias_parques or '—'}
Asesoría visa: {'Sí' if consulta.asesoria_visa else 'No'}

── PRESUPUESTO ───────────────────
Presupuesto:  {consulta.presupuesto or '—'}
Observaciones:{consulta.observaciones or '—'}
            """

            try:
                send_mail(
                    subject=f'Nueva consulta — {consulta.nombre_apellido} | Turno: {consulta.fecha_turno.strftime("%d/%m/%Y")} {consulta.hora_turno.strftime("%H:%M")}hs',
                    message=mensaje,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.EMAIL_DESTINO],
                    fail_silently=False,
                )
            except Exception as e:
                print(f"Error al enviar correo al admin: {e}", flush=True)

            try:
                send_mail(
                    subject='¡Tu consulta fue recibida! ✨ Paola Ripa - Agente Oficial Disney & Universal',
                    message=f"""
Hola {consulta.nombre_apellido}!

¡Gracias por contactarme! Recibí tu consulta y estoy muy feliz de poder acompañarte en esta aventura mágica. 🎢✨

Tu turno está confirmado para:

📅 Día: {DIAS_ES[consulta.fecha_turno.weekday()]} {consulta.fecha_turno.strftime('%d/%m/%Y')}
🕐 Horario: {consulta.hora_turno.strftime('%H:%M')}hs

En esa reunión vamos a repasar todos los detalles de tu viaje y armar el presupuesto ideal para vos.

Si necesitás reprogramar o tenés alguna consulta antes de la reunión, escribime por Instagram o WhatsApp.

📱 Instagram: @PAOVALIJAMAGICA

¡Nos vemos pronto!
Paola Ripa
Agente Oficial Disney & Universal ✨
                    """,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[consulta.email],
                    fail_silently=False,
                )
            except Exception as e:
                print(f"Error al enviar correo al cliente: {e}", flush=True)

            return redirect('consulta_exitosa')
    else:
        form = ConsultaForm()
    return render(request, 'base.html', {'form': form})


def consulta_exitosa(request):
    return render(request, 'exito.html')


# ── Login / Logout ──────────────────────────────────────────

def panel_login(request):
    error = None
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST.get('username'),
            password=request.POST.get('password'),
        )
        if user is not None:
            login(request, user)
            return redirect('panel')
        else:
            error = 'Usuario o contraseña incorrectos.'
    return render(request, 'reservas/login.html', {'error': error})


def panel_logout(request):
    logout(request)
    return redirect('panel_login')


# ── Panel principal ─────────────────────────────────────────
@login_required(login_url='panel_login')
def panel(request):
    consultas = Consulta.objects.all()

    mes = request.GET.get('mes', '')
    dia = request.GET.get('dia', '')
    destino = request.GET.get('destino', '')
    etiqueta = request.GET.get('etiqueta', '')

    if mes:
        consultas = consultas.filter(fecha_turno__month=mes)
    if dia:
        consultas = consultas.filter(fecha_turno__day=dia)
    if destino:
        consultas = consultas.filter(destino=destino)
    if etiqueta:
        consultas = consultas.filter(etiqueta=etiqueta)

    meses = [
        ('1','Enero'),('2','Febrero'),('3','Marzo'),('4','Abril'),
        ('5','Mayo'),('6','Junio'),('7','Julio'),('8','Agosto'),
        ('9','Septiembre'),('10','Octubre'),('11','Noviembre'),('12','Diciembre'),
    ]
    dias = [str(i) for i in range(1, 32)]

    # Marcamos selected desde Python
    meses_opts = [{'val': v, 'nom': n, 'sel': v == mes} for v, n in meses]
    dias_opts = [{'val': d, 'sel': d == dia} for d in dias]
    destinos_opts = [{'val': v, 'nom': n, 'sel': v == destino} for v, n in Consulta.DESTINO_CHOICES]
    etiquetas_opts = [{'val': v, 'nom': n, 'sel': v == etiqueta} for v, n in Consulta.ETIQUETA_CHOICES]

    # Para los selects de etiqueta dentro de cada consulta
    for c in consultas:
        c.etiquetas_opts = [{'val': v, 'nom': n, 'sel': v == (c.etiqueta or '')} for v, n in Consulta.ETIQUETA_CHOICES]

    context = {
        'consultas': consultas,
        'meses_opts': meses_opts,
        'dias_opts': dias_opts,
        'destinos_opts': destinos_opts,
        'etiquetas_opts': etiquetas_opts,
        'etiquetas': Consulta.ETIQUETA_CHOICES,
    }
    return render(request, 'reservas/panel.html', context)


# ── Ver detalle ─────────────────────────────────────────────
@login_required(login_url='panel_login')
def panel_detalle(request, pk):
    consulta = get_object_or_404(Consulta, pk=pk)
    return render(request, 'reservas/detalle.html', {'consulta': consulta})


# ── Editar ──────────────────────────────────────────────────
@login_required(login_url='panel_login')
def panel_editar(request, pk):
    consulta = get_object_or_404(Consulta, pk=pk)
    if request.method == 'POST':
        form = ConsultaForm(request.POST, instance=consulta)
        if form.is_valid():
            form.save()
            return redirect('panel_detalle', pk=pk)
    else:
        form = ConsultaForm(instance=consulta)
    return render(request, 'reservas/editar.html', {'form': form, 'consulta': consulta})


# ── Borrar ──────────────────────────────────────────────────
@login_required(login_url='panel_login')
def panel_borrar(request, pk):
    consulta = get_object_or_404(Consulta, pk=pk)
    if request.method == 'POST':
        consulta.delete()
        return redirect('panel')
    return render(request, 'reservas/confirmar_borrar.html', {'consulta': consulta})

# -─ Cambiar etiqueta ─────────────────────────────────────────
@login_required(login_url='panel_login')
def panel_etiqueta(request, pk):
    consulta = get_object_or_404(Consulta, pk=pk)
    if request.method == 'POST':
        consulta.etiqueta = request.POST.get('etiqueta') or None
        consulta.save()
    return redirect(request.POST.get('next', 'panel'))