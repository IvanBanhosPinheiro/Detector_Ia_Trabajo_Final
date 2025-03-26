Estructura de Directorios
=========================
A modo de referencia, una posible estructura (servidor) es la siguiente:

.. code-block:: none

   Servidor
   ├── Dockerfile
   ├── deploy.bat
   ├── requirements.txt
   ├── run.py                  # Punto de arranque de Flask
   ├── models/
   │   └── models.py           # Modelos de datos (SQLAlchemy)
   ├── routes/
   │   └── auth.py                 # Blueprint de autenticación
   │   └── keywords.py             # Blueprint de palabras clave
   │   └── capturas_control.py     # Blueprint de control de capturas
   │   └── capturas_files.py       # Blueprint para descargar/eliminar ficheros
   │   └── capturas_view.py        # Blueprint para visualización de capturas
   │   └──  horarios.py             # Blueprint para gestionar horarios
   │   └── error.py                # Manejo de errores (404, etc.)
   ├── data/
   │   └── config.ini          # Configuración (puerto, admin, etc.)
   ├── instance/
   │   └── database.db         # Creada tras la primera ejecución
   ├── templates/
   │   ├── login.html
   │   ├── panel_control.html
   │   ├── usuarios.html
   │   ├── ...
   └── static/
       ├── css/
       ├── img/
       └── js/

El **cliente** podría disponerse en un repositorio o carpeta aparte:

.. code-block:: none

   Cliente
   ├── cliente.py
   ├── requirements.txt
   ├── config.ini          # Config local (ruta Tesseract, servidor, etc.)
