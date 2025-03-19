"""
Módulo de modelos de datos.

Define las estructuras de datos para la aplicación mediante SQLAlchemy ORM,
incluyendo los modelos para usuarios, equipos, capturas de datos y horarios.

Los modelos implementados son:
- Usuario: Usuarios del sistema (administradores y profesores)
- Equipo: Computadoras que envían capturas al servidor
- Datos: Capturas de pantalla y texto extraído
- Horario: Configuración de horarios para capturas automáticas
"""
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin

db = SQLAlchemy()

class Usuario(UserMixin, db.Model): # UserMixin agrega métodos necesarios para Flask-Login
    """
    Modelo de usuario del sistema.
    
    Representa tanto a administradores como profesores. Hereda de UserMixin
    para proporcionar los métodos necesarios para Flask-Login.
    
    Attributes:
        id (int): Identificador único del usuario
        nombre (str): Nombre de usuario único
        password_hash (str): Hash de la contraseña (nunca la contraseña en texto plano)
        administrador (bool): Indica si el usuario tiene permisos de administrador
        datos (relationship): Relación con las capturas asociadas al usuario
        horarios (relationship): Relación con los horarios asociados al usuario
        
    Note:
        Los usuarios con administrador=True tienen acceso a todas las
        funciones administrativas del sistema
    """
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    administrador = db.Column(db.Boolean, default=False)
    datos = db.relationship('Datos', backref='usuario', lazy=True)
    horarios = db.relationship('Horario', backref='usuario', lazy=True)

    def set_password(self, password):
        """
        Establece la contraseña del usuario.
        
        Convierte la contraseña en texto plano a un hash seguro
        para almacenamiento en la base de datos.
        
        Args:
            password (str): Contraseña en texto plano
            
        Note:
            La contraseña original nunca se almacena, solo su hash
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Verifica si la contraseña proporcionada es correcta.
        
        Compara la contraseña en texto plano con el hash almacenado.
        
        Args:
            password (str): Contraseña a verificar
            
        Returns:
            bool: True si la contraseña es correcta, False en caso contrario
        """
        return check_password_hash(self.password_hash, password)

class Equipo(db.Model):
    """
    Modelo de equipo o dispositivo cliente.
    
    Representa un equipo o computadora que envía capturas al servidor.
    
    Attributes:
        id (int): Identificador único del equipo
        nombre (str): Nombre único del equipo (generalmente su identificador de red)
        datos (relationship): Relación con las capturas generadas por este equipo
    """
    __tablename__ = 'equipos'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False, unique=True)
    datos = db.relationship('Datos', backref='equipo', lazy=True)

class Datos(db.Model):
    """
    Modelo de datos capturados.
    
    Almacena la información capturada por los clientes, incluyendo
    imágenes de pantalla y texto extraído.
    
    Attributes:
        id (int): Identificador único de la captura
        id_usuario (int): ID del usuario (profesor) propietario de la captura
        id_equipo (int): ID del equipo que generó la captura
        fecha (datetime): Fecha y hora de la captura
        imagen (LargeBinary): Datos binarios de la imagen capturada
        texto (Text): Texto extraído de la captura o enviado por el cliente
        usuario (relationship): Relación con el usuario propietario
        equipo (relationship): Relación con el equipo origen
    """
    __tablename__ = 'datos'
    
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    id_equipo = db.Column(db.Integer, db.ForeignKey('equipos.id'), nullable=False)
    fecha = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    imagen = db.Column(db.LargeBinary)  # Para guardar la imagen directamente
    texto = db.Column(db.Text)
    
class Horario(db.Model):
    """
    Modelo de horario para capturas automáticas.
    
    Define períodos de tiempo en los que el sistema capturará
    automáticamente la actividad de los equipos para un usuario específico.
    
    Attributes:
        id (int): Identificador único del horario
        hora_inicio (Time): Hora de inicio del período de captura
        hora_fin (Time): Hora de finalización del período de captura
        dia (int): Día de la semana (0=Lunes, 6=Domingo)
        id_usuario (int): ID del usuario (profesor) asociado con este horario
        usuario (relationship): Relación con el usuario propietario
        
    Note:
        En modo automático, el sistema utilizará estos horarios para
        activar y desactivar las capturas sin intervención manual
    """
    __tablename__ = 'horarios'
    
    id = db.Column(db.Integer, primary_key=True)
    hora_inicio = db.Column(db.Time, nullable=False)
    hora_fin = db.Column(db.Time, nullable=False)
    dia = db.Column(db.Integer, nullable=False)  # 0=Lunes, 6=Domingo
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)