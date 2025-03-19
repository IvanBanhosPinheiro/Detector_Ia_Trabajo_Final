# 1. Descripción General

Este proyecto es un **sistema Cliente-Servidor** diseñado para la monitorización y el control de equipos mediante capturas de pantalla y reconocimiento óptico de caracteres (OCR). Se compone de dos aplicaciones escritas en **Python 3.8.20**:

- **Cliente**: Realiza capturas de pantalla en Windows, extrae texto con OCR y detecta la presencia de palabras clave.
- **Servidor**: Recibe y almacena las capturas, permitiendo a los usuarios (profesores/administradores) visualizarlas y gestionar el sistema a través de un panel web.

Además, el repositorio incluye un archivo **`.bat`** (en la carpeta del servidor) que automatiza la construcción y el despliegue en **Docker**, facilitando la instalación y puesta en marcha del servidor en contenedores.

## 2. Principales Características

- **Detección de Palabras Clave**: El cliente realiza OCR en la pantalla (usando Tesseract) y compara el texto con una lista configurable de _keywords_.  
- **Roles de Usuario**:  
  - **Administrador**: Tiene privilegios para gestionar usuarios, configurar las capturas (horarios, activar/desactivar), modificar las palabras clave, etc.  
  - **Profesor**: Puede consultar y administrar únicamente sus capturas, ver el panel de control, descargar/eliminar capturas, etc.  
- **Capturas Automáticas o Manuales**:  
  - **Modo Manual**: El usuario (profesor) decide cuándo activar/desactivar las capturas.  
  - **Modo Automático**: El servidor habilita o deshabilita la recepción de capturas según el horario configurado.  
- **Panel Web**: Interfaz amigable para visualizar las capturas (agrupadas por equipo y fecha), con opción de descargar y eliminar.  
- **Encriptación de Contraseñas**: Uso de _hashing_ seguro (por ejemplo, `generate_password_hash` y `check_password_hash`) para almacenar contraseñas.  
- **Despliegue con Docker**: Mediante un archivo `.bat` en la carpeta del servidor, se automatiza la construcción de la imagen y la ejecución del contenedor Docker.  

## 3. Requisitos y Dependencias

- **Python 3.8.20**  
  Imprescindible para el desarrollo y ejecución del Servidor (y también del Cliente si deseas ejecutarlo desde código fuente en lugar de usar el instalador).

- **Cliente (Instalador)**  
  - Existe un instalador disponible en la sección de **Releases** del repositorio:  
    [Versión 0.1 del Cliente](https://github.com/IvanBanhosPinheiro/Detector_Ia_Trabajo_Final/releases/tag/v0.1)  
  - Tras instalarlo, deberás editar el archivo `config.ini` (que se genera en la ruta de instalación) para:
    - Apuntar a la **ruta de Tesseract** (por ejemplo, `C:\Program Files\Tesseract-OCR\tesseract.exe`).
    - Indicar la **URL** donde corre el Servidor (`http://<IP_o_HOST>:<puerto>`).

- **Tesseract OCR** (sólo en el Cliente)  
  - Necesario para que el Cliente realice el reconocimiento óptico de caracteres.
  - Instálalo y verifica que el `.exe` se ubique en la ruta configurada en `config.ini`.

- **Docker** (opcional, para el Servidor)  
  - El Servidor incluye un **`.bat`** que automatiza la construcción y ejecución de la imagen Docker.
  - Recomendado para un despliegue rápido y aislado.

- **Paquetes de Python (Servidor)**  
  - Al clonar el código fuente del Servidor, asegúrate de instalar las dependencias con:  
    ```bash
    pip install -r requirements.txt
    ```
  - Entre otros, se necesitan: Flask, SQLAlchemy, Flask-Login, etc.

- **Conexión en Red**  
  - El Cliente debe poder conectarse a la IP/puerto donde se ejecute el Servidor.
  - Si usas Docker, comprueba que los puertos estén mapeados correctamente.

### 4.1 Ejecución con Docker (usando el `deploy.bat`)

En la carpeta del Servidor encontrarás un archivo **`deploy.bat`** que automatiza los siguientes pasos:

1. **Construir** la imagen Docker a partir del Dockerfile (si existe) o de la configuración incluida en el proyecto.  
2. **Ejecutar** el contenedor mapeando el puerto correspondiente (generalmente el **5000**) para que puedas acceder al Servidor desde tu navegador o desde el Cliente.

**Para usarlo**:

1. Abre una consola (CMD o PowerShell) en la carpeta del Servidor.  
2. Ejecuta el archivo **`deploy.bat`**:

   ```bash
   ./deploy.bat
   ```
Tras estos pasos, se iniciará el contenedor Docker con tu aplicación Flask, expuesta en la IP del host y el puerto definido en el `deploy.bat` (por defecto [http://localhost:5000](http://localhost:5000)).

> **Nota**: Dependiendo de tu configuración, es posible que necesites privilegios de administrador o asegurarte de que Docker Desktop (o el daemon de Docker) se esté ejecutando antes de lanzar el `deploy.bat`.

### 4.2 Ejecución Local (sin Docker)

Si prefieres no usar contenedores o estás en una etapa de desarrollo, también puedes iniciar el Servidor localmente siguiendo estos pasos:

1. **Clona** este repositorio o descarga el código fuente del Servidor.  
2. **Instala** Python **3.8.20** (si no lo tienes).  
3. **Crea** un entorno virtual (opcional, pero recomendado):  
   ```bash 
   python -m venv venv  
   .\venv\Scripts\activate (Windows)  
   source venv/bin/activate (Linux/Mac)
   ```

4. **Instala** las dependencias:  
   ```bash  
   pip install -r requirements.txt
   ```

5. **Configura** el archivo `config.ini` (si corresponde), indicando:  
   - El **puerto** que usará Flask (por defecto 5000).  
   - Las **credenciales** para crear automáticamente el primer usuario administrador.  
   - Parámetros de la **base de datos** (por defecto se usa SQLite).

6. **Ejecuta** el Servidor:  
   ```bash   
   python run.py
   ```

Tras el arranque, el Servidor quedará **escuchando** las peticiones del Cliente, así como cualquier acceso web al panel de control. Accede desde tu navegador a [http://127.0.0.1:5000](http://127.0.0.1:5000) (o a la IP/puerto configurado).

  

   
