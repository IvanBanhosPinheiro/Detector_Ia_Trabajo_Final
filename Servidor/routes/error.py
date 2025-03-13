from flask import render_template
# Manejo de error 404
def paginaNoEncontrada(error):
    return render_template("errores/404.html"), 404