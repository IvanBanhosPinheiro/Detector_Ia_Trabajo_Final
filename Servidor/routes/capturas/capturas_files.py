from flask import Blueprint, send_file, abort
# Imports de Flask-Login
from flask_login import login_required, current_user

# Imports de modelos
from models.models import Equipo, Datos, db

# Imports de sistema y utilidades
import io
from datetime import datetime, timedelta

capturas_files = Blueprint('capturas_files', __name__)


# Ruta para eliminar capturas de un día
@capturas_files.route('/eliminar_fecha/<equipo_id>/<fecha>', methods=['DELETE'])
@login_required
def eliminar_fecha(equipo_id, fecha):
    try:
        # Convertir la fecha de string a datetime
        fecha_dt = datetime.strptime(fecha, '%Y-%m-%d')
        fecha_siguiente = fecha_dt + timedelta(days=1)
        
        # Obtener todas las capturas de ese día
        capturas = Datos.query.join(Equipo).filter(
            Datos.id_usuario == current_user.id,
            Equipo.nombre == equipo_id,
            Datos.fecha >= fecha_dt, # Desde 2024-03-16 00:00:00
            Datos.fecha < fecha_siguiente # Hasta  2024-03-17 00:00:00
        ).all()
        
        # Eliminar todas las capturas
        for captura in capturas:
            db.session.delete(captura)
        
        db.session.commit()
        return '', 204
        
    except Exception as e:
        print(f"Error al eliminar capturas: {str(e)}")
        db.session.rollback()
        return 'Error al eliminar capturas', 500

# Ruta para descargar capturas    
@capturas_files.route('/descargar_imagen/<int:dato_id>')
@login_required
def descargar_imagen(dato_id):
    dato = Datos.query.get_or_404(dato_id)
    if dato.id_usuario != current_user.id:
        abort(403)
        
    try:
        return send_file(
            io.BytesIO(dato.imagen),
            mimetype='image/png',
            as_attachment=True,
            download_name=f'captura_{dato.fecha.strftime("%Y%m%d_%H%M%S")}.png'
        )
    except Exception as e:
        print(f"Error al descargar imagen: {str(e)}")
        abort(500)

# Ruta para descargar texto
@capturas_files.route('/descargar_texto/<int:dato_id>')
@login_required
def descargar_texto(dato_id):
    dato = Datos.query.get_or_404(dato_id)
    if dato.id_usuario != current_user.id:
        abort(403)
        
    try:
        return send_file(
            io.BytesIO(dato.texto.encode('utf-8')),
            mimetype='text/plain',
            as_attachment=True,
            download_name=f'texto_{dato.fecha.strftime("%Y%m%d_%H%M%S")}.txt'
        )
    except Exception as e:
        print(f"Error al descargar texto: {str(e)}")
        abort(500)

# Ruta para eliminar capturas
@capturas_files.route('/eliminar_captura/<int:dato_id>', methods=['DELETE'])
@login_required
def eliminar_captura(dato_id):
    dato = Datos.query.get_or_404(dato_id)
    if dato.id_usuario != current_user.id:
        abort(403)
        
    try:
        db.session.delete(dato)
        db.session.commit()
        return '', 204
    except Exception as e:
        print(f"Error al eliminar captura: {str(e)}")
        db.session.rollback()
        abort(500)