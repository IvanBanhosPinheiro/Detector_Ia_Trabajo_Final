Conclusiones y Mejoras Futuras
==============================
- **Conclusiones**:
  - El sistema **cumple** con la finalidad de detectar y registrar el
    posible uso de IA, ofreciendo un panel de control sencillo para
    profesores y un panel de administración para gestionar palabras
    clave, horarios y usuarios.
  - La arquitectura modular (Blueprints en Flask + cliente aparte) ha
    facilitado el desarrollo y la escalabilidad.

- **Mejoras Futuras**:
  - Migrar a un motor de base de datos más robusto (PostgreSQL,
    MySQL) en entornos con alta concurrencia.
  - Añadir **WebSockets** para notificaciones en tiempo real.
  - Soportar **HTTPS** para proteger el tráfico de imágenes y credenciales.
  - Ampliar la gestión de logs o crear un sistema avanzado de
    auditoría.
  - Integrar una interfaz de estadísticas y gráficos de uso.