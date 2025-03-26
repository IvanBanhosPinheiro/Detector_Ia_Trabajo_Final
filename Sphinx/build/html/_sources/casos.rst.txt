==============================
Casos de Uso
==============================

.. list-table::
   :widths: 20 80
   :header-rows: 0

   * - **Identificador y Nombre:**
     - CU-Usuario (Uso general del sistema por parte de usuarios)
   * - **Descripción:**
     - El usuario accede al sistema mediante la interfaz web y realiza acciones
       según su rol (profesor o administrador), gestionando información a
       través de distintas pantallas (panel de control, gestión de usuarios,
       horarios, capturas, etc.).
   * - **Actores:**
     - Usuario (Profesor / Administrador)
   * - **Precondiciones:**
     - | El usuario debe existir en la base de datos.
       | El servidor debe estar en ejecución.
   * - **Postcondiciones:**
     - El usuario accede a las opciones de su rol (profesor/administrador).
   * - **Secuencia Normal:**
     - | 1. El usuario navega a la URL del sistema.
       | 2. El sistema muestra la página de login.
       | 3. El usuario ingresa credenciales (nombre y contraseña).
       | 4. El sistema valida las credenciales.
       | 5. Si son correctas, redirige al panel correspondiente (profesor o admin).
       | 6. El usuario realiza las acciones disponibles según su rol (ver capturas,
       |    gestionar usuarios, etc.).
       | 7. Finalmente, el usuario cierra sesión y el sistema regresa a la
       |    pantalla de inicio.
   * - **Excepciones:**
     - | (p1) Usuario/contraseña incorrectos: se muestra un error y no se permite
       |      el acceso.
       | (p2) Se intenta acceder a funciones administrativas con un rol profesor:
       |      el sistema niega el acceso.
   * - **Rendimiento:**
     - Respuesta en menos de 2 segundos en condiciones normales.
   * - **Frecuencia de Uso:**
     - Diario, especialmente en horario de clases o exámenes.
   * - **Importancia:**
     - Alta, pues este caso refleja la operación principal del sistema.
   * - **Urgencia:**
     - Inmediata, ya que es la vía de acceso de profesores y administradores.
   * - **Comentarios:**
     - Se requiere controlar cuidadosamente la seguridad, protegiendo las
       funcionalidades críticas para el rol administrador.

.. list-table::
   :widths: 20 80
   :header-rows: 0

   * - **Identificador y Nombre:**
     - CU-Cliente (Comportamiento del cliente en el sistema)
   * - **Descripción:**
     - El cliente, ejecutado en segundo plano en el equipo del alumno, monitoriza
       la ventana activa y, cuando detecta coincidencias con palabras clave
       (referentes a uso de IA), realiza una captura de pantalla y la envía al
       servidor.
   * - **Actores:**
     - Cliente (software instalado en los equipos de los alumnos)
   * - **Precondiciones:**
     - | Archivo de configuración (config.ini) con la ruta a Tesseract y la URL
       | del servidor.
       | El servidor debe estar disponible para recibir las capturas.
   * - **Postcondiciones:**
     - Se generan y envían capturas al servidor si se detectan coincidencias.
   * - **Secuencia Normal:**
     - | 1. Al arrancar, el cliente lee su configuración (ruta Tesseract, servidor).
       | 2. Periódicamente detecta la ventana activa y efectúa una captura.
       | 3. Aplica OCR para extraer texto.
       | 4. Compara el texto con las palabras clave descargadas del servidor.
       | 5. Si coincide, envía la captura y el texto al servidor vía HTTP POST.
       | 6. El servidor responde con éxito y el cliente continúa monitoreando.
   * - **Excepciones:**
     - | (p1) Sin conexión al servidor: el cliente guarda la captura localmente e
       |      intenta reenviarla más adelante.
       | (p2) Configuración incorrecta (ruta Tesseract o servidor): el cliente
       |      registra error y no procesa capturas.
   * - **Rendimiento:**
     - El OCR y el envío deben ejecutarse en pocos segundos para no ralentizar
       el equipo.
   * - **Frecuencia de Uso:**
     - Frecuente, pudiendo capturar cada X segundos y enviar al servidor al
       detectar coincidencias.
   * - **Importancia:**
     - Crítica, pues sin el cliente no se recaban evidencias de uso de IA.
   * - **Urgencia:**
     - Inmediata, ya que es la funcionalidad primordial para alimentar el
       servidor con datos.
   * - **Comentarios:**
     - La política de notificación al usuario depende de la normativa; puede
       mostrarse o no un aviso de monitorización en segundo plano.