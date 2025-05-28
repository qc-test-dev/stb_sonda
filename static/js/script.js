/*Funcion de Detalle Matriz*/
function actualizarColorSelect(select) {
    const valor = select.value;
    select.classList.remove(
        'estado-funciona', 'estado-falla-nueva', 'estado-falla-persistente',
        'estado-na', 'estado-pendiente', 'estado-por-ejecutar'
    );
    switch (valor) {
        case 'funciona':
            select.classList.add('estado-funciona');
            break;
        case 'falla_nueva':
            select.classList.add('estado-falla-nueva');
            break;
        case 'falla_persistente':
            select.classList.add('estado-falla-persistente');
            break;
        case 'na':
            select.classList.add('estado-na');
            break;
        case 'pendiente':
            select.classList.add('estado-pendiente');
            break;
        case 'por_ejecutar':
            select.classList.add('estado-por-ejecutar');
            break;
    }
}

document.querySelectorAll('.estado-select').forEach(function (select) {
    actualizarColorSelect(select);
    select.addEventListener('change', function () {
        actualizarColorSelect(select);
    });
});

function enviarFormulario() {
    const form = document.getElementById('form-casos');
    const formData = new FormData(form);

    fetch(window.location.href, {
        method: 'POST',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
        },
        body: formData,
        credentials: 'same-origin'
    })
    .then(response => {
        if (!response.ok) throw new Error('Error en la petición');
        return response.text();
    })
    .then(data => {
        const mensaje = document.getElementById('mensaje');
        mensaje.classList.remove('d-none', 'alert-danger');
        mensaje.classList.add('alert-success');
        mensaje.textContent = 'Cambios guardados automáticamente.';
        setTimeout(() => mensaje.classList.add('d-none'), 3000);
    })
    .catch(error => {
        const mensaje = document.getElementById('mensaje');
        mensaje.classList.remove('d-none', 'alert-success');
        mensaje.classList.add('alert-danger');
        mensaje.textContent = '❌ Error al guardar automáticamente.';
        console.error(error);
    });
}

document.getElementById('form-casos').addEventListener('submit', function(event){
    event.preventDefault();
    enviarFormulario();
});

// Guardado automático cada 15 segundos (15000 ms)
setInterval(() => {
    enviarFormulario();
}, 15000);

//Funcion sobre ticktes por levantar 
    // Filtrado simple por tester
    document.getElementById('searchTester').addEventListener('input', function () {
        const filter = this.value.toLowerCase();
        const rows = document.querySelectorAll('#ticketsTable tbody tr');
        rows.forEach(row => {
            const testerCell = row.querySelector('td:first-child').textContent.toLowerCase();
            row.style.display = testerCell.includes(filter) ? '' : 'none';
        });
    });