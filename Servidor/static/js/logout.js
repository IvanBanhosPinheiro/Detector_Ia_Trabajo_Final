/**
 * Gestión del proceso de cierre de sesión.
 * Maneja la activación del modo automático y redirección.
 * 
 * @module logout
 */

/**
 * Inicializa el botón de logout y sus manejadores de eventos.
 * 
 * @listens DOMContentLoaded
 */
document.addEventListener('DOMContentLoaded', function() {
    const logoutBtn = document.getElementById('logoutBtn');

    /**
     * Maneja el proceso de cierre de sesión.
     * Verifica y activa el modo automático si es necesario.
     * 
     * @param {Event} e - Evento del click
     * @listens click
     * @async
     * @fires fetch
     */
    if (logoutBtn) {
        logoutBtn.addEventListener('click', async function(e) {
            e.preventDefault();

            try {
                /**
                 * Obtiene el estado actual del sistema de capturas
                 * @fires fetch
                 */
                const response = await fetch(captureStatusUrl);
                
                if (!response.ok) {
                    throw new Error('Error al obtener estado de capturas');
                }

                const status = await response.json();
                console.log('Estado capturas:', status);

                /**
                 * Activa el modo automático si no está activado
                 * Asegura que el sistema quede en modo automático al cerrar sesión
                 * 
                 * @fires fetch
                 */
                if (!status.modo_automatico) {
                    console.log('Activando modo automático antes de cerrar sesión...');
                    const toggleResponse = await fetch(toggleModoUrl, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    });

                    if (!toggleResponse.ok) {
                        throw new Error('Error al activar modo automático');
                    }
                }

            } catch (error) {
                console.error('Error:', error);
            } finally {
                /**
                 * Redirección al endpoint de logout
                 * Se ejecuta siempre, incluso si hay errores
                 */
                window.location.href = logoutUrl;
            }
        });
    }
});