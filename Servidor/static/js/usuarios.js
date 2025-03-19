/**
 * Gestión de usuarios del sistema.
 * Maneja la eliminación de usuarios y cambio de contraseñas.
 * 
 * @module usuarios
 */

/**
 * Elimina un usuario del sistema previa confirmación.
 * 
 * @param {string} id - ID del usuario a eliminar
 * @param {string} nombre - Nombre del usuario para mostrar en la confirmación
 * @fires showNotification
 * @fires fetch
 * 
 * @example
 * eliminarUsuario('123', 'Juan Pérez');
 */
function eliminarUsuario(id, nombre) {
    if (confirm(`¿Estás seguro de que deseas eliminar al usuario "${nombre}"?`)) {
        fetch(deleteUrl.replace('0', id), {
            method: 'DELETE'
        })
        .then(response => {
            if (response.ok) {
                // Eliminar la fila de la tabla
                const fila = document.querySelector(`tr[data-user-id="${id}"]`);
                if (fila) {
                    fila.remove();
                }
                showNotification('Usuario eliminado correctamente', 'success');
            } else {
                return response.text().then(text => {
                    throw new Error(text);
                });
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('Error al eliminar el usuario: ' + error.message, 'danger');
        });
    }
}


/**
 * Prepara y muestra el modal para cambiar la contraseña de un usuario.
 * 
 * @param {string} userId - ID del usuario a modificar
 * @param {string} userName - Nombre del usuario para mostrar en el modal
 * @fires bootstrap.Modal
 * 
 * @example
 * cambiarPassword('123', 'Juan Pérez');
 */
function cambiarPassword(userId, userName) {
    // Resetear el formulario antes de mostrar el modal
    const form = document.getElementById('passwordForm');
    form.reset();
    
    // Actualizar los campos del modal
    document.getElementById('userId').value = userId;
    document.getElementById('userName').textContent = userName;
    
    // Mostrar el modal
    const modal = new bootstrap.Modal(document.getElementById('passwordModal'));
    modal.show();
}

/**
 * Manejador para el formulario de cambio de contraseña.
 * Valida y procesa el cambio de contraseña.
 * 
 * @listens click
 * @fires showNotification
 * @fires fetch
 * @async
 */
document.getElementById('savePassword')?.addEventListener('click', async function() {
    const userId = document.getElementById('userId').value;
    const newPassword = document.getElementById('newPassword').value;
    const confirmPassword = document.getElementById('confirmPassword').value;

    // Validaciones
    if (!newPassword || !confirmPassword) {
        showNotification('Todos los campos son obligatorios', 'danger');
        return;
    }

    if (newPassword !== confirmPassword) {
        showNotification('Las contraseñas no coinciden', 'danger');
        return;
    }

    try {
        const response = await fetch(changePasswordUrl.replace('0', userId), {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                new_password: newPassword
            })
        });

        const data = await response.json();

        if (response.ok) {
            showNotification(data.message || 'Contraseña actualizada correctamente', 'success');
            const modal = bootstrap.Modal.getInstance(document.getElementById('passwordModal'));
            modal.hide();
        } else {
            throw new Error(data.error || 'Error al cambiar la contraseña');
        }
    } catch (error) {
        console.error('Error:', error);
        showNotification(error.message, 'danger');
    }
});