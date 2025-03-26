Pruebas y Validación
====================
Se realizaron diferentes pruebas:

- **Pruebas unitarias**: Métodos de lectura/escritura de la base de
  datos, funciones de OCR y detección de ventanas activas.
- **Pruebas de integración**: Comunicación entre el cliente y el
  servidor (envío de capturas).
- **Pruebas de carga**: Múltiples clientes enviando capturas
  simultáneas; se empleó una cola para serializar escrituras en
  SQLite y evitar bloqueos.
- **Pruebas de usabilidad**: Interfaz web revisada con atención a la
  accesibilidad y la claridad de las acciones (activar/desactivar
  capturas, etc.).