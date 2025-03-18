from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin

db = SQLAlchemy()

class Usuario(UserMixin, db.Model): # UserMixin agrega métodos necesarios para Flask-Login
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    administrador = db.Column(db.Boolean, default=False)
    datos = db.relationship('Datos', backref='usuario', lazy=True)
    horarios = db.relationship('Horario', backref='usuario', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Equipo(db.Model):
    __tablename__ = 'equipos'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False, unique=True)
    datos = db.relationship('Datos', backref='equipo', lazy=True)

class Datos(db.Model):
    __tablename__ = 'datos'
    
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    id_equipo = db.Column(db.Integer, db.ForeignKey('equipos.id'), nullable=False)
    fecha = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    imagen = db.Column(db.LargeBinary)  # Para guardar la imagen directamente
    texto = db.Column(db.Text)
    
class Horario(db.Model):
    __tablename__ = 'horarios'
    
    id = db.Column(db.Integer, primary_key=True)
    hora_inicio = db.Column(db.Time, nullable=False)
    hora_fin = db.Column(db.Time, nullable=False)
    dia = db.Column(db.Integer, nullable=False)  # 0=Lunes, 6=Domingo
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)