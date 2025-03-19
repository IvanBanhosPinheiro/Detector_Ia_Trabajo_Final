"""
Módulo de gestión de rutas absolutas.
Proporciona funciones para obtener rutas absolutas a recursos de la aplicación,
con soporte para entornos de desarrollo y Docker.

Este módulo se encarga de resolver las diferencias de rutas entre sistemas operativos
y entornos de ejecución, garantizando acceso consistente a los archivos.
"""
import os

def get_app_root():
    """
    Obtiene la ruta raíz de la aplicación.
    
    Detecta automáticamente si la aplicación se está ejecutando en un contenedor Docker
    o en un entorno de desarrollo local, y devuelve la ruta raíz correspondiente.
    
    Returns:
        str: Ruta absoluta al directorio raíz de la aplicación
        
    Examples:
        >>> get_app_root()
        '/app'  # En Docker
        'C:/ruta/a/la/app'  # En desarrollo local
    """

    # En Docker, siempre usaremos /app como directorio raíz
    if os.environ.get('DOCKER_CONTAINER'):
        return '/app'
    # Si se ejecuta en desarrollo
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_data_path(filename):
    """
    Obtiene la ruta absoluta de un archivo en el directorio data.
    
    Construye y normaliza la ruta completa al archivo especificado dentro
    del directorio 'data' de la aplicación, con separadores de ruta
    adecuados para cualquier sistema operativo.
    
    Args:
        filename (str): Nombre del archivo o ruta relativa dentro de 'data'
        
    Returns:
        str: Ruta absoluta normalizada al archivo solicitado
        
    Examples:
        >>> get_data_path('config.ini')
        '/app/data/config.ini'
        >>> get_data_path('imagenes/logo.png')
        '/app/data/imagenes/logo.png'
    """
    return os.path.join(get_app_root(), os.path.join('data', filename)).replace('\\', '/')