/**
 * Gestión de eliminación de capturas por fecha para un equipo específico.
 * Inicializa los manejadores de eventos para los botones de eliminación.
 * 
 * @listens DOMContentLoaded
 */
document.addEventListener('DOMContentLoaded', function() {
    /**
     * Asigna manejadores de eventos a todos los botones de eliminación.
     * Cada botón está asociado a una fecha específica de capturas.
     */
    document.querySelectorAll('.delete-btn').forEach(button => {
        button.addEventListener('click', async function(e) {
            e.preventDefault();
            const fecha = this.getAttribute('data-fecha');
            
            /**
             * Muestra diálogo de confirmación y procesa la eliminación.
             * Si se confirma, elimina todas las capturas de la fecha especificada.
             * 
             * @param {string} fecha - Fecha de las capturas a eliminar
             * @fires fetch
             * @fires alert
             */
            if (confirm(`¿Estás seguro de que deseas eliminar todas las capturas del ${fecha}?\nEsta acción no se puede deshacer.`)) {
                try {
                    const response = await fetch(`{{ url_for('capturas_files.eliminar_fecha', equipo_id=equipo_id, fecha='') }}${fecha}`, {
                        method: 'DELETE'
                    });

                    if (response.ok) {
                        // Eliminar elemento del DOM
                        const item = this.closest('.date-item');
                        item.remove();
                        
                        /**
                         * Verifica si quedan carpetas y actualiza la interfaz.
                         * Si no quedan carpetas, muestra mensaje informativo.
                         */
                        const grid = document.querySelector('.date-grid');
                        if (!grid.children.length) {
                            const cardBody = document.querySelector('.card-body');
                            cardBody.innerHTML = '<p class="text-muted">No hay capturas disponibles para este equipo.</p>';
                        }
                        
                        alert('Carpeta eliminada correctamente');
                    } else {
                        throw new Error('Error al eliminar la carpeta');
                    }
                } catch (error) {
                    console.error('Error:', error);
                    alert('Error al eliminar la carpeta');
                }
            }
        });
    });
});