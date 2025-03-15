document.getElementById('toggleCapture').addEventListener('click', function() {
    fetch(toggleCaptureUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (response.ok) {
            location.reload();
        } else {
            throw new Error('Network response was not ok');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error al cambiar estado de capturas');
    });
});