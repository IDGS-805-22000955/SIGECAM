from flask import render_template, request, jsonify, make_response, redirect, url_for, current_app, Blueprint
import jwt
import time
from app.services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__)

# RUTA A PÁGINA  DE LOGIN
@auth_bp.route('/')
def login_page():
    token = request.cookies.get('access_token')
    if token:
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])

            if data.get('role') == 'admin':
                return redirect(url_for('admin.dashboard'))
            elif data.get('role') == 'user':
                return redirect(url_for('user.dashboard'))

        except Exception:
            pass

    return render_template('auth/login.html')


# RUTA A PROCESAR LOGIN
@auth_bp.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    time.sleep(3)

    result = AuthService.login_user(data.get('email'), data.get('password'))

    if result['success']:
        if result.get('role') == 'admin':
            target_url = url_for('admin.dashboard')
        else:
            target_url = url_for('user.dashboard')

        resp = make_response(jsonify({'redirect': target_url}))
        resp.set_cookie('access_token', result['token'], httponly=True)
        return resp, 200

    return jsonify({'message': result['message']}), 401


# RUTA A PÁGINA REGISTRO DE CLIENTE
@auth_bp.route('/register')
def register_page():
    return render_template('auth/register.html')


# RUTA A PROCESAR REGISTRO DE CLIENTE
@auth_bp.route('/api/register', methods=['POST'])
def api_register():
    data = request.get_json()

    required_fields = ['email', 'password', 'nombre', 'apellido_paterno']
    if not all(k in data for k in required_fields):
        return jsonify({'message': 'Faltan datos obligatorios'}), 400

    result = AuthService.register_user(data)

    if result['success']:
        return jsonify({'message': 'Cuenta creada exitosamente'}), 201
    return jsonify({'message': result['message']}), 409


# RUTA A CERRAR SESIÓN
@auth_bp.route('/api/logout', methods=['POST'])
def api_logout():
    time.sleep(3)

    token = request.cookies.get('access_token')
    if token:
        try:
            AuthService.logout_user(token)
        except Exception as e:
            print(f"Error al blacklist token: {e}")

    resp = make_response(jsonify({'redirect': url_for('auth.login_page')}))
    resp.set_cookie('access_token', '', expires=0)
    return resp, 200