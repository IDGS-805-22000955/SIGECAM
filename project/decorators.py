from functools import wraps
from flask import request, redirect, url_for, current_app, abort
import jwt
from project.repositories.token_repository import TokenRepository

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('access_token')
        if not token:
            return redirect(url_for('auth.login_page'))

        if TokenRepository.is_blacklisted(token):
            return redirect(url_for('auth.login_page'))

        try:
            jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
        except Exception:
            return redirect(url_for('auth.login_page'))

        return f(*args, **kwargs)

    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('access_token')
        if not token or TokenRepository.is_blacklisted(token):
            return redirect(url_for('auth.login_page'))

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])

            if data.get('role') != 'Admin':
                return abort(403, description="Acceso denegado: Se requieren permisos de Administrador")
            
            current_user = data
        except Exception:
            return redirect(url_for('auth.login_page'))

        return f(current_user, *args, **kwargs)

    return decorated