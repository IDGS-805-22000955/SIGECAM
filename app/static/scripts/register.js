
    document.getElementById('registerForm').addEventListener('submit', async function(e) {
        e.preventDefault();

        const payload = {
            nombre: document.getElementById('nombre').value,
            apellido_paterno: document.getElementById('apellido_paterno').value,
            apellido_materno: document.getElementById('apellido_materno').value,
            email: document.getElementById('email').value,
            password: document.getElementById('password').value,
            pais: 'México'
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
                msgDiv.innerText = data.message;
                msgDiv.classList.remove('d-none');
            }
        } catch (error) {
            console.error(error);
            msgDiv.classList.add('alert-danger');
            msgDiv.innerText = "Error de conexión";
            msgDiv.classList.remove('d-none');
        }
    });
