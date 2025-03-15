from flask import Flask, request, render_template
from flask_login import LoginManager
import os, configparser

# Importamos los modelos
from models.models import db, Usuario 

# Importar y registrar blueprints después de la configuración
from routes.auth import auth
from routes.error import paginaNoEncontrada
from routes.keywords import keywords
from routes.capturas.capturas_control import capturas_control
from routes.capturas.capturas_view import capturas_view
from routes.capturas.capturas_files import capturas_files
from routes.error import error


# Inicialización de Flask
app = Flask(__name__)

# Configuración de la aplicación
app.config['SECRET_KEY'] = '3-H^fJTYrwi4hjs'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Cargar configuración desde config.ini
config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/config.ini'))
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


app.register_blueprint(auth)
app.register_blueprint(keywords)
app.register_blueprint(capturas_control)
app.register_blueprint(capturas_files)
app.register_blueprint(capturas_view)
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
    app.run(host='0.0.0.0', port=port)