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

# Función para descargar el archivo de palabras clave del servidor
def descargar_keywords():
    try:
        print(f"[{datetime.now()}] Intentando descargar las palabras clave desde: {url_keywords}")
        response = requests.get(url_keywords)
        if response.status_code == 200:
            keywords = response.text.splitlines()  # Convertir el texto en lista de palabras clave
            with open('keywords.pkl', 'wb') as file:
                pickle.dump(keywords, file)
            print(f"[{datetime.now()}] Archivo de palabras clave descargado exitosamente.")
        else:
            print(f"[{datetime.now()}] Error al descargar el archivo de palabras clave: {response.status_code}")
            print(f"[{datetime.now()}] Respuesta del servidor: {response.text}")
    except Exception as e:
        print(f"[{datetime.now()}] Error al descargar el archivo de palabras clave: {str(e)}")


# Función para tomar captura de pantalla
def tomar_captura_pantalla():
    # Tomar captura de pantalla
    screenshot = pyautogui.screenshot()
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    # Guardar la captura en un objeto BytesIO en lugar de guardarla en disco
    screenshot_bytes_io = BytesIO()
    screenshot.save(screenshot_bytes_io, format='PNG')
    screenshot_bytes_io.seek(0)
    return screenshot_bytes_io, screenshot, timestamp

# Función para enviar una alerta al servidor
def enviar_alerta_servidor(screenshot_bytes_io, txt_data, timestamp):
    try:
        files = {
            'screenshot': ('screenshot.png', screenshot_bytes_io, 'image/png'),
            'data': ('alerta.txt', txt_data, 'text/plain')
        }
        data = {
            "cliente_id": cliente_id, 
            "timestamp": str(timestamp)  # Asegúrate de que timestamp sea string
        }
        
        print(f"[{datetime.now()}] Enviando datos: {data}")
        print(f"[{datetime.now()}] Archivos: {[k for k in files.keys()]}")
        
        response = requests.post(f"{url_servidor}/uploads", files=files, data=data)
        
        print(f"[{datetime.now()}] Respuesta: {response.status_code} - {response.text}")
        
        if response.status_code == 200:
            print(f"[{datetime.now()}] Alerta enviada exitosamente")
        else:
            print(f"[{datetime.now()}] Error al enviar la alerta: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[{datetime.now()}] Error al enviar la alerta: {str(e)}")

def cargar_keywords():
    """
    Esta función carga las palabras clave desde el archivo binario 'keywords.pkl' y las devuelve como una lista.
    Si ocurre algún error al abrir o leer el archivo, se captura la excepción y se devuelve una lista vacía.
    
    El archivo 'keywords.pkl' debe contener las palabras clave en un formato binario (guardadas previamente con pickle).
    """
    try:
        if not os.path.exists('keywords.pkl'):
            print(f"[{datetime.now()}] Archivo de palabras clave no encontrado.")
            return []
        
        with open('keywords.pkl', 'rb') as file:
            return pickle.load(file)
    except Exception as e:
        print(f"[{datetime.now()}] Error al cargar las palabras clave: {str(e)}")
        return []


# Función para realizar OCR en la captura de pantalla y detectar uso de IA
def detectar_uso_ia_pantalla():
    screenshot_bytes_io, screenshot, timestamp = tomar_captura_pantalla()
    # Extraer texto usando OCR
    text = pytesseract.image_to_string(screenshot)
    
     # Cargar palabras clave desde el archivo binario
    keywords = cargar_keywords()
    
    print(keywords)
    
    # Buscar palabras clave relacionadas con IA
    if any(keyword.lower() in text.lower() for keyword in keywords):
        print(f"[{datetime.now()}] Posible uso de IA detectado en la pantalla: {text[:50]}...")
        txt_data = f"Ordenador: {cliente_id}\nVentana: {ventana_activa_anterior}\nTexto detectado: {text}\n"
        enviar_alerta_servidor(screenshot_bytes_io, txt_data, timestamp)

# Bucle principal para monitorear el cambio de ventana activa
if __name__ == "__main__":
    # Descargar archivo de palabras clave del servidor al iniciar
    descargar_keywords()

    while True:
        try:
            # Obtener la ventana activa actual
            ventana_activa = gw.getActiveWindow()
            nombre_ventana = ventana_activa.title if ventana_activa else "Unknown"

            # Verificar si la ventana activa ha cambiado
            if ventana_activa_anterior != nombre_ventana:
                ventana_activa_anterior = nombre_ventana
                print(f"[{datetime.now()}] Cambio de ventana detectado: {nombre_ventana}")

                # Capturar pantalla y verificar uso de IA mediante OCR
                detectar_uso_ia_pantalla()

            # Esperar un corto intervalo antes de verificar nuevamente
            time.sleep(1)
        except Exception as e:
            print(f"[{datetime.now()}] Error en el monitoreo de ventana activa: {str(e)}")
