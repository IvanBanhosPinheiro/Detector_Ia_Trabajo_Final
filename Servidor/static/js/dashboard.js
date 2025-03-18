document.addEventListener('DOMContentLoaded', function() {
    const toggleCaptureBtn = document.getElementById('toggleCapture');
    const toggleModoSwitch = document.getElementById('toggleModo');
    const controlManual = document.getElementById('controlManual');

    // Manejar botón de capturas
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

    // Manejar switch de modo automático
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
                
                // Actualizar visibilidad del control manual
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