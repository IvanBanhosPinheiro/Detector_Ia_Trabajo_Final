import os

def get_app_root():
    """Obtiene la ruta raíz de la aplicación"""
    # En Docker, siempre usaremos /app como directorio raíz
    if os.environ.get('DOCKER_CONTAINER'):
        return '/app'
    # Si se ejecuta en desarrollo
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_data_path(filename):
    """
    Obtiene la ruta absoluta de un archivo en el directorio data
    Args:
        filename: Nombre del archivo
    Returns:
        Ruta absoluta al archivo en el directorio data
    """
    return os.path.join(get_app_root(), os.path.join('data', filename)).replace('\\', '/')