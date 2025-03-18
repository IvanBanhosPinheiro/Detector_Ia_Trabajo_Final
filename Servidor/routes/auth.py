# Imports necesarios de Flask y sus extensiones
from flask import Blueprint, request, render_template, redirect, url_for, flash, jsonify
from flask_login import login_user, login_required, current_user, logout_user
# Imports de modelos
from models.models import Usuario, db, Datos


# Creación del blueprint de autenticación
auth = Blueprint('auth', __name__)

# Ruta para el login de usuarios
@auth.route('/login', methods=['GET', 'POST'])
def login():
    # Si ya está autenticado, redirigir al panel
    if current_user.is_authenticated:
        return redirect(url_for('capturas_control.panel_control'))

    # Si es una petición POST, procesar el formulario
    if request.method == 'POST':
        nombre = request.form['usuario']
        password = request.form['password']
        
        # Buscar usuario en la base de datos
        usuario = Usuario.query.filter_by(nombre=nombre).first()
        
        # Verificar credenciales
        if usuario and usuario.check_password(password):
            login_user(usuario)
            flash('Has iniciado sesión correctamente', 'success')
            return redirect(url_for('capturas_control.panel_control'))
        
        # Credenciales incorrectas
        flash('Usuario o contraseña incorrectos', 'danger')
        return render_template('auth/login.html'), 401
    
    # Si es GET, mostrar formulario
    return render_template('auth/login.html')

# Ruta para registrar un nuevo usuario
@auth.route("/registro", methods=['GET', 'POST'])
@login_required
def registro():
    # Verificar permisos de administrador
    if not current_user.administrador:
        flash('No tienes permisos de administrador', 'danger')
        return redirect(url_for('capturas_control.panel_control'))

    # Si es POST, procesar el formulario
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
        
        # Intentar guardar en la base de datos
        try:
            db.session.add(nuevo_usuario)
            db.session.commit()
            flash('Usuario registrado correctamente', 'success')
            return redirect(url_for('auth.lista_usuarios'))
        except Exception as e:
            db.session.rollback()
            flash('Error al registrar usuario', 'danger')
                    
    # Si es GET o falló el registro, mostrar formulario
    return render_template("auth/registro.html")

# Ruta para cerrar sesión
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión correctamente', 'success')
    return redirect(url_for('auth.login'))

# Ruta para ver la lista de usuarios
@auth.route("/usuarios")
@login_required
def lista_usuarios():
    # Verificar permisos de administrador
    if not current_user.administrador:
        flash('No tienes permisos de administrador', 'danger')
        return redirect(url_for('capturas_control.panel_control'))
        
    # Obtener todos los usuarios
    usuarios = Usuario.query.all()
    return render_template("admin/usuarios.html", usuarios=usuarios)

# Ruta para eliminar un usuario
@auth.route("/usuario/<int:id>", methods=['DELETE'])
@login_required
def eliminar_usuario(id):
    # Verificar permisos de administrador
    if not current_user.administrador:
        flash('No tienes permisos de administrador', 'danger')
        return 'No autorizado', 403
        
    # Buscar usuario y verificar que no sea admin
    usuario = Usuario.query.get_or_404(id)
    if usuario.administrador:
        return 'No se puede eliminar un administrador', 400
        
    try:
        # Primero eliminar todas las capturas asociadas
        capturas = Datos.query.filter_by(id_usuario=id).all()
        for captura in capturas:
            # Eliminar registro de la base de datos
            db.session.delete(captura)
            
        # Luego eliminar el usuario
        db.session.delete(usuario)
        db.session.commit()
        return 'Usuario y sus capturas eliminados correctamente', 200
        
    except Exception as e:
        db.session.rollback()
        print(f"Error al eliminar usuario: {str(e)}")
        return 'Error al eliminar usuario', 500

# Ruta para cambiar la contraseña del usuario actual
@auth.route('/cambiar_password_admin/<int:id>', methods=['POST'])
@login_required
def cambiar_password_admin(id):
    """Cambia la contraseña de un usuario (solo admin)"""
    if not current_user.administrador:
        return jsonify({'error': 'Solo los administradores pueden cambiar contraseñas'}), 403

    # No permitir cambiar contraseña de administradores
    usuario = Usuario.query.get_or_404(id)
    if usuario.administrador:
        return jsonify({'error': 'No se puede cambiar la contraseña de un administrador'}), 400

    data = request.get_json()
    new_password = data.get('new_password')

    if not new_password:
        return jsonify({'error': 'La contraseña no puede estar vacía'}), 400

    try:
        usuario.set_password(new_password)
        db.session.commit()
        return jsonify({'message': f'Contraseña actualizada correctamente para {usuario.nombre}'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error al actualizar la contraseña'}), 500