"""
Módulo principal de la aplicación Flask.
Configura y arranca el servidor web con todas sus funcionalidades.

Imports:
    flask: Framework web utilizado para crear la aplicación
    flask_login: Gestión de autenticación de usuarios
    configparser: Lectura de archivos de configuración
"""
from flask import Flask, render_template
from flask_login import LoginManager
import configparser



#Importamos la rutas absolutas
from routes.ruta_abs import get_data_path

# Importamos los modelos
from models.models import db, Usuario 

# Importar y registrar blueprints después de la configuración
from routes.auth import auth
from routes.error import paginaNoEncontrada
from routes.keywords import keywords
from routes.capturas.capturas_control import capturas_control
from routes.capturas.capturas_view import capturas_view
from routes.capturas.capturas_files import capturas_files
from routes.horarios import horarios
from routes.error import error

# Importamos el hilo de comprobación de horarios
from background_process.horario_checker import HorarioChecker



# Inicialización de Flask
app = Flask(__name__)

"""
Configuración principal de Flask:
    SECRET_KEY: Clave secreta para sesiones
    SQLALCHEMY_DATABASE_URI: Ubicación de la base de datos SQLite
    SQLALCHEMY_TRACK_MODIFICATIONS: Desactivar tracking de modificaciones
"""
# Configuración de la aplicación
app.config['SECRET_KEY'] = '3-H^fJTYrwi4hjs'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Cargar configuración desde config.ini
config_path = get_data_path('config.ini')
config = configparser.ConfigParser()
config.read(config_path)
port = int(config['Servidor']['puerto'])

# Inicialización de extensiones
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

# Función para cargar usuario en Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# Ruta principal
@app.route("/")
def index():
    return render_template("index.html")

"""
Registro de Blueprints:
    auth: Gestión de autenticación y usuarios
    error: Manejo de errores HTTP
    keywords: Gestión de palabras clave
    capturas_*: Módulos relacionados con la captura de pantalla
        - control: Activación/desactivación de capturas
        - view: Visualización de capturas
        - files: Gestión de archivos de capturas
    horarios: Gestión de horarios de profesores
"""
app.register_blueprint(auth)
app.register_blueprint(keywords)
app.register_blueprint(capturas_control)
app.register_blueprint(capturas_files)
app.register_blueprint(capturas_view)
app.register_blueprint(horarios)
app.register_blueprint(error)

# Punto de entrada principal
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Crear usuario admin si no existe
        usuario = config['Servidor']['usuario']
        password = config['Servidor']['password']
        
        admin = Usuario.query.filter_by(nombre=usuario).first()
        if not admin:
            admin = Usuario(nombre=usuario, administrador=True)
            admin.set_password(password)
            db.session.add(admin)
            db.session.commit()
            print('Usuario administrador creado:')
            print(f'Usuario: {usuario}')
            print('Contraseña: ********')
    
    app.register_error_handler(404, paginaNoEncontrada)   
    # Iniciar proceso de comprobación de horarios
    horario_checker = HorarioChecker(app)
    app.horario_checker = horario_checker  # Guardar referencia al hilo en la aplicación
    horario_checker.start()
    
    # Arrancar servidor
    app.run(host='0.0.0.0', port=port)