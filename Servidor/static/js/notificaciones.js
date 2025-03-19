/**
 * Sistema de notificaciones toast.
 * Proporciona feedback visual al usuario mediante notificaciones temporales.
 * 
 * @module notificaciones
 */

/**
 * Muestra una notificación toast con el mensaje y categoría especificados.
 * La notificación se auto-oculta después de 3 segundos.
 * 
 * @param {string} message - Mensaje a mostrar en la notificación
 * @param {string} category - Categoría de la notificación (success, danger, warning, info)
 * @throws {Error} Si no encuentra el contenedor de toasts
 * @fires bootstrap.Toast
 * 
 * @example
 * showNotification('Operación exitosa', 'success');
 * showNotification('Error al procesar', 'danger');
 */
function showNotification(message, category) {
    // Obtener contenedor de toasts
    const toastContainer = document.getElementById('toast-container');
    if (!toastContainer) {
        console.error('No se encontró el contenedor de notificaciones');
        return;
    }
    
    // Crear elemento toast
    const toast = `
        <div class="toast align-items-center text-white bg-${category} border-0" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        </div>
    `;
    
    // Insertar toast en el DOM
    toastContainer.insertAdjacentHTML('beforeend', toast);
    
    // Inicializar y mostrar toast
    const toastElement = toastContainer.lastElementChild;
    const bsToast = new bootstrap.Toast(toastElement, {
        autohide: true,
        delay: 3000
    });
    
    /**
     * Limpiar el toast del DOM cuando se oculte
     * @listens hidden.bs.toast
     */
    toastElement.addEventListener('hidden.bs.toast', () => {
        toastElement.remove();
    });
    
    bsToast.show();
}

// Exportar la función para uso global
window.showNotification = showNotification;