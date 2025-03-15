document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.delete-btn').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const fecha = this.getAttribute('data-fecha');
            
            if (confirm(`¿Estás seguro de que deseas eliminar todas las capturas del ${fecha}?\nEsta acción no se puede deshacer.`)) {
                fetch(`{{ url_for('capturas_files.eliminar_fecha', equipo_id=equipo_id, fecha='') }}${fecha}`, {
                    method: 'DELETE'
                })
                .then(response => {
                    if (response.ok) {
                        const item = this.closest('.date-item');
                        item.remove();
                        
                        // Verificar si quedan carpetas
                        const grid = document.querySelector('.date-grid');
                        if (!grid.children.length) {
                            const cardBody = document.querySelector('.card-body');
                            cardBody.innerHTML = '<p class="text-muted">No hay capturas disponibles para este equipo.</p>';
                        }
                        
                        alert('Carpeta eliminada correctamente');
                    } else {
                        throw new Error('Error al eliminar la carpeta');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('Error al eliminar la carpeta');
                });
            }
        });
    });
});