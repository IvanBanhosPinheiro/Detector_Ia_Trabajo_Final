from flask import Flask, request, render_template, redirect, url_for, flash, send_file, abort
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from models import db, Usuario, Equipo, Datos  # Importamos los modelos
import os, configparser, io
from datetime import datetime, timedelta
from PIL import Image

# Inicialización de Flask
app = Flask(__name__)

# Configuración de la aplicación
app.config['SECRET_KEY'] = '3-H^fJTYrwi4hjs'  # Clave secreta para sesiones
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # URI de la base de datos
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Desactivar tracking de modificaciones

# Inicialización de extensiones
db.init_app(app)  # Inicializar SQLAlchemy
login_manager = LoginManager()  # Gestor de login
login_manager.init_app(app)
login_manager.login_view = 'login'  # Vista para el login

# Variable global para control de capturas
capture_enabled = False
# Variable global para control de profesor activo
profesor_activo = None

# Cargar configuración desde config.ini
config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'config.ini'))
config = configparser.ConfigParser()
config.read(config_path)
port = int(config['Servidor']['puerto'])

# Ruta para el archivo de palabras clave
ruta_keywords = os.path.abspath(os.path.join(os.path.dirname(__file__), config['Servidor']['ruta_keywords']))
# ruta_keywords = os.path.join(os.getcwd(), 'keywords.txt')

# Función para cargar usuario en Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# Ruta principal
@app.route("/")
def index():
    return render_template("index.html")

# Ruta de login
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        usuario = Usuario.query.filter_by(nombre=request.form['usuario']).first()
        if usuario and usuario.check_password(request.form['password']):
            login_user(usuario)
            return redirect(url_for('dashboard'))
        flash('Usuario o contraseña incorrectos')
    return render_template("auth/login.html")

@app.route("/usuarios")
@login_required
def lista_usuarios():
    # Verificar si el usuario actual es administrador
    if not current_user.administrador:
        flash('No tienes permisos de administrador', 'danger')
        return redirect(url_for('dashboard'))
        
    usuarios = Usuario.query.all()
    return render_template("admin/usuarios.html", usuarios=usuarios)

@app.route("/registro", methods=['GET', 'POST'])
@login_required
def registro():
    # Verificar si el usuario actual es administrador
    if not current_user.administrador:
        flash('No tienes permisos de administrador', 'danger')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        nombre = request.form['usuario']
        password = request.form['password']
        password_confirm = request.form['password_confirm']
        
        # Verificar si el usuario ya existe
        if Usuario.query.filter_by(nombre=nombre).first():
            flash('El nombre de usuario ya está en uso', 'danger')
            return render_template("auth/registro.html")
            
        # Verificar que las contraseñas coincidan
        if password != password_confirm:
            flash('Las contraseñas no coinciden', 'danger')
            return render_template("auth/registro.html")
            
        # Crear nuevo usuario profesor
        nuevo_usuario = Usuario(
            nombre=nombre,
            administrador=False  # Los nuevos usuarios no son administradores
        )
        nuevo_usuario.set_password(password)
        
        try:
            db.session.add(nuevo_usuario)
            db.session.commit()
            flash('Usuario registrado correctamente', 'success')
            return redirect(url_for('lista_usuarios'))
        except Exception as e:
            db.session.rollback()
            flash('Error al registrar usuario', 'danger')
                    
    return render_template("auth/registro.html")

@app.route("/usuario/<int:id>", methods=['DELETE'])
@login_required
def eliminar_usuario(id):
    if not current_user.administrador:
        return 'No autorizado', 403
        
    # No permitir eliminar al admin
    usuario = Usuario.query.get_or_404(id)
    if usuario.administrador:
        return 'No se puede eliminar un administrador', 400
        
    try:
        db.session.delete(usuario)
        db.session.commit()
        return 'OK', 200
    except Exception as e:
        db.session.rollback()
        return 'Error al eliminar usuario', 500

# Ruta de logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Ruta del panel de control
@app.route('/dashboard')
@login_required
def dashboard():
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

