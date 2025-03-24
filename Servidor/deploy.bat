@echo off
REM Construir la imagen de Docker
echo Construyendo la imagen de Docker...
docker build -t serverdetectoria .
if %errorlevel% neq 0 (
    echo Error al construir la imagen.
    exit /b %errorlevel%
)

REM Eliminar contenedor anterior si existe (opcional pero recomendable)
echo Eliminando contenedor anterior si existe...
docker rm -f serverdetectoria >nul 2>&1

REM Ejecutar el contenedor con reinicio automático
echo Ejecutando el contenedor...
docker run -d --restart=always -p 5000:5000 --name serverdetectoria -v mi-bd:/app/instance serverdetectoria
if %errorlevel% neq 0 (
    echo Error al ejecutar el contenedor.
    exit /b %errorlevel%
)

echo Despliegue completado con éxito. El contenedor se reiniciará automáticamente al arrancar Windows si Docker está activo.
pause
