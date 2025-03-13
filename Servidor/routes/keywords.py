from flask import Blueprint, request, render_template, redirect, url_for, flash, send_file, current_app
from flask_login import login_required, current_user
import os
from datetime import datetime

keywords = Blueprint('keywords', __name__)

def get_keywords_path():
    """Obtiene la ruta del archivo keywords"""
    return os.path.abspath(os.path.join(current_app.root_path, "data/keywords.txt"))

@keywords.route('/editar_keywords', methods=['GET', 'POST'])
@login_required
def editar_keywords():
    if not current_user.administrador:
        flash('No tienes permisos de administrador', 'danger')
        return redirect(url_for('dashboard'))
        
    ruta_keywords = get_keywords_path()
    
    if request.method == 'POST':
        try:
            nuevo_contenido = request.form['contenido']
            palabras = '\n'.join(line.strip() for line in nuevo_contenido.splitlines() if line.strip())
            
            with open(ruta_keywords, 'w', encoding='utf-8') as file:
                file.write(palabras)
                
            flash('Archivo actualizado correctamente', 'success')
            
        except Exception as e:
            flash(f'Error al guardar el archivo: {str(e)}', 'danger')
    
    try:
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

@keywords.route('/keywords', methods=['GET'])
def descargar_keywords():
    ruta_keywords = get_keywords_path()
    try:
        if not os.path.exists(ruta_keywords):
            print(f"[{datetime.now()}] Error: No se encuentra el archivo keywords en: {ruta_keywords}")
            return 'Archivo de palabras clave no encontrado', 404

        return send_file(
            ruta_keywords,
            mimetype='text/plain',
            as_attachment=True,
            download_name='keywords.txt'
        )

    except Exception as e:
        print(f"[{datetime.now()}] Error al servir keywords.txt: {str(e)}")
        return 'Error interno del servidor', 500