# Ruta para ver capturas de un equipo
@app.route('/equipo/<equipo_id>')
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
@app.route('/equipo/<equipo_id>/fecha/<fecha>')
@login_required
def ver_fecha(equipo_id, fecha):
    try:
        # Convertir la fecha de string a datetime
        fecha_dt = datetime.strptime(fecha, '%Y-%m-%d')
        fecha_siguiente = fecha_dt + timedelta(days=1)
        
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
        return redirect(url_for('ver_equipo', equipo_id=equipo_id))

# Ruta para ver una captura
@app.route('/miniatura/<int:dato_id>')
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
@app.route('/eliminar_fecha/<equipo_id>/<fecha>', methods=['DELETE'])
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
@app.route('/descargar_imagen/<int:dato_id>')
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
@app.route('/descargar_texto/<int:dato_id>')
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
@app.route('/eliminar_captura/<int:dato_id>', methods=['DELETE'])
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

# Ruta para activar/desactivar capturas
@app.route('/toggle_capture', methods=['POST'])
@login_required
def toggle_capture():
    global capture_enabled, profesor_activo
    capture_enabled = not capture_enabled
    profesor_activo = current_user.id if capture_enabled else None
    return {'status': 'enabled' if capture_enabled else 'disabled'}

# Ruta para editar palabras clave
@app.route('/editar_keywords', methods=['GET', 'POST'])
@login_required
def editar_keywords():
    if not current_user.administrador:
        flash('No tienes permisos de administrador', 'danger')
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        try:
            # Obtener el contenido del formulario
            nuevo_contenido = request.form['contenido']
            
            # Eliminar saltos de línea múltiples manteniendo los simples
            palabras = '\n'.join(line.strip() for line in nuevo_contenido.splitlines() if line.strip())
            
            # Guardar el contenido
            with open(ruta_keywords, 'w', encoding='utf-8') as file:
                file.write(palabras)
                
            flash('Archivo actualizado correctamente', 'success')
            
        except Exception as e:
            flash(f'Error al guardar el archivo: {str(e)}', 'danger')
            
    try:
        # Leer el contenido actual del archivo
        if os.path.exists(ruta_keywords):
            with open(ruta_keywords, 'r', encoding='utf-8') as file:
                contenido = file.read()
        else:
            contenido = ''
            flash('El archivo no existe. Se creará al guardar.', 'warning')
            
    except Exception as e:
        contenido = ''
        flash(f'Error al leer el archivo: {str(e)}', 'danger')
        
    return render_template('admin/editarKeywords.html', contenido=contenido)

# Ruta para descargar el archivo de palabras clave
@app.route('/keywords', methods=['GET'])
def descargar_keywords():
    """Endpoint para que los clientes descarguen el archivo de palabras clave"""
    try:
        # Verificar que el archivo existe
        if not os.path.exists(ruta_keywords):
            print(f"[{datetime.now()}] Error: No se encuentra el archivo keywords en: {ruta_keywords}")
            return 'Archivo de palabras clave no encontrado', 404

        # Enviar el archivo
        return send_file(
            ruta_keywords,
            mimetype='text/plain',
            as_attachment=True,
            download_name='keywords.txt'
        )

    except Exception as e:
        print(f"[{datetime.now()}] Error al servir keywords.txt: {str(e)}")
        return 'Error interno del servidor', 500
    
    
# Ruta para recibir capturas
@app.route('/uploads', methods=['POST'])
def upload():
    try:
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
@app.route('/ver_imagen/<int:dato_id>')
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

# Manejo de error 404
def paginaNoEncontrada(error):
    return render_template("errores/404.html"), 404

# Punto de entrada principal
if __name__ == '__main__':
    # Crear todas las tablas de la base de datos
    with app.app_context():
        db.create_all()
        
        # Obtener credenciales del admin desde config.ini
        usuario = config['Servidor']['usuario']
        password = config['Servidor']['password']
        
        # Crear usuario admin si no existe
        admin = Usuario.query.filter_by(nombre=usuario).first()
        if not admin:
            admin = Usuario(
                nombre=usuario,
                administrador=True
            )
            admin.set_password(password)
            db.session.add(admin)
            db.session.commit()
            print('Usuario administrador creado:')
            print(f'Usuario: {usuario}')
            print('Contraseña: ********')
    
    # Registrar manejador de error 404
    app.register_error_handler(404, paginaNoEncontrada)
    
    # Iniciar el servidor
    app.run(host='0.0.0.0', port=port)