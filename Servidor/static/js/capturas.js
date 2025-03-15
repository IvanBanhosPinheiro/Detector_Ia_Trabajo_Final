document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.delete-btn').forEach(button => {
        button.addEventListener('click', function() {
            const id = this.getAttribute('data-id');
            confirmarBorrado(id);
        });
    });
});

function confirmarBorrado(id) {
    if (confirm('¿Estás seguro de que deseas eliminar esta captura? Esta acción no se puede deshacer.')) {
        fetch(deleteUrl.replace('0', id), {
            method: 'DELETE'
        })
        .then(response => {
            if (response.ok) {
                const card = document.querySelector(`[data-captura-id="${id}"]`);
                if (card) {
                    card.remove();
                    const grid = document.querySelector('.capture-grid');
                    if (!grid.children.length) {
                        window.location.href = returnUrl;
                    }
                }
            } else {
                alert('Error al eliminar la captura');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error al eliminar la captura');
        });
    }
}