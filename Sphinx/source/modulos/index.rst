Módulos del Detector de IA
==========================

Esta sección describe los principales componentes del sistema de detección de IA, explicando su arquitectura, funcionalidades y relaciones entre módulos.

Arquitectura del Sistema
-----------------------

El Detector de IA se compone de dos módulos principales que trabajan en conjunto:

.. code-block:: text

   ┌─────────────────┐                  ┌─────────────────┐
   │     CLIENTE     │                  │     SERVIDOR    │
   │                 │   HTTP/HTTPS     │                 │
   │  • Monitoreo    │◄─────────────────┤  • API REST     │
   │  • Captura      │                  │  • BD SQLite    │
   │  • OCR          │─────────────────►│  • Gestión      │
   │  • Detección    │                  │  • Dashboard    │
   └─────────────────┘                  └─────────────────┘

Descripción de Módulos
---------------------

* **Cliente**: Agente instalado en estaciones de trabajo que monitorea actividad, captura pantallas y detecta posible uso de IA.

* **Servidor**: Sistema centralizado que recibe alertas, almacena datos, proporciona interfaz de administración y controla políticas de detección.

.. toctree::
   :maxdepth: 2
   :caption: Componentes del Sistema:
   
   cliente
   servidor

Interacción entre Módulos
------------------------

El cliente y el servidor se comunican mediante una API REST que permite el intercambio de información en tiempo real, la configuración remota de los agentes y el envío de alertas cuando se detecta posible uso de herramientas de IA.