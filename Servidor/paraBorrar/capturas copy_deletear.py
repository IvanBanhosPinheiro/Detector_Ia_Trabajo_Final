from flask import Blueprint, request, render_template, redirect, url_for, flash, send_file, abort
# Imports de Flask-Login
from flask_login import login_required, current_user

# Imports de modelos
from models.models import Equipo, Datos, db

# Imports de sistema y utilidades
import io
from datetime import datetime, timedelta
from PIL import Image

capturas = Blueprint('capturas', __name__)

# Variables globales para control de capturas
capture_enabled = False
profesor_activo = None

# Ruta para ver capturas de un equipo
@capturas.route('/equipo/<equipo_id>')
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
@capturas.route('/equipo/<equipo_id>/fecha/<fecha>')
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
@capturas.route('/miniatura/<int:dato_id>')
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

# Ruta para eliminar capturas de un día
@capturas.route('/eliminar_fecha/<equipo_id>/<fecha>', methods=['DELETE'])
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
            Datos.fecha >= fecha_dt,
            Datos.fecha < fecha_siguiente
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
@capturas.route('/descargar_imagen/<int:dato_id>')
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
@capturas.route('/descargar_texto/<int:dato_id>')
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
@capturas.route('/eliminar_captura/<int:dato_id>', methods=['DELETE'])
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
        
# Ruta del panel de control
@capturas.route('/dashboard')
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
    
    return render_template('dashboard.html', 
                         capture_enabled=capture_enabled,
                         equipos=equipos)
    
    
# Ruta para habilitar/deshabilitar capturas
@capturas.route('/toggle_capture', methods=['POST'])
@login_required
def toggle_capture():
    global capture_enabled, profesor_activo
    print(f"DEBUG - Estado anterior: capture_enabled={capture_enabled}, profesor_activo={profesor_activo}")
    
    capture_enabled = not capture_enabled
    profesor_activo = current_user.id if capture_enabled else None
    
    print(f"DEBUG - Nuevo estado: capture_enabled={capture_enabled}, profesor_activo={profesor_activo}")
    
    return {'status': 'enabled' if capture_enabled else 'disabled'}


# Ruta para recibir capturas
@capturas.route('/uploads', methods=['POST'])
def upload():
    try:
        global capture_enabled, profesor_activo
        # Debug: Imprimir todos los datos recibidos
        print(f"[{datetime.now()}] Form data: {request.form}")
        print(f"[{datetime.now()}] Files: {request.files}")
        
        # Verificar que las capturas están habilitadas y hay un profesor activo
        if not capture_enabled or profesor_activo is None:
            print(f"[{datetime.now()}] Estado capturas: {capture_enabled}, Profesor activo: {profesor_activo}")
            return 'Capturas deshabilitadas', 403

        # Obtener datos del formulario con verificación
        if 'cliente_id' not in request.form:
            print(f"[{datetime.now()}] Falta cliente_id en el formulario")
            return 'Falta cliente_id', 400
            
        if 'timestamp' not in request.form:
            print(f"[{datetime.now()}] Falta timestamp en el formulario")
            return 'Falta timestamp', 400

        cliente_id = request.form['cliente_id']
        timestamp_str = request.form['timestamp']

        # Convertir el timestamp del formato '20250312_192909' a datetime
        try:
            fecha = datetime.strptime(timestamp_str, '%Y%m%d_%H%M%S')
        except ValueError as e:
            print(f"[{datetime.now()}] Error al parsear timestamp: {str(e)}")
            return 'Formato de timestamp inválido', 400

        # Verificar archivos requeridos
        if 'data' not in request.files:
            print(f"[{datetime.now()}] Falta archivo data")
            return 'Falta archivo data', 400

        # Buscar o crear el equipo
        equipo = Equipo.query.filter_by(nombre=cliente_id).first()
        if not equipo:
            equipo = Equipo(nombre=cliente_id)
            db.session.add(equipo)
            db.session.commit()

        # Crear nuevo registro de datos
        nuevo_dato = Datos(
            id_usuario=profesor_activo,
            id_equipo=equipo.id,
            fecha=fecha
        )

        # Guardar el contenido del archivo de texto
        archivo_texto = request.files['data']
        try:
            texto_contenido = archivo_texto.read().decode('utf-8')
            nuevo_dato.texto = texto_contenido
        except UnicodeDecodeError as e:
            print(f"[{datetime.now()}] Error decodificando texto: {str(e)}")
            return 'Error en codificación del archivo', 400

        # Guardar screenshot si existe
        if 'screenshot' in request.files:
            screenshot = request.files['screenshot']
            nuevo_dato.imagen = screenshot.read()

        # Guardar en la base de datos
        db.session.add(nuevo_dato)
        db.session.commit()

        print(f"[{datetime.now()}] Datos recibidos correctamente de {cliente_id} para profesor {profesor_activo}")
        return 'OK', 200
        
    except Exception as e:
        print(f"[{datetime.now()}] Error inesperado: {str(e)}")
        db.session.rollback()
        return 'Error interno del servidor', 500

# Ruta para ver imágenes guardadas
@capturas.route('/ver_imagen/<int:dato_id>')
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