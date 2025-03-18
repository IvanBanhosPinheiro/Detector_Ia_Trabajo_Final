document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('horarioForm');
    
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const formData = new FormData(form);
        
        try {
            const response = await fetch(form.action, {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            if (response.ok) {
                showNotification('Horario añadido correctamente', 'success');
                location.reload();
            } else {
                showNotification(data.error || 'Error al añadir horario', 'danger');
            }
        } catch (error) {
            console.error('Error:', error);
            showNotification('Error al procesar la solicitud', 'danger');
        }
    });
});

async function eliminarHorario(id) {
    if (confirm('¿Estás seguro de que deseas eliminar este horario?')) {
        try {
            const response = await fetch(eliminarHorarioUrl.replace('0', id), {
                method: 'DELETE'
            });

            if (response.ok) {
                // Eliminar la fila de la tabla
                const button = document.querySelector(`button[data-horario-id="${id}"]`);
                const row = button.closest('tr');
                row.remove();
                
                showNotification('Horario eliminado correctamente', 'success');
            } else {
                const data = await response.json();
                showNotification(data.error || 'Error al eliminar horario', 'danger');
            }
        } catch (error) {
            console.error('Error:', error);
            showNotification('Error al procesar la solicitud', 'danger');
        }
    }
}