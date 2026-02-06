from flask import Blueprint, render_template, request, redirect, url_for, current_app, abort
from functools import wraps
import jwt
from app.repositories.token_repository import TokenRepository
from app.repositories.producto_repository import ProductoRepository
from app.repositories.materia_prima_repository import MateriaPrimaRepository


user_bp = Blueprint('user', __name__)

# DECORADOR DE SEGURIDAD PARA USUARIOS
def user_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('access_token')
        if not token or TokenRepository.is_blacklisted(token):
            return redirect(url_for('auth.login_page'))

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            if data['role'] != 'user':
                if data['role'] == 'admin':
                    return redirect(url_for('admin.dashboard'))
                return abort(403)
            current_user = data
        except Exception:
            return redirect(url_for('auth.login_page'))

        return f(current_user, *args, **kwargs)

    return decorated


#  RUTAS AL DASHBOAR DE USUARIOI
@user_bp.route('/dashboard')
@user_required
def dashboard(current_user):
    return render_template('user/dashboard.html', user=current_user)


#  RUTAS AL PÁGINA DE MATERIALES
@user_bp.route('/materiales')
@user_required
def materiales_list(current_user):
    materiales = MateriaPrimaRepository.get_all()
    return render_template('user/materiales/list.html', user=current_user, materiales=materiales)


#  RUTAS AL PÁGINA DE PRODUCTOS
@user_bp.route('/productos')
@user_required
def productos_list(current_user):
    productos = ProductoRepository.get_all()
    return render_template('user/productos/list.html', user=current_user, productos=productos)