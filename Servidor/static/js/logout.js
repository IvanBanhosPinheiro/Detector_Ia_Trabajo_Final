document.addEventListener('DOMContentLoaded', function() {
    const logoutBtn = document.getElementById('logoutBtn');

    if (logoutBtn) {
        logoutBtn.addEventListener('click', async function(e) {
            e.preventDefault();

            try {
                // Obtener estado actual
                const response = await fetch(captureStatusUrl, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                    }
                });

                if (!response.ok) {
                    throw new Error('Error al obtener estado de capturas');
                }

                const status = await response.json();
                console.log('Estado capturas:', status);

                // Si el usuario actual tiene el control, activar modo automático
                if (!status.modo_automatico && status.current_user_id === status.user_id) {
                    console.log('Activando modo automático...');
                    await fetch(toggleModoUrl, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    });
                }

            } catch (error) {
                console.error('Error:', error);
            } finally {
                window.location.href = logoutUrl;
            }
        });
    }
});