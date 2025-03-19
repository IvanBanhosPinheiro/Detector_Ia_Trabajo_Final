"""
Módulo de gestión de horarios.

Este Blueprint maneja las operaciones relacionadas con los horarios de profesores,
incluyendo la creación, visualización y eliminación de horarios para la detección
automática de actividades en función del tiempo.

Las operaciones principales incluyen:
- Listado de horarios existentes
- Creación de nuevos horarios
- Eliminación de horarios
- Validación de superposiciones y conflictos
"""
from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from models.models import db, Usuario, Horario
from datetime import datetime

horarios = Blueprint('horarios', __name__)

@horarios.route("/horarios")
@login_required
def lista_horarios():
    """
    Vista para listar y gestionar horarios.
    
    Muestra una página con todos los horarios configurados y un formulario
    para añadir nuevos horarios. Solo accesible para administradores.
    
    Returns:
        render_template: Página de gestión de horarios
        redirect: Redirección a página principal si no es administrador
        
    Note:
        Requiere autenticación
        Solo usuarios administradores pueden acceder a esta función
    """
    if not current_user.administrador:
        flash('No tienes permisos de administrador', 'danger')
        return redirect(url_for('index'))
        
    usuarios = Usuario.query.filter_by(administrador=False).all()
    horarios = Horario.query.all()
    return render_template("admin/horarios.html", usuarios=usuarios, horarios=horarios)

@horarios.route("/horarios", methods=['POST'])
@login_required
def crear_horario():
    """
    Añade un nuevo horario al sistema.
    
    Procesa el formulario de creación de horario y valida que no haya
    superposiciones con otros horarios existentes para el mismo día.
    
    Request Form:
        usuario (str): ID del usuario asociado al horario
        dia (int): Día de la semana (0=Lunes, 6=Domingo)
        hora_inicio (str): Hora de inicio en formato HH:MM
        hora_fin (str): Hora de fin en formato HH:MM
    
    Returns:
        JSON: Mensaje de éxito o error
        
    Status Codes:
        201: Horario creado correctamente
        400: Error de validación (horario superpuesto o horas inválidas)
        403: Usuario no autorizado
        500: Error del servidor
        
    Note:
        Solo usuarios administradores pueden crear horarios
    """
    if not current_user.administrador:
        return jsonify({'error': 'No tienes permisos de administrador'}), 403

    try:
        # Obtener datos del formulario
        usuario_id = request.form.get('usuario')
        dia = int(request.form.get('dia'))
        hora_inicio = datetime.strptime(request.form.get('hora_inicio'), '%H:%M').time()
        hora_fin = datetime.strptime(request.form.get('hora_fin'), '%H:%M').time()

        # Validar rango de horas
        if hora_inicio >= hora_fin:
            return jsonify({'error': 'La hora de inicio debe ser anterior a la hora de fin'}), 400

        # Verificar superposición de horarios
        horarios_superpuestos = Horario.query.filter(
            Horario.dia == dia,
            db.or_(
                db.and_(
                    Horario.hora_inicio <= hora_inicio,
                    Horario.hora_fin > hora_inicio
                ),
                db.and_(
                    Horario.hora_inicio < hora_fin,
                    Horario.hora_fin >= hora_fin
                )
            )
        ).first()

        if horarios_superpuestos:
            return jsonify({'error': 'Ya existe un horario en ese rango de tiempo'}), 400

        # Crear nuevo horario
        nuevo_horario = Horario(
            id_usuario=usuario_id,
            dia=dia,
            hora_inicio=hora_inicio,
            hora_fin=hora_fin
        )

        db.session.add(nuevo_horario)
        db.session.commit()

        return jsonify({'message': 'Horario creado correctamente'}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@horarios.route("/horario/<int:id>", methods=['DELETE'])
@login_required
def eliminar_horario(id):
    """
    Elimina un horario existente.
    
    Busca el horario por su ID y lo elimina de la base de datos.
    
    Args:
        id (int): ID del horario a eliminar
        
    Returns:
        str: Respuesta vacía con código 204 si se eliminó correctamente
        JSON: Mensaje de error en caso contrario
        
    Status Codes:
        204: Horario eliminado correctamente
        403: Usuario no autorizado
        404: Horario no encontrado
        500: Error del servidor
        
    Note:
        Solo usuarios administradores pueden eliminar horarios
    """
    if not current_user.administrador:
        return jsonify({'error': 'No tienes permisos de administrador'}), 403

    try:
        horario = Horario.query.get_or_404(id)
        db.session.delete(horario)
        db.session.commit()
        return '', 204

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500