Arquitectura y Funcionamiento
=============================
El sistema se compone de:

- **Cliente**:
  - Monitoriza la ventana activa (ej. cada segundo).
  - Captura la pantalla (PyAutoGUI).
  - Extrae texto (Pytesseract).
  - Si encuentra coincidencias con las *keywords*, envía la imagen y el
    texto al servidor vía HTTP POST.
  - El modo de captura puede ser "manual" (el profesor decide encender
    o apagar) o "automático" (basado en horarios).

- **Servidor**:
  - Recibe las peticiones (``/uploads``, etc.).
  - Almacena la imagen y el texto en la base de datos (tabla
    ``datos``).
  - Asocia la captura a un ``usuario`` (profesor) y a un ``equipo``.
  - Ofrece paneles de gestión:
    - *Panel Control*: estado de capturas, modo manual/automático.
    - *Usuarios*: alta, baja y cambio de contraseñas.
    - *Horarios*: definir periodos para la captura automática.
    - *Keywords*: edición de las palabras clave.

Modos de Captura
----------------
- **Automático**:
  - Se comprueban los *horarios* asociados al usuario. Si la hora
    actual entra en un horario válido, el servidor activa la
    recepción de capturas.
- **Manual**:
  - El profesor, desde el panel, puede pinchar en “Activar/Desactivar
    capturas”.
  - El servidor habilita o no la recepción de capturas según ese
    botón.

Flujo de Trabajo
----------------
1. **Inicio**:
   - El profesor inicia sesión en ``http://<servidor>:5000``.
   - Puede ver su *panel de control*, cambiar modo a manual o
     automático.
2. **Capturas**:
   - El cliente está corriendo en cada PC de alumnos, monitorea
     ventanas.
   - Si detecta palabra clave, sube la captura al servidor.
3. **Almacenamiento**:
   - El servidor guarda la información en la base de datos (fecha,
     imagen, texto).
4. **Revisión**:
   - El profesor entra a ver sus equipos y las capturas agrupadas por
     fecha/hora.
   - Puede descargar la imagen, el texto o eliminarla.