/**
 * Inicialización del manejo de eventos para botones de borrado.
 * Se ejecuta cuando el DOM está completamente cargado.
 * 
 * @listens DOMContentLoaded
 */
document.addEventListener('DOMContentLoaded', function() {
    // Asignar eventos a todos los botones de borrado
    document.querySelectorAll('.delete-btn').forEach(button => {
        button.addEventListener('click', function() {
            const id = this.getAttribute('data-id');
            confirmarBorrado(id);
        });
    });
});

/**
 * Gestiona el proceso de borrado de una captura.
 * Muestra un diálogo de confirmación y maneja la eliminación.
 * 
 * @param {string} id - ID de la captura a eliminar
 * @returns {void}
 * 
 * @example
 * confirmarBorrado('123');
 */
function confirmarBorrado(id) {
    // Mostrar diálogo de confirmación
    if (confirm('¿Estás seguro de que deseas eliminar esta captura? Esta acción no se puede deshacer.')) {
        // Realizar petición DELETE al servidor
        fetch(deleteUrl.replace('0', id), {
            method: 'DELETE'
        })
        .then(response => {
            if (response.ok) {
                // Eliminar la tarjeta del DOM si existe
                const card = document.querySelector(`[data-captura-id="${id}"]`);
                if (card) {
                    card.remove();
                    // Verificar si quedan capturas, si no, redirigir
                    const grid = document.querySelector('.capture-grid');
                    if (!grid.children.length) {
                        window.location.href = returnUrl;
                    }
                }
            } else {
                // Mostrar error si la eliminación falla
                alert('Error al eliminar la captura');
            }
        })
        .catch(error => {
            // Manejar errores de red o del servidor
            console.error('Error:', error);
            alert('Error al eliminar la captura');
        });
    }
}