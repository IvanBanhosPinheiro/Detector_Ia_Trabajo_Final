"""
Módulo de manejo de errores HTTP.

Este Blueprint gestiona las respuestas a errores HTTP comunes,
proporcionando páginas personalizadas que mantienen la experiencia
de usuario consistente incluso cuando ocurren errores.

Las páginas de error incluidas son:
- Error 404 (Página no encontrada)
"""
from flask import Blueprint, render_template

error = Blueprint('error', __name__)

@error.app_errorhandler(404)
def paginaNoEncontrada(error):
    """
    Maneja el error 404 (Página no encontrada).
    
    Intercepta las peticiones a rutas inexistentes y devuelve una
    página personalizada con un mensaje amigable para el usuario.
    
    Args:
        error: Objeto de error proporcionado por Flask
        
    Returns:
        tuple: Template renderizado y código de estado HTTP 404
        
    Example:
        Cuando un usuario accede a /ruta-inexistente, en lugar de
        mostrar el error estándar del servidor, se muestra una
        plantilla personalizada manteniendo el diseño del sitio.
    """
    return render_template("errores/404.html"), 404