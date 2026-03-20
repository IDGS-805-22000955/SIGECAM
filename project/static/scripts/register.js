document.getElementById('registerForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const payload = {
        nombre_usuario: document.getElementById('nombre_usuario').value,
        password: document.getElementById('password').value
    };

    const msgDiv = document.getElementById('msg');
    msgDiv.classList.add('d-none');
    msgDiv.classList.remove('alert-success', 'alert-danger');

    try {
        const res = await fetch('/api/register', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(payload)
        });
        const data = await res.json();

        if (res.ok) {
            msgDiv.classList.add('alert-success');
            msgDiv.innerText = "¡Registro completado! Redirigiendo...";
            msgDiv.classList.remove('d-none');
            setTimeout(() => window.location.href = '/', 2000); 
        } else {
            msgDiv.classList.add('alert-danger');
            msgDiv.innerText = data.message || "Error al registrar";
            msgDiv.classList.remove('d-none');
        }
    } catch (error) {
        console.error(error);
        msgDiv.classList.add('alert-danger');
        msgDiv.innerText = "Error de conexión";
        msgDiv.classList.remove('d-none');
    }
});