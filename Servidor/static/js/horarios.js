/**
 * Gestión de horarios de profesores.
 * Maneja la creación y eliminación de horarios.
 * 
 * @module horarios
 */

/**
 * Inicializa el formulario de horarios y sus manejadores de eventos.
 * 
 * @listens DOMContentLoaded
 */
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('horarioForm');
    
    /**
     * Maneja el envío del formulario de horarios.
     * Realiza una petición POST al servidor y muestra notificaciones.
     * 
     * @param {Event} e - Evento del formulario
     * @fires showNotification
     * @listens submit
     */
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const formData = new FormData(form);
        
        try {
            const response = await fetch(form.action, {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            if (response.ok) {
                showNotification('Horario añadido correctamente', 'success');
                location.reload();
            } else {
                showNotification(data.error || 'Error al añadir horario', 'danger');
            }
        } catch (error) {
            console.error('Error:', error);
            showNotification('Error al procesar la solicitud', 'danger');
        }
    });
});

/**
 * Elimina un horario específico.
 * Muestra confirmación, realiza la eliminación y actualiza la interfaz.
 * 
 * @param {string} id - ID del horario a eliminar
 * @fires showNotification
 * @fires confirm
 * @returns {Promise<void>}
 * 
 * @example
 * eliminarHorario('123');
 */
async function eliminarHorario(id) {
    if (confirm('¿Estás seguro de que deseas eliminar este horario?')) {
        try {
            const response = await fetch(eliminarHorarioUrl.replace('0', id), {
                method: 'DELETE'
            });

            if (response.ok) {
                // Eliminar la fila de la tabla
                const button = document.querySelector(`button[data-horario-id="${id}"]`);
                const row = button.closest('tr');
                row.remove();
                
                showNotification('Horario eliminado correctamente', 'success');
            } else {
                const data = await response.json();
                showNotification(data.error || 'Error al eliminar horario', 'danger');
            }
        } catch (error) {
            console.error('Error:', error);
            showNotification('Error al procesar la solicitud', 'danger');
        }
    }
}