from flask import render_template, request, redirect, url_for, current_app, abort
from functools import wraps
import jwt
from project.modules.pedidos import pedidos_bp
from project.repositories.token_repository import TokenRepository
from project.repositories.admin_repository import AdminRepository
from project.repositories.proveedor_repository import ProveedorRepository
from project.repositories.user_repository import UserRepository
from project.repositories.producto_repository import ProductoRepository
from project.repositories.materia_prima_repository import MateriaPrimaRepository
from project.services.proveedor_service import ProveedorService
from project.services.usuario_service import UsuarioService


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('access_token')
        if not token or TokenRepository.is_blacklisted(token):
            return redirect(url_for('auth.login_page'))

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])

            if data['role'] != 'Admin':
                return abort(403, description="Acceso denegado: Se requieren permisos de Administrador")
            current_user = data
        except Exception:
            return redirect(url_for('auth.login_page'))

        return f(current_user, *args, **kwargs)

    return decorated


# --- DASHBOARD ---
@pedidos_bp.route('/')
@admin_required
def index(current_user):
    stats = AdminRepository.get_dashboard_stats()
    # return render_template('admin/dashboard.html', user=current_user, stats=stats)
    return "Pedidos"

