Instalación y Configuración
===========================
A continuación se describen los pasos más relevantes para poner en
marcha el servidor y el cliente. Existen dos vías principales para el
servidor:

1. **Ejecución con Docker**
2. **Ejecución local** (sin Docker, con Python directamente)

Requisitos Mínimos
------------------
- **Servidor**:
  - Python 3.8+ (si no usas Docker).
  - Recomendable 8 GB RAM y ~50 GB de disco libre.
  - SO: Windows 10/11, o Linux.
  - Docker (opcional).

- **Cliente**:
  - Windows 10/11.
  - Python 3.8+ (si se compila desde fuente) o instalador EXE.
  - Tesseract OCR instalado (o incluido dentro del instalador).
  - 4 GB RAM recomendados.

Servidor: Opción Docker
-----------------------
#. **Editar** ``data/config.ini`` con:
   
   - ``[Servidor]``
   - usuario = "admin"
   - password = "adminpass"
   - puerto = 5000
   
   Al arrancar por primera vez, se creará un **usuario administrador**
   con esas credenciales.

#. **Ejecutar** en consola el script ``deploy.bat`` para:
   
   - Construir la imagen Docker.
   - Levantar el contenedor con Flask en el puerto 5000.
   - Montar un volumen para la base de datos (``instance/database.db``).

#. **Verificar** en el navegador:  
   ``http://localhost:5000``  
   Debería mostrar la página de login; credenciales: *admin/adminpass*.

Servidor: Opción Local
----------------------
1. **Clonar** o descargar el proyecto.
2. (Opcional) Crear un **entorno virtual** con Python >= 3.8.
3. Instalar dependencias:

   .. code-block:: bash

      pip install -r requirements.txt

4. Editar ``data/config.ini`` con las credenciales deseadas para el
   primer admin.

5. Lanzar la aplicación:

   .. code-block:: bash

      python run.py

6. Acceder en el navegador a
   ``http://127.0.0.1:5000`` (o la IP/puerto configurado).

Cliente: Instalador
-------------------
Si se dispone de un **instalador** (ej. ``IaDetectorCliente.exe``), se
puede:

1. Ejecutar el instalador en el equipo cliente.
2. Localizar y editar el ``config.ini`` que genera:
   - ``[Cliente]``
   - ruta = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe" (por ejemplo)
   - servidor = "http://192.168.0.10:5000" (IP o dominio del servidor)
3. Verificar que, al ejecutarse, se active el bucle de detección
   (monitorizar ventanas y enviar capturas cuando se encuentre una
   palabra clave).

Cliente: Ejecución desde Código Fuente
--------------------------------------
1. Clonar o descargar la carpeta del **cliente**.
2. Instalar librerías requeridas:

   .. code-block:: bash

      pip install -r requirements.txt

3. Editar ``config.ini`` con la ruta de Tesseract (apartado ``[Cliente]``)
   y la IP del servidor.

4. Iniciar con:

   .. code-block:: bash

      python cliente.py

5. El cliente descargará las **keywords** iniciales y comenzará a
   detectar ventanas activas, capturando la pantalla si halla
   coincidencias.