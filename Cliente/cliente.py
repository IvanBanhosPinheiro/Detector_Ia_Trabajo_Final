import os, configparser, time, pyautogui, requests, pytesseract, pickle
from datetime import datetime
import pygetwindow as gw
from io import BytesIO


# Configuración
config = configparser.ConfigParser()

# config_path = os.path.join(os.getcwd(), 'config.ini')
config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'config.ini'))
config.read(config_path)

# Configuración de Tesseract
pytesseract.pytesseract.tesseract_cmd = config['Cliente']['ruta']

# Configuración del cliente
url_servidor = config['Cliente']['url_servidor']

# URL para descargar el archivo de palabras clave del servidor
url_keywords = f"{url_servidor}/keywords"

# Generar un identificador único para cada cliente usando el nombre del equipo
cliente_id = os.environ.get('COMPUTERNAME', 'unknown_client')

# Variable para almacenar la ventana activa anterior
ventana_activa_anterior = None


if __name__ == "__main__":
    print(config_path)
    print(url_keywords)
    print(url_servidor)
    print(cliente_id)