"""
Módulo de control de capturas.

Este Blueprint maneja las operaciones de control del sistema de capturas,
incluyendo el panel de control, la activación/desactivación de capturas,
la alternancia de modos y la recepción de archivos de captura.

Las operaciones principales incluyen:
- Panel de control con visualización del estado
- Cambio entre modo automático y manual
- Activación/desactivación de capturas
- Recepción y almacenamiento de capturas desde clientes
- Consulta del estado del sistema
"""
import queue, sqlalchemy.exc, time
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

# Cola global para almacenar capturas pendientes
capturas_pendientes = queue.Queue(maxsize=100)

# Número de capturas a procesar por cada solicitud
MAX_CAPTURAS_POR_CICLO = 5

# Ruta del panel de control
@capturas_control.route('/dashboard')
@login_required
def panel_control():
    """
    Muestra el panel de control principal.
    
    Recupera las capturas del usuario actual, las agrupa por equipos y fechas,
    y muestra el estado actual del sistema de capturas.
    
    Returns:
        render_template: Página del panel de control con datos dinámicos
        
    Note:
        Requiere autenticación previa
        Muestra solo capturas del usuario autenticado
    """    
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
    """
    Alterna el estado de las capturas.
    
    En modo manual, activa o desactiva las capturas.
    En modo automático, fuerza el cambio a modo manual y activa las capturas.
    
    Returns:
        dict: Estado actualizado del sistema de capturas en formato JSON
        
    Note:
        Requiere autenticación previa
        En modo automático, cambia automáticamente a modo manual
        En modo manual, alterna entre activado/desactivado
    """
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
    """
    Alterna entre modo automático y manual.
    
    Cambia la forma en que se controla la activación de capturas:
    - Modo automático: Controlado por horarios predefinidos
    - Modo manual: Controlado directamente por el usuario
    
    Returns:
        dict: Estado actualizado del sistema de capturas en formato JSON
        
    Side Effects:
        En modo automático: Desactiva capturas y despierta el comprobador de horarios
        En modo manual: Activa capturas para el usuario actual
        
    Note:
        Requiere autenticación previa
    """
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
    """
    Recibe capturas enviadas por los clientes y las encola para procesamiento.
    
    En lugar de procesar inmediatamente en la base de datos, coloca la 
    captura en una cola y devuelve respuesta rápida al cliente.
    Posteriormente, procesa algunas capturas pendientes de la cola.
    
    Request Form:
        cliente_id (str): Identificador único del cliente
        timestamp (str): Marca temporal en formato YYYYMMDD_HHMMSS
        
    Request Files:
        data (file): Archivo de texto con contenido capturado (obligatorio)
        screenshot (file): Imagen capturada (opcional)
        
    Returns:
        str: Mensaje de confirmación o error
        
    Status Codes:
        200: Captura recibida correctamente
        400: Datos faltantes o formato incorrecto
        403: Capturas deshabilitadas o falta profesor activo
        500: Error interno del servidor
        503: Cola llena, servidor ocupado
    """
    try:
        global capture_enabled, profesor_activo
        
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

        # Preparar datos para la cola
        datos_captura = {
            'cliente_id': cliente_id,
            'profesor_activo': profesor_activo,
            'fecha': fecha,
            'texto': None,
            'imagen': None
        }

        # Procesar archivos
        archivo_texto = request.files['data']
        try:
            texto_contenido = archivo_texto.read().decode('utf-8')
            datos_captura['texto'] = texto_contenido
        except UnicodeDecodeError as e:
            print(f"[{datetime.now()}] Error decodificando texto: {str(e)}")
            return 'Error en codificación del archivo', 400

        if 'screenshot' in request.files:
            screenshot = request.files['screenshot']
            datos_captura['imagen'] = screenshot.read()

        # Intentar encolar la captura
        try:
            capturas_pendientes.put(datos_captura, block=False)
            print(f"[{datetime.now()}] Captura de {cliente_id} encolada correctamente")
            
            # Procesar algunas capturas pendientes
            procesar_capturas_pendientes()
            
            return 'OK', 200
        except queue.Full:
            print(f"[{datetime.now()}] Cola llena, rechazando captura de {cliente_id}")
            return 'Servidor ocupado, intentar más tarde', 503
        
    except Exception as e:
        print(f"[{datetime.now()}] Error inesperado: {str(e)}")
        return 'Error interno del servidor', 500


