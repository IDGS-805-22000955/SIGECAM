from flask import Blueprint, render_template, request, redirect, url_for, current_app, abort
from functools import wraps
import jwt
from project.repositories.token_repository import TokenRepository
from project.repositories.producto_repository import ProductoRepository
from project.repositories.materia_prima_repository import MateriaPrimaRepository


user_bp = Blueprint('user', __name__)


# --- DECORADOR DE SEGURIDAD PARA COLABORADORES ---
def user_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('access_token')
        if not token or TokenRepository.is_blacklisted(token):
            return redirect(url_for('auth.login_page'))

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            if data['role'] == 'Admin':
                return redirect(url_for('admin.dashboard'))

            current_user = data
        except Exception:
            return redirect(url_for('auth.login_page'))

        return f(current_user, *args, **kwargs)

    return decorated


# --- RUTAS DEL USUARIO / COLABORADOR ---

@user_bp.route('/dashboard')
@user_required
def dashboard(current_user):
    return render_template('user/dashboard.html', user=current_user)


@user_bp.route('/materiales')
@user_required
def materiales_list(current_user):
    materiales = MateriaPrimaRepository.get_all()
    return render_template('user/materiales/list.html', user=current_user, materiales=materiales)


@user_bp.route('/productos')
@user_required
def productos_list(current_user):
    productos = ProductoRepository.get_all()
    return render_template('user/productos/list.html', user=current_user, productos=productos)