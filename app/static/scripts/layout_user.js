function logout() {
        Swal.fire({
            title: '¿Cerrar sesión?',
            text: "¿Estás seguro de que quieres salir del sistema?",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#562c2c',
            cancelButtonColor: '#8a897c',
            confirmButtonText: 'Sí, salir',
            cancelButtonText: 'Cancelar',
            background: '#fff',
            customClass: {
                popup: 'animated fadeInDown'
            }
        }).then(async (result) => {
            if (result.isConfirmed) {
                try {
                    Swal.fire({
                        title: 'Cerrando sesión...',
                        text: 'Por favor espere',
                        allowOutsideClick: false,
                        didOpen: () => {
                            Swal.showLoading();
                        }
                    });

                    await fetch('/api/logout', { method: 'POST' });

                    Swal.fire({
                        title: '¡Hasta luego!',
                        text: 'Sesión finalizada correctamente',
                        icon: 'success',
                        timer: 2000,
                        showConfirmButton: false,
                        timerProgressBar: true
                    }).then(() => {
                        window.location.href = '/';
                    });

                } catch (error) {
                    console.error('Error al cerrar sesión:', error);
                    window.location.href = '/';
                }
            }
        });
    }
