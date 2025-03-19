/**
 * Inicialización y gestión del panel de control.
 * Maneja los controles de captura y modo automático.
 * 
 * @listens DOMContentLoaded
 */
document.addEventListener('DOMContentLoaded', function() {
    const toggleCaptureBtn = document.getElementById('toggleCapture');
    const toggleModoSwitch = document.getElementById('toggleModo');
    const controlManual = document.getElementById('controlManual');

    /**
     * Maneja el botón de activación/desactivación de capturas.
     * Realiza una petición POST al servidor para cambiar el estado.
     * 
     * @listens click
     */
    if (toggleCaptureBtn) {
        toggleCaptureBtn.addEventListener('click', async function() {
            try {
                const response = await fetch(toggleCaptureUrl, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });

                if (!response.ok) {
                    throw new Error('Error al cambiar estado de capturas');
                }

                location.reload();
            } catch (error) {
                console.error('Error:', error);
                showNotification('Error al cambiar estado de capturas', 'danger');
            }
        });
    }

    /**
     * Maneja el switch de modo automático/manual.
     * Realiza una petición POST al servidor y actualiza la interfaz.
     * 
     * @listens change
     * @fires showNotification
     */
    if (toggleModoSwitch) {
        toggleModoSwitch.addEventListener('change', async function() {
            try {
                const response = await fetch(toggleModoUrl, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });

                if (!response.ok) {
                    throw new Error('Error al cambiar modo');
                }

                const data = await response.json();
                
                /**
                 * Actualiza la visibilidad del panel de control manual
                 * basado en el modo seleccionado
                 */
                if (controlManual) {
                    if (data.modo === 'automatico') {
                        controlManual.classList.add('d-none');
                    } else {
                        controlManual.classList.remove('d-none');
                    }
                }

                showNotification(`Modo ${data.modo} activado`, 'success');
                location.reload();
                
            } catch (error) {
                console.error('Error:', error);
                showNotification('Error al cambiar modo', 'danger');
                toggleModoSwitch.checked = !toggleModoSwitch.checked;
            }
        });
    }
});