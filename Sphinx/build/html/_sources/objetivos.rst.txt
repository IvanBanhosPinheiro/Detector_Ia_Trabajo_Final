Objetivos
=========
- **Objetivo General**: Desarrollar una herramienta capaz de monitorizar
  el uso de inteligencia artificial en ordenadores de aula durante
  exámenes o clases, proporcionando una interfaz de revisión a
  profesores y un panel de administración para el usuario
  administrador.

- **Objetivos Específicos**:
  
  - Implementar un **cliente ligero** que detecte cambios de ventana y
    procese la pantalla en búsqueda de IA.
  - Diseñar un **servidor** que reciba y almacene las capturas,
    asociándolas al profesor correspondiente.
  - Ofrecer un **panel de control** para activar/desactivar la
    monitorización en modo automático o manual.
  - Incorporar un **sistema de gestión de usuarios** (profesores y
    administradores), horarios y palabras clave.
  - Garantizar la **seguridad de credenciales** mediante cifrado
    (password hashing) y un acceso restringido según rol.
  - Facilitar la **instalación y despliegue** mediante Docker o
    entornos virtuales (p. ej., Anaconda), y la configuración a través
    de ficheros ``.ini``.