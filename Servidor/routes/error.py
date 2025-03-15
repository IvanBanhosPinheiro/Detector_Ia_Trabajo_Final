from flask import Blueprint, render_template

error = Blueprint('error', __name__)

@error.app_errorhandler(404)
def paginaNoEncontrada(error):
    return render_template("errores/404.html"), 404