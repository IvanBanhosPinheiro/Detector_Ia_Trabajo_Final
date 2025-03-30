# 1. Descripción General

Este proyecto es un **sistema Cliente-Servidor** diseñado para la monitorización y el control de equipos mediante capturas de pantalla y reconocimiento óptico de caracteres (OCR). Se compone de dos aplicaciones escritas en **Python 3.8.20**:

- **Cliente**: Realiza capturas de pantalla en Windows, extrae texto con OCR y detecta la presencia de palabras clave.
- **Servidor**: Recibe y almacena las capturas, permitiendo a los usuarios (profesores/administradores) visualizarlas y gestionar el sistema a través de un panel web.

Además, el repositorio incluye:
- Un archivo **`deploy.bat`** (en la carpeta del servidor) que automatiza la construcción y el despliegue en **Docker**, facilitando la instalación y puesta en marcha del servidor en contenedores.
- Un documento **`Memoria.pdf`** que contiene toda la documentación necesaria de forma más detallada, incluyendo explicaciones adicionales, diagramas y aspectos técnicos profundos.

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
## 4. Instalación y Configuración del Servidor
### 4.1 Ejecución con Docker (usando el `deploy.bat`)

En la carpeta del Servidor encontrarás un archivo **`deploy.bat`** que automatiza los siguientes pasos:

1. **Construir** la imagen Docker a partir del Dockerfile (si existe) o de la configuración incluida en el proyecto.  
2. **Ejecutar** el contenedor mapeando el puerto correspondiente (generalmente el **5000**) para que puedas acceder al Servidor desde tu navegador o desde el Cliente.
3. **Configurar** el archivo `config.ini` (si lo requieres), indicando:
   - El **puerto** que usará Flask (por defecto 5000).
   - Las **credenciales** para crear automáticamente el primer usuario administrador.
   - Parámetros de la **base de datos** (por defecto se usa SQLite).

   > **Nota sobre la primera cuenta de administrador**:  
   > Al arrancar el servidor por primera vez, la aplicación creará automáticamente un usuario administrador utilizando los credenciales especificados en el archivo `config.ini`.  
   > Esta cuenta será la que podrás usar para acceder inicialmente a la interfaz con privilegios de administrador.

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

   > **Nota sobre la primera cuenta de administrador**:  
   > Al arrancar el servidor por primera vez, la aplicación creará automáticamente un usuario administrador utilizando los credenciales especificados en el archivo `config.ini`.  
   > Esta cuenta será la que podrás usar para acceder inicialmente a la interfaz con privilegios de administrador.


6. **Ejecuta** el Servidor:  
   ```bash   
   python run.py
   ```

