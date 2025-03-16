document.addEventListener('DOMContentLoaded', function() {
    const logoutBtn = document.getElementById('logoutBtn');

    if (logoutBtn) {
        logoutBtn.addEventListener('click', async function(e) {
            e.preventDefault();

            try {
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

                if (status.enabled && status.current_user_id === status.user_id) {
                    console.log('Desactivando capturas...');
                    await fetch(toggleCaptureUrl, {
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