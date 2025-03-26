# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import os
import sys

sys.path.insert(0, os.path.abspath("../../"))
# Añadir específicamente el directorio del servidor
sys.path.insert(0, os.path.abspath('../../Servidor'))
# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Detector de Inteligencia Artificial'
copyright = '2025, Iván Baños Piñeiro'
author = 'Iván Baños Piñeiro'
release = '26/03/2025'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# -- Extensiones de Sphinx --------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',      # Documentación automática desde docstrings
    'sphinx.ext.viewcode',     # Añadir enlaces al código fuente
    'sphinx.ext.napoleon',     # Soporte para formato Google/NumPy docstrings
    'sphinx.ext.intersphinx',  # Enlaces a documentación externa
    'sphinx.ext.mathjax',      # Soporte para ecuaciones matemáticas
    'sphinx.ext.autosummary',  # Resúmenes automáticos de módulos
]

# # Mock objects para dependencias externas
# autodoc_mock_imports = [
#     'flask', 'flask_login', 'werkzeug', 'sqlalchemy', 
#     'pyautogui', 'pytesseract', 'pygetwindow'
# ]
# -- Configuración de autodoc -----------------------------------------------
autodoc_member_order = 'bysource'  # Ordenar miembros como aparecen en el código
add_module_names = False          # No añadir nombres de módulos a las funciones

templates_path = ['_templates']
exclude_patterns = []

language = 'es'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ['_static']
