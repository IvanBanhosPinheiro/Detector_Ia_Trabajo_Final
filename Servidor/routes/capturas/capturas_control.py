from flask import Blueprint, request, render_template, current_app
# Imports de Flask-Login
from flask_login import login_required, current_user

# Imports de modelos
from models.models import Equipo, Datos, db, Usuario

# Imports de sistema y utilidades
from datetime import datetime


capturas_control = Blueprint('capturas_control', __name__)

# Variables globales para control de capturas
capture_enabled = False  # Estado de captura
profesor_activo = None  # ID del profesor actualmente capturando
modo_automatico = True  # Control por horario (True) o manual (False)


# Ruta del panel de control
@capturas_control.route('/dashboard')
@login_required
def panel_control():    
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
   # Obtener nombre del usuario activo si existe
    nombre_usuario = None
    if profesor_activo:
        usuario = Usuario.query.get(profesor_activo)
        if usuario:
            nombre_usuario = usuario.nombre
    
    return render_template('dashboard.html', 
                         capture_enabled=capture_enabled,
                         modo_automatico=modo_automatico,
                         user = nombre_usuario,
                         equipos=equipos)
    
    
# Ruta para habilitar/deshabilitar capturas
@capturas_control.route('/toggle_capture', methods=['POST'])
@login_required
def toggle_capture():
    """Alterna el estado de las capturas"""
    estado = get_estado_sistema()
    
    if estado['modo_automatico']:
        # Cambiar a modo manual
        set_capture_status(True, current_user.id, modo=False)
    else:
        # Alternar estado en modo manual
        nuevo_estado = not estado['enabled']
        set_capture_status(
            enabled=nuevo_estado,
            user_id=current_user.id if nuevo_estado else None
        )
    
    return get_capture_status()

# Ruta para cambiar el modo de capturas
@capturas_control.route('/toggle_modo', methods=['POST'])
@login_required
def toggle_modo():
    """Alterna entre modo automático y manual"""
    estado = get_estado_sistema()
    nuevo_modo = not estado['modo_automatico']
    
    if nuevo_modo:  # Cambio a automático
        set_capture_status(False, None, modo=True)
        # Despertar al hilo para que compruebe horarios
        if hasattr(current_app, 'horario_checker'):
            current_app.horario_checker.despertar()
    else:  # Cambio a manual
        set_capture_status(True, current_user.id, modo=False)
    
    return get_capture_status()

# Ruta para recibir capturas
@capturas_control.route('/uploads', methods=['POST'])
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

# Ruta para obtener el estado de las capturas
@capturas_control.route('/capture_status')
@login_required
def get_capture_status():
    """Obtiene el estado actual de las capturas"""
    return {
        'enabled': capture_enabled,
        'modo_automatico': modo_automatico,
        'user_id': profesor_activo,
        'current_user_id': current_user.id
    }
    
def get_estado_sistema():
    """Obtiene el estado del sistema sin necesitar contexto de request"""
    return {
        'enabled': capture_enabled,
        'modo_automatico': modo_automatico,
        'user_id': profesor_activo
    }

def set_capture_status(enabled, user_id, modo=None):
    """Actualiza el estado de las capturas"""
    global capture_enabled, profesor_activo, modo_automatico
    capture_enabled = enabled
    profesor_activo = user_id
    if modo is not None:
        modo_automatico = modo