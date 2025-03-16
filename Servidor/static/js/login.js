document.addEventListener('DOMContentLoaded', function() {
    // Mantener el estilo del body
    const body = document.querySelector('body');
    body.classList.add('text-center');

    // Manejar el formulario de login
    const loginForm = document.querySelector('form');

    if (loginForm) {
        loginForm.addEventListener('submit', async function(e) {
            e.preventDefault();

            try {
                const formData = new FormData(loginForm);
                const response = await fetch(loginForm.action, {
                    method: 'POST',
                    body: formData
                });

                if (response.ok) {
                    // Pequeña pausa antes de redireccionar
                    await new Promise(resolve => setTimeout(resolve, 100));
                    window.location.href = '/dashboard';
                } else {
                    const data = await response.json();
                    showNotification(data.error || 'Error al iniciar sesión', 'danger');
                }
            } catch (error) {
                console.error('Error:', error);
                showNotification('Error al procesar la solicitud', 'danger');
            }
        });
    }
});