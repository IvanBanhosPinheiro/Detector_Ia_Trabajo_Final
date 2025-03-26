Cliente del Detector de IA
==========================

Este módulo implementa la aplicación cliente que monitorea la pantalla en busca de uso de IA.

Funcionalidades
--------------

* Monitoreo continuo de la ventana activa
* Captura de pantalla al detectar cambios de ventana
* Procesamiento OCR para extraer texto
* Detección de palabras clave relacionadas con IA
* Envío de alertas al servidor central

Flujo de Funcionamiento
----------------------

.. code-block:: text

    ┌─────────────────┐      ┌────────────────┐      ┌────────────────┐
    │  Monitorización │      │   Detección    │      │     Alerta     │
    │  de actividad   │─────>│   mediante     │─────>│    enviada     │
    │                 │      │      OCR       │      │  al servidor   │
    └─────────────────┘      └────────────────┘      └────────────────┘

Documentación del Código
----------------------

.. automodule:: Cliente.cliente
   :members:
   :undoc-members:
   :show-inheritance: