document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.querySelector('form');
    const submitButton = loginForm?.querySelector('button[type="submit"]');

    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            // Deshabilitar botón y mostrar spinner durante el proceso
            if (submitButton) {
                submitButton.disabled = true;
                submitButton.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Iniciando sesión...';
                
                // Restaurar el botón después de un tiempo máximo
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