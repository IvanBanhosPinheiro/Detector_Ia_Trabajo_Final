# Imagen base - Python 3.8.20 versión slim (Debian)
FROM python:3.8.20-slim

# Directorio de trabajo en el contenedor
WORKDIR /app

# Variable de entorno para identificar que estamos en Docker
ENV DOCKER_CONTAINER=1

# Copiar requirements.txt primero para aprovechar la caché de Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . .

# Crear directorio para la base de datos SQLite
# RUN mkdir -p instance

# Puerto que expondrá el contenedor
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["python", "run.py"]