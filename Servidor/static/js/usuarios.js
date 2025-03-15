function eliminarUsuario(id, nombre) {
    if (confirm(`¿Estás seguro de que deseas eliminar al usuario "${nombre}"?`)) {
        fetch(deleteUrl.replace('0', id), {
            method: 'DELETE'
        })
        .then(response => {
            if (response.ok) {
                // Buscar y eliminar la fila por ID
                const filas = document.querySelectorAll('tr');
                filas.forEach(fila => {
                    const celdaId = fila.querySelector('td');
                    if (celdaId && celdaId.textContent === id.toString()) {
                        fila.remove();
                    }
                });
                alert('Usuario eliminado correctamente');
            } else {
                response.text().then(text => {
                    alert('Error al eliminar el usuario: ' + text);
                });
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error al eliminar el usuario');
        });
    }
}