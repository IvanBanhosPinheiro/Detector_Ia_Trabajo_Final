from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from models.models import db, Usuario, Horario
from datetime import datetime

horarios = Blueprint('horarios', __name__)

@horarios.route("/horarios")
@login_required
def lista_horarios():
    """Vista para listar y gestionar horarios"""
    if not current_user.administrador:
        flash('No tienes permisos de administrador', 'danger')
        return redirect(url_for('index'))
        
    usuarios = Usuario.query.filter_by(administrador=False).all()
    horarios = Horario.query.all()
    return render_template("admin/horarios.html", usuarios=usuarios, horarios=horarios)

@horarios.route("/horarios", methods=['POST'])
@login_required
def crear_horario():
    """Añadir nuevo horario"""
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
    """Eliminar un horario"""
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