Tras el arranque, el Servidor quedará **escuchando** las peticiones del Cliente, así como cualquier acceso web al panel de control. Accede desde tu navegador a [http://127.0.0.1:5000](http://127.0.0.1:5000) (o a la IP/puerto configurado).

## 5. Instalación y Configuración del Cliente

El Cliente es una aplicación de **Python** (versión 3.8.20) que captura la pantalla, realiza OCR y detecta palabras clave. Estas capturas se envían al Servidor siempre y cuando las capturas estén activadas (modo manual o automático).

### 5.1 Usando el Instalador

En la sección de _Releases_ del repositorio encontrarás un **instalador** para el Cliente.  
- Tras la instalación, localiza el archivo `config.ini` que se genera en la carpeta de instalación.  
- Ajusta los siguientes parámetros:
  - `ruta`: la ubicación del ejecutable de Tesseract (por ejemplo, `C:\Program Files\Tesseract-OCR\tesseract.exe`).  
  - `servidor`: la URL del Servidor (por defecto, `http://127.0.0.1:5000` si está en la misma máquina).

Cuando lances el Cliente, se iniciará un bucle que:
1. Monitorea la ventana activa cada cierto intervalo.
2. Captura la pantalla y la procesa con OCR.
3. Busca coincidencias con las palabras clave (descargadas desde el Servidor).
4. Envía la captura y el texto extraído si encuentra alguna palabra clave.

### 5.2 Ejecutando desde Código Fuente

Si prefieres usar el código fuente:
1. **Clona** o descarga el repositorio del Cliente.
2. **Instala** Python 3.8.20 (o la versión compatible).
3. **Crea** un entorno virtual (opcional, recomendado).
4. **Instala** las dependencias:
   ```bash  
   pip install -r requirements.txt
   ```
5. **Configura** el archivo `config.ini` indicando:
   - `ruta`: ruta de Tesseract OCR.
   - `servidor`: dirección del Servidor Flask.
6. **Ejecuta** el archivo principal (p.ej. `cliente.py`):
   ```bash  
   python cliente.py
   ```

Al arrancar, el Cliente descargará automáticamente las palabras clave y empezará a monitorear la pantalla. Cada cambio de ventana activa o cada cierto intervalo (según configuración) generará una captura, que será procesada y enviada al Servidor si contiene coincidencias.

## 6. Uso de la Aplicación Web

El sistema ofrece un **panel web** para el Profesor y el Administrador, accesible en la ruta base del Servidor (por defecto [http://127.0.0.1:5000](http://127.0.0.1:5000)).

### 6.1 Inicio de Sesión

1. Visita la URL principal del Servidor (e.g., `http://127.0.0.1:5000`).
2. Serás redirigido a la pantalla de **login**, donde deberás ingresar tus credenciales (usuario y contraseña).

**Roles disponibles**:

- **Administrador**: Privilegios para gestionar todo el sistema (usuarios, palabras clave, horarios, etc.).
- **Profesor**: Puede visualizar sus capturas, activar/desactivar el modo de captura y ver estadísticas.

### 6.2 Panel de Control (Profesor)

Tras iniciar sesión como Profesor:
1. Accede a **Panel Control** para:
   - Ver el **estado** de las capturas (activadas/desactivadas).
   - Cambiar entre **modo automático** (según horario) y **modo manual**.
   - Activar o desactivar manualmente las capturas (si está en modo manual).
2. Visualiza tus **equipos** y las capturas asociadas:
   - Ordenadas por **fecha**.
   - Permite descargar la imagen o el texto extraído, así como eliminar capturas individuales o masivas.

### 6.3 Panel de Administración

Tras iniciar sesión como Administrador:
1. **Gestión de Usuarios**  
   - Crear nuevos usuarios (profesores).
   - Eliminar usuarios y todas sus capturas.
   - Cambiar la contraseña de cualquier usuario.
2. **Editar Palabras Clave**  
   - Añadir, modificar o eliminar términos que activan las alertas en el Cliente.
3. **Configurar Horarios**  
   - Establecer rangos de tiempo en los que las capturas se activan o desactivan automáticamente para determinados usuarios.
4. **Revisar Capturas**  
   - Al igual que un profesor, el administrador puede acceder a las capturas almacenadas en el sistema (o a las de todos los usuarios, según la implementación).

### 6.4 Cierre de Sesión

Al finalizar, haz clic en “Cerrar Sesión” para volver a la pantalla de login y asegurar que nadie más acceda a tus permisos.

## 7. Posibles Mejoras Futuras

Si bien el proyecto cumple las funcionalidades básicas de monitoreo y envío de capturas, se pueden plantear diversas mejoras y extensiones:

1. **Notificaciones en Tiempo Real**  
   - Implementar un mecanismo de *push notifications* (por ejemplo, WebSockets) para alertar inmediatamente al profesor o al administrador cuando se detecta una palabra clave.

2. **Encriptación de Comunicaciones**  
   - Configurar el servidor Flask para trabajar sobre **HTTPS**, asegurando que las capturas y datos viajen cifrados.

3. **Base de Datos Externa**  
   - Sustituir la base de datos SQLite por una solución en la nube (MySQL, PostgreSQL, etc.) para un entorno productivo y con mayor concurrencia.

4. **Logs y Auditoría**  
   - Registrar en detalle la actividad del sistema (hora de envío de capturas, logs de acceso, etc.) en un archivo o base de datos de auditoría.

5. **Gestión de Permisos Más Detallada**  
   - Ampliar el sistema de roles para contemplar perfiles intermedios o restricciones más finas (por ejemplo, profesores con visibilidad solo de ciertos equipos).

6. **Interfaz de Análisis**  
   - Incluir gráficos o resúmenes estadísticos para que los administradores/profesores vean cuántas capturas se han realizado o cuántas coincidencias con palabras clave ha habido en un periodo de tiempo.

7. **Soporte Multiplataforma para el Cliente**  
   - Adaptar el proceso de captura y OCR para equipos Linux o macOS, ampliando el alcance de la aplicación.

Con estas ideas, el proyecto podría evolucionar hacia un sistema de monitoreo más robusto, seguro y escalable.

## 8. Conclusiones

Este sistema de monitorización Cliente-Servidor demuestra cómo integrar diferentes tecnologías (Flask, PyTesseract, PyAutoGUI, Docker) para lograr un control de uso en equipos remotos:

- **Viabilidad Técnica**: Se logra capturar, procesar y almacenar imágenes de manera eficaz. El uso de OCR y la búsqueda de palabras clave funciona correctamente para los propósitos iniciales.
- **Arquitectura Modular**: Separar la funcionalidad en Blueprints (Flask) y módulos (Cliente) facilita la escalabilidad, el mantenimiento y la comprensión de cada parte del sistema.
- **Seguridad y Roles**: Aunque se ha implementado un esquema básico de roles (administrador y profesor) con contraseñas cifradas, este enfoque podría mejorarse con HTTPS, tokens JWT, etc. según las necesidades de despliegue real.
- **Uso de Docker**: La posibilidad de desplegar el servidor dentro de contenedores simplifica la instalación en distintos entornos. El script `deploy.bat` automatiza la mayor parte del proceso.

En conjunto, el proyecto proporciona una **prueba de concepto funcional** que puede servir como base para implementaciones más robustas y escalables en entornos de monitorización de exámenes, laboratorios o equipos remotos.

---

## Licencia

Este proyecto se distribuye bajo la licencia [Creative Commons Atribución-NoComercial 4.0 Internacional](LICENSE).
Si deseas más detalles, revisa el texto completo en el archivo [LICENSE](./LICENSE) o en 
[la web oficial de Creative Commons](https://creativecommons.org/licenses/by-nc/4.0/legalcode.es).

**Resumen**:
- Eres libre de usar, modificar y compartir el proyecto, siempre que:
  1. Se reconozca la autoría original (BY).
  2. No se utilice con fines comerciales (NC).
 
---

## 10. Contribuciones y Créditos

- Desarrollo realizado como proyecto final de ciclo (DAM/DAW/Multiplataforma).  
- Uso de frameworks y librerías de terceros (Flask, Tesseract, PyAutoGUI, Docker, etc.).  
- Agradecimientos a docentes y colaboradores que apoyaron las pruebas y validación.

Si deseas contribuir con mejoras, PRs o correcciones, por favor crea un **Pull Request** en este repositorio o abre un _issue_ describiendo la propuesta.
