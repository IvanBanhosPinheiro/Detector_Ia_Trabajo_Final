Tecnologías Empleadas
=====================
- **Python 3.8+**: Base para el cliente y el servidor.
- **Flask**: Framework web ligero para el backend.
- **Flask-Login**: Gestión de sesiones y autenticación de usuarios.
- **SQLAlchemy** (con **SQLite** por defecto): ORM para la persistencia
  de datos (usuarios, capturas, horarios...).
- **Werkzeug**: Cifrado de contraseñas (hashing) y utilidades de
  seguridad.
- **PyAutoGUI** + **Pillow**: Capturas de pantalla en el cliente.
- **Pytesseract** (Tesseract OCR): Extracción de texto de las imágenes.
- **ConfigParser**: Lectura de ficheros ``.ini`` de configuración (ruta
  de Tesseract, URL del servidor, usuario admin, etc.).
- **Docker** (opcional): Despliegue automatizado del servidor.
- **HTML + CSS + JS**: Interfaz web; las plantillas HTML se generan con
  Jinja2 (integrado con Flask).