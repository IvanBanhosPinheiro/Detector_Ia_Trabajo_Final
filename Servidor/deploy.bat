@echo off
REM Construir la imagen de Docker
echo Construyendo la imagen de Docker...
docker build -t serverdetectoria .
if %errorlevel% neq 0 (
    echo Error al construir la imagen.
    exit /b %errorlevel%
)

REM Ejecutar el contenedor
echo Ejecutando el contenedor...
docker run -d -p 5000:5000 --name serverdetectoria -v mi-bd:/app/instance serverdetectoria
if %errorlevel% neq 0 (
    echo Error al ejecutar el contenedor.
    exit /b %errorlevel%
)

echo Despliegue completado con éxito.
pause
