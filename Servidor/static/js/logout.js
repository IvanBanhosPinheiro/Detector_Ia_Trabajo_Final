document.addEventListener('DOMContentLoaded', function() {
    const logoutBtn = document.getElementById('logoutBtn');

    if (logoutBtn) {
        logoutBtn.addEventListener('click', async function(e) {
            e.preventDefault();

            try {
                // Obtener estado actual
                const response = await fetch(captureStatusUrl);
                
                if (!response.ok) {
                    throw new Error('Error al obtener estado de capturas');
                }

                const status = await response.json();
                console.log('Estado capturas:', status);

                // Activar modo automático si no está activado
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
                // Siempre redirigir al logout
                window.location.href = logoutUrl;
            }
        });
    }
});