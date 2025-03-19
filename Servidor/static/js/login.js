/**
 * Gestión del formulario de inicio de sesión.
 * Maneja el estado del botón y feedback visual durante el envío.
 * 
 * @module login
 */

/**
 * Inicializa el formulario de login y sus manejadores de eventos.
 * 
 * @listens DOMContentLoaded
 */
document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.querySelector('form');
    const submitButton = loginForm?.querySelector('button[type="submit"]');

    /**
     * Maneja el envío del formulario de login.
     * Proporciona feedback visual durante el proceso.
     * 
     * @param {Event} e - Evento del formulario
     * @listens submit
     * @returns {boolean} - true para permitir el envío normal del formulario
     */
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            // Deshabilitar botón y mostrar spinner durante el proceso
            if (submitButton) {
                submitButton.disabled = true;
                submitButton.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Iniciando sesión...';
                
                /**
                 * Restaura el estado del botón después de un tiempo máximo.
                 * Previene que el botón quede bloqueado si hay problemas.
                 * 
                 * @fires setTimeout
                 */
                setTimeout(() => {
                    submitButton.disabled = false;
                    submitButton.innerHTML = 'Iniciar sesión';
                }, 3000);
            }

            // Permitir que el formulario se envíe normalmente
            return true;
        });
    }
});