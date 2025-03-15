# Imports de Flask
from flask import Blueprint, render_template, jsonify
# Imports de Flask-Login
from flask_login import login_required, current_user
# Imports de modelos
from models.models import Datos
from routes.capturas import capture_enabled

# Creación del blueprint
dashboard = Blueprint('dashboard', __name__)

# Ruta del panel de control
@dashboard.route('/dashboard')
@login_required
def panel_control():    # Cambiado de dashboard a panel_control
    # Obtener datos del usuario actual
    datos = Datos.query.filter_by(id_usuario=current_user.id).order_by(Datos.fecha.desc()).all()
    
    # Agrupar por equipos
    equipos = {}
    for dato in datos:
        equipo_id = dato.equipo.nombre
        fecha_str = dato.fecha.strftime('%Y-%m-%d')
        
        if equipo_id not in equipos:
            equipos[equipo_id] = {}
            
        if fecha_str not in equipos[equipo_id]:
            equipos[equipo_id][fecha_str] = []
            
        equipos[equipo_id][fecha_str].append(dato)
        print(capture_enabled)
    
    return render_template('dashboard.html', 
                         capture_enabled=capture_enabled,
                         equipos=equipos)

