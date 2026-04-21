from django import forms
from django.utils import timezone
from datetime import timedelta, date, time
from .models import Consulta
 
 
# 🔹 Diccionario de días en español
DIAS_ES = {
    0: 'Lunes',
    1: 'Martes',
    2: 'Miércoles',
    3: 'Jueves',
    4: 'Viernes',
    5: 'Sábado',
    6: 'Domingo',
}
 
 
def get_turnos_disponibles():
    hoy = date.today()
    limite = hoy + timedelta(weeks=4)
    horarios = [time(17, 0), time(17, 30), time(18, 0), time(18, 30), time(19, 0)]
 
    ocupados = set(
        Consulta.objects.values_list('fecha_turno', 'hora_turno')
    )
 
    turnos = []
    dia = hoy + timedelta(days=1)
    while dia <= limite:
        if dia.weekday() in [0, 1, 2, 3]:
            for hora in horarios:
                nombre_dia = DIAS_ES[dia.weekday()]
                value = f"{dia.isoformat()}|{hora.strftime('%H:%M')}"
                if (dia, hora) in ocupados:
                    label = f"🔴 {nombre_dia} {dia.strftime('%d/%m/%Y')} — {hora.strftime('%H:%M')}hs · No Disponible"
                    turnos.append((value, label, True))
                else:
                    label = f"{nombre_dia} {dia.strftime('%d/%m/%Y')} — {hora.strftime('%H:%M')}hs"
                    turnos.append((value, label, False))
        dia += timedelta(days=1)
 
    return turnos
 
 
class SelectWithDisabled(forms.Select):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.disabled_values = set()  # se llena desde el form
 
    def optgroups(self, name, value, attrs=None):
        grupos = super().optgroups(name, value, attrs)
        for _, subgroup, _ in grupos:
            for opcion in subgroup:
                if opcion['value'] in self.disabled_values:
                    opcion['attrs']['disabled'] = True
        return grupos
 
 
class ConsultaForm(forms.ModelForm):
 
    turno = forms.ChoiceField(
        choices=[],
        label="Día y horario del turno",
        widget=SelectWithDisabled(attrs={'class': 'form-select'}),
    )
 
    class Meta:
        model = Consulta
        exclude = ['creado_en', 'leido', 'fecha_turno', 'hora_turno']
        widgets = {
            'nombre_apellido':     forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: María González'}),
            'whatsapp':            forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: +54 9 261 000 0000'}),
            'email':               forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'tu@email.com'}),
            'pais_ciudad':         forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Argentina, Mendoza'}),
            'tiene_visa':          forms.Select(attrs={'class': 'form-select'}),
            'destino':             forms.Select(attrs={'class': 'form-select'}),
            'destino_otro':        forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Especificá el destino'}),
            'multidestino':        forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Orlando + Miami'}),
            'preferencia_hotel':   forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dentro del complejo, fuera, sin preferencia...'}),
            'fecha_salida':        forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'flexibilidad_fechas': forms.Select(attrs={'class': 'form-select'}),
            'cantidad_noches':     forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'adultos':             forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'menores':             forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'edades_menores':      forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 4, 7, 12 años'}),
            'dias_parques':        forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'presupuesto':         forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: USD 3000 - 5000'}),
            'observaciones':       forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Contanos todo lo que quieras...'}),
        }
 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        turnos_raw = get_turnos_disponibles()
 
        # Guardamos los valores deshabilitados en el widget
        self.fields['turno'].widget.disabled_values = {
            v for v, l, d in turnos_raw if d
        }
 
        # Choices siempre de 2 elementos — Django no acepta más
        self.fields['turno'].choices = (
            [('', '— Seleccioná un turno disponible —')] +
            [(v, l) for v, l, d in turnos_raw]
        )
 
    def clean_turno(self):
        valor = self.cleaned_data.get('turno')
        if not valor:
            raise forms.ValidationError('Tenés que elegir un turno.')
        try:
            fecha_str, hora_str = valor.split('|')
            fecha = date.fromisoformat(fecha_str)
            hora = time(*[int(x) for x in hora_str.split(':')])
        except Exception:
            raise forms.ValidationError('Turno inválido.')
 
        if Consulta.objects.filter(fecha_turno=fecha, hora_turno=hora).exists():
            raise forms.ValidationError('¡Ese turno ya fue reservado! Por favor elegí otro.')
 
        self.cleaned_data['fecha_turno_parsed'] = fecha
        self.cleaned_data['hora_turno_parsed'] = hora
        return valor
 
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.fecha_turno = self.cleaned_data['fecha_turno_parsed']
        instance.hora_turno = self.cleaned_data['hora_turno_parsed']
        if commit:
            instance.save()
        return instance