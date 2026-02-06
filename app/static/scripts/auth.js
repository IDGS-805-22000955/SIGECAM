document.getElementById('loginForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const submitBtn = this.querySelector('button[type="submit"]');

    submitBtn.disabled = true;
    submitBtn.textContent = 'Validando credenciales...';

    try {
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (response.ok) {
            Swal.fire({
                icon: 'success',
                title: '¡Acceso Correcto!',
                text: 'Redirigiendo...',
                toast: true,
                position: 'top-end',
                showConfirmButton: false,
                timer: 1500,
                timerProgressBar: true
            }).then(() => {

                window.location.href = data.redirect;
            });

        } else {

            Swal.fire({
                icon: 'error',
                title: 'Acceso denegado',
                text: data.message || 'Credenciales incorrectas',
                confirmButtonColor: '#562c2c'
            });
            submitBtn.disabled = false;
            submitBtn.textContent = 'Acceder';
        }

    } catch (error) {
        console.error('Error:', error);
        Swal.fire({
            icon: 'warning',
            title: 'Error de conexión',
            text: 'El servidor no responde',
            confirmButtonColor: '#562c2c'
        });
        submitBtn.disabled = false;
        submitBtn.textContent = 'Acceder';
    }
});