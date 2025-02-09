#Realizado con un entorno virtual de conta con la version python 3.8.20
from flask import Flask, request
import os, configparser
from datetime import datetime



app = Flask(__name__)

# Directorio para guardar las capturas de pantalla y alertas recibidas
#ruta_guardado_capturas = os.path.join(os.path.dirname(__file__), 'screenshots_recibidas')
ruta_guardado_capturas = os.path.join(os.path.dirname(__file__), 'screenshots_recibidas')
if not os.path.exists(ruta_guardado_capturas):
    os.makedirs(ruta_guardado_capturas)

#config_path = os.path.join(os.getcwd(), 'config.ini')
config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'config.ini'))

# Cargar configuración desde config.ini
config = configparser.ConfigParser()
config.read(config_path)
port = int(config['Servidor']['puerto'])

# Ruta para el archivo de palabras clave
#ruta_keywords = os.path.abspath(os.path.join(os.path.dirname(__file__), 'keywords.txt'))
ruta_keywords = os.path.join(os.getcwd(), 'keywords.txt')


if __name__ == '__main__':
    print(ruta_guardado_capturas)
    print(port)
    app.run(host='127.0.0.1', port=port)
    