def procesar_capturas_pendientes():
    """
    Procesa algunas capturas pendientes de la cola.
    
    Esta función intenta procesar hasta MAX_CAPTURAS_POR_CICLO capturas de la cola,
    serializando las escrituras en la base de datos para evitar bloqueos.
    """
    capturas_procesadas = 0
    
    while not capturas_pendientes.empty() and capturas_procesadas < MAX_CAPTURAS_POR_CICLO:
        try:
            # Obtener la siguiente captura de la cola sin bloquear
            datos_captura = capturas_pendientes.get(block=False)
            
            # Procesar la captura
            resultado = guardar_captura_en_bd(datos_captura)
            
            # Marcar como procesada (se haya procesado correctamente o no)
            capturas_pendientes.task_done()
            
            if resultado:
                capturas_procesadas += 1
            
        except queue.Empty:
            # La cola estaba vacía
            break
        except Exception as e:
            print(f"[{datetime.now()}] Error procesando capturas pendientes: {str(e)}")
            break


def guardar_captura_en_bd(datos_captura):
    """
    Guarda una captura en la base de datos con sistema de reintentos.
    
    Args:
        datos_captura (dict): Datos de la captura a guardar
        
    Returns:
        bool: True si se guardó correctamente, False en caso de error
    """
    max_reintentos = 3
    reintentos = 0
    tiempo_espera = 0.2  # Segundos iniciales
    
    while reintentos <= max_reintentos:
        try:
            cliente_id = datos_captura['cliente_id']
            profesor_activo = datos_captura['profesor_activo']
            fecha = datos_captura['fecha']
            
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
                fecha=fecha,
                texto=datos_captura.get('texto'),
                imagen=datos_captura.get('imagen')
            )
            
            # Guardar en la base de datos
            db.session.add(nuevo_dato)
            db.session.commit()
            
            print(f"[{datetime.now()}] Captura de {cliente_id} guardada (intento {reintentos+1})")
            return True
            
        except sqlalchemy.exc.OperationalError as e:
            # Verificar si es un error de base de datos bloqueada
            error_mensaje = str(e).lower()
            if "database is locked" in error_mensaje or "sqlite_busy" in error_mensaje:
                reintentos += 1
                db.session.rollback()
                
                if reintentos <= max_reintentos:
                    # Tiempo de espera creciente
                    tiempo_espera_actual = tiempo_espera * (2 ** (reintentos - 1))
                    print(f"[{datetime.now()}] Base de datos bloqueada, esperando {tiempo_espera_actual}s")
                    time.sleep(tiempo_espera_actual)
                else:
                    print(f"[{datetime.now()}] Máximo de reintentos alcanzado")
                    return False
            else:
                # Otro tipo de error de base de datos
                print(f"[{datetime.now()}] Error de base de datos: {str(e)}")
                db.session.rollback()
                return False
        except Exception as e:
            print(f"[{datetime.now()}] Error guardando captura: {str(e)}")
            db.session.rollback()
            return False
    
    return False

# Ruta para obtener el estado de las capturas
@capturas_control.route('/capture_status')
@login_required
def get_capture_status():
    """
    Obtiene el estado actual de las capturas.
    
    Devuelve un objeto JSON con información sobre si las capturas
    están habilitadas, el modo actual, y los usuarios relacionados.
    
    Returns:
        dict: Estado del sistema de capturas en formato JSON con:
            - enabled: Si las capturas están activadas
            - modo_automatico: Si está en modo automático u manual
            - user_id: ID del profesor para el que se captura
            - current_user_id: ID del usuario actual
            
    Note:
        Requiere autenticación previa
    """
    return {
        'enabled': capture_enabled,
        'modo_automatico': modo_automatico,
        'user_id': profesor_activo,
        'current_user_id': current_user.id
    }
    
def get_estado_sistema():
    """
    Obtiene el estado del sistema sin necesitar contexto de request.
    
    Función auxiliar que proporciona el estado actual del sistema
    para uso interno, sin requerir un contexto HTTP activo.
    
    Returns:
        dict: Estado del sistema de capturas en formato JSON con:
            - enabled: Si las capturas están activadas
            - modo_automatico: Si está en modo automático u manual
            - user_id: ID del profesor para el que se captura
            
    Note:
        Función interna, no expuesta como endpoint
    """
    return {
        'enabled': capture_enabled,
        'modo_automatico': modo_automatico,
        'user_id': profesor_activo
    }

def set_capture_status(enabled, user_id, modo=None):
    """
    Actualiza el estado de las capturas.
    
    Modifica las variables globales que controlan el estado del sistema.
    
    Args:
        enabled (bool): Si las capturas deben estar activadas
        user_id (int): ID del usuario para el que se capturan datos (None si desactivado)
        modo (bool, opcional): Modo automático (True) o manual (False)
        
    Side Effects:
        Modifica las variables globales:
            - capture_enabled
            - profesor_activo
            - modo_automatico (solo si se especifica)
            
    Note:
        Función interna, no expuesta como endpoint
    """
    global capture_enabled, profesor_activo, modo_automatico
    capture_enabled = enabled
    profesor_activo = user_id
    if modo is not None:
        modo_automatico = modo