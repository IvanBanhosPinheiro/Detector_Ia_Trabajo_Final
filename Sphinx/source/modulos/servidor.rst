Servidor del Detector de IA
===========================

Este módulo implementa el servidor central que gestiona el sistema de detección de IA, 
procesando las alertas de los clientes y proporcionando una interfaz de administración.

Componentes Principales
----------------------

* **Aplicación Flask**: Núcleo del servidor web
* **Sistema de autenticación**: Control de acceso seguro
* **Base de datos**: Almacenamiento persistente de datos
* **Módulos funcionales**:
  * Gestión de palabras clave
  * Procesamiento de capturas
  * Control de horarios
  * Interfaz de administración

Arquitectura del Sistema
----------------------

.. code-block:: text

    ┌────────────────┐      ┌────────────────┐      ┌────────────────┐
    │   Cliente      │      │    Servidor    │      │   Base de      │
    │   (Agente)     │─────>│     Flask      │─────>│    Datos       │
    │                │      │                │      │                │
    └────────────────┘      └───────┬────────┘      └────────────────┘
                                   │
                      ┌────────────┼────────────┐
                      │            │            │
            ┌─────────▼───┐ ┌──────▼─────┐ ┌────▼──────┐
            │  Gestión de │ │ Gestión de │ │ Gestión de│
            │ Palabras    │ │  Capturas  │ │ Horarios  │
            │  Clave      │ │            │ │           │
            └─────────────┘ └────────────┘ └───────────┘

Módulo Principal
--------------

.. automodule:: Servidor.run
   :members:
   :undoc-members:
   :show-inheritance:

Módulos del Servidor
------------------

Modelos de Datos
^^^^^^^^^^^^^^^

.. automodule:: Servidor.models.models
   :members:
   :undoc-members:
   :show-inheritance:

Autenticación
^^^^^^^^^^^^

.. automodule:: Servidor.routes.auth
   :members:
   :undoc-members:
   :show-inheritance:

Gestión de Palabras Clave
^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: Servidor.routes.keywords
   :members:
   :undoc-members:
   :show-inheritance:

Gestión de Capturas
^^^^^^^^^^^^^^^^^

.. automodule:: Servidor.routes.capturas.capturas_control
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: Servidor.routes.capturas.capturas_view
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: Servidor.routes.capturas.capturas_files
   :members:
   :undoc-members:
   :show-inheritance:

Gestión de Horarios
^^^^^^^^^^^^^^^^^

.. automodule:: Servidor.routes.horarios
   :members:
   :undoc-members:
   :show-inheritance:

Proceso en Segundo Plano
^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: Servidor.background_process.horario_checker
   :members:
   :undoc-members:
   :show-inheritance: