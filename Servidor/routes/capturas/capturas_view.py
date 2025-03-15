from flask import Blueprint, render_template, redirect, url_for, flash, send_file, abort
# Imports de Flask-Login
from flask_login import login_required, current_user

# Imports de modelos
from models.models import Equipo, Datos

# Imports de sistema y utilidades
import io
from datetime import datetime, timedelta
from PIL import Image


capturas_view = Blueprint('capturas_view', __name__)

# Ruta para ver capturas de un equipo
@capturas_view.route('/equipo/<equipo_id>')
@login_required
def ver_equipo(equipo_id):
    datos = Datos.query.join(Equipo).filter(
        Datos.id_usuario == current_user.id,
        Equipo.nombre == equipo_id
    ).order_by(Datos.fecha.desc()).all()
    
    # Agrupar por fechas
    fechas = {}
    for dato in datos:
        fecha_str = dato.fecha.strftime('%Y-%m-%d')
        if fecha_str not in fechas:
            fechas[fecha_str] = []
        fechas[fecha_str].append(dato)
    
    return render_template('equipo.html', 
                         equipo_id=equipo_id,
                         fechas=fechas)

# Ruta para ver capturas de un equipo en una fecha
@capturas_view.route('/equipo/<equipo_id>/fecha/<fecha>')
@login_required
def ver_fecha(equipo_id, fecha):
    try:
        print(f"Fecha recibida: {fecha}")
        # Convertir la fecha de string a datetime
        fecha_dt = datetime.strptime(fecha, '%Y-%m-%d')
        fecha_siguiente = fecha_dt + timedelta(days=1)
        print(fecha_dt, fecha_siguiente)
        
        # Obtener las capturas del día
        datos = Datos.query.join(Equipo).filter(
            Datos.id_usuario == current_user.id,
            Equipo.nombre == equipo_id,
            Datos.fecha >= fecha_dt,
            Datos.fecha < fecha_siguiente
        ).order_by(Datos.fecha.desc()).all()
        
        return render_template('capturas.html',
                             equipo_id=equipo_id,
                             fecha=fecha,
                             capturas=datos)
                             
    except ValueError:
        flash('Formato de fecha inválido', 'danger')
        return redirect(url_for('capturas.ver_equipo', equipo_id=equipo_id))

# Ruta para ver una captura
@capturas_view.route('/miniatura/<int:dato_id>')
@login_required
def miniatura(dato_id):
    dato = Datos.query.get_or_404(dato_id)
    
    # Verificar que el usuario tiene acceso a esta captura
    if dato.id_usuario != current_user.id:
        abort(403)
    
    try:
        # Crear miniatura
        image = Image.open(io.BytesIO(dato.imagen))
        image.thumbnail((250, 150))
        
        # Guardar en buffer
        img_buffer = io.BytesIO()
        image.save(img_buffer, 'PNG')
        img_buffer.seek(0)
        
        return send_file(
            img_buffer,
            mimetype='image/png'
        )
    except Exception as e:
        print(f"Error al generar miniatura: {str(e)}")
        abort(500)
        
# Ruta para ver imágenes guardadas
@capturas_view.route('/ver_imagen/<int:dato_id>')
@login_required
def ver_imagen(dato_id):
    dato = Datos.query.get_or_404(dato_id)
    # Verificar que el usuario actual sea el propietario
    if dato.id_usuario != current_user.id:
        return 'No autorizado', 403
    return send_file(
        io.BytesIO(dato.imagen),
        mimetype='image/png',
        as_attachment=False
    )