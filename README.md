# 🌟 Paovalijamagica — Sistema de Reservas de Viajes

Sitio web y sistema de gestión de consultas para **Paola Ripa**, agente oficial de Disney & Universal.

---

## 🚀 Tecnologías

- **Backend**: Django 6
- **Base de datos**: PostgreSQL (producción) / SQLite (desarrollo)
- **Frontend**: Bootstrap 5 + HTML/CSS
- **Email**: SendGrid
- **Hosting**: Railway
- **Archivos estáticos**: WhiteNoise

---

## ✨ Funcionalidades

### Sitio público
- Landing page con información de servicios
- Formulario de consulta con validaciones
- Sistema de turnos (Lunes a Jueves, 17:00 a 19:00hs, cada 30 minutos)
- Control de disponibilidad de turnos en tiempo real
- Envío automático de email al cliente y a la agente al reservar
- Galería de fotos con carrusel en mobile
- Página de éxito tras enviar la consulta

### Panel privado
- Login con usuario y contraseña
- Listado de todas las consultas
- Ver detalle completo de cada consulta
- Editar y eliminar consultas
- Etiquetas por estado: Cotización, Confirmación, Reserva, Pago completado, etc.
- Filtros por mes, día, destino y etiqueta
- Responsive para mobile y desktop

---

## ⚙️ Instalación local

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/paovalijamagica.git
cd paovalijamagica

# Crear entorno virtual
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux

# Instalar dependencias
pip install -r requirements.txt

# Correr migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Iniciar servidor
python manage.py runserver
```

---

## 🔑 Variables de entorno

Crear un archivo `.env` en la raíz con estas variables:

---

## 🚂 Deploy en Railway

1. Conectar repositorio de GitHub en Railway
2. Agregar servicio PostgreSQL
3. Configurar variables de entorno

---

## 📅 Sistema de turnos

- **Días disponibles**: Lunes a Jueves
- **Horarios**: 17:00, 17:30, 18:00, 18:30 y 19:00hs
- **Duración**: 30 minutos por turno
- **Disponibilidad**: 8 semanas hacia adelante
- Los turnos ocupados no aparecen en el selector

---

## 📬 Emails automáticos

Al recibir una consulta se envían dos emails automáticamente:
- **A la agente**: con todos los datos del formulario
- **Al cliente**: confirmación del turno reservado

---

*Desarrollado para — Agente Oficial Disney & Universal*
