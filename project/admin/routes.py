from flask import render_template, request, redirect, url_for, current_app, abort
from functools import wraps
import jwt
from project.admin import admin_bp
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
@admin_bp.route('/dashboard')
@admin_required
def dashboard(current_user):
    stats = AdminRepository.get_dashboard_stats()
    return render_template('admin/dashboard.html', user=current_user, stats=stats)


# --- PROVEEDORES ---
@admin_bp.route('/proveedores')
@admin_required
def proveedores_list(current_user):
    proveedores = ProveedorRepository.get_all()
    return render_template('admin/proveedores/list.html', user=current_user, proveedores=proveedores)


@admin_bp.route('/proveedores/nuevo', methods=['GET', 'POST'])
@admin_required
def proveedores_create(current_user):
    if request.method == 'POST':
        data = request.form.to_dict()
        result = ProveedorService.create_proveedor(data)

        if result['success']:
            return redirect(url_for('admin.proveedores_list'))
        else:
            return f"Error: {result['message']}"

    return render_template('admin/proveedores/create.html', user=current_user)


# --- USUARIOS ---
@admin_bp.route('/usuarios')
@admin_required
def usuarios_list(current_user):
    users = UserRepository.get_all()
    return render_template('admin/usuarios/list.html', user=current_user, users=users)


@admin_bp.route('/usuarios/nuevo', methods=['GET', 'POST'])
@admin_required
def users_create(current_user):
    if request.method == 'POST':
        data = request.form.to_dict()
        result = UsuarioService.create_user(data)

        if result['success']:
            return redirect(url_for('admin.usuarios_list'))
        else:
            return f"Error: {result['message']}"

    return render_template('admin/usuarios/create.html', user=current_user)


@admin_bp.route('/usuarios/editar/<int:user_id>', methods=['GET', 'POST'])
@admin_required
def users_edit(current_user, user_id):
    if request.method == 'POST':
        data = request.form.to_dict()
        result = UsuarioService.update_user(user_id, data)

        if result['success']:
            return redirect(url_for('admin.usuarios_list'))
        else:
            user_to_edit = UserRepository.get_by_id(user_id)
            return render_template('admin/usuarios/edit.html', user=current_user, edit_user=user_to_edit,
                                   error=result['message'])

    user_to_edit = UserRepository.get_by_id(user_id)
    if not user_to_edit:
        return redirect(url_for('admin.usuarios_list'))

    return render_template('admin/usuarios/edit.html', user=current_user, edit_user=user_to_edit)


@admin_bp.route('/usuarios/eliminar/<int:user_id>', methods=['POST'])
@admin_required
def users_delete(current_user, user_id):
    if user_id == current_user['user_id']:
        return "No puedes eliminar tu propia cuenta", 400

    if UsuarioService.delete_user(user_id):
        return redirect(url_for('admin.usuarios_list'))
    else:
        return "Error al eliminar usuario", 500


# --- MATERIALES ---
@admin_bp.route('/materiales')
@admin_required
def materiales_list(current_user):
    materiales = MateriaPrimaRepository.get_all()
    return render_template('admin/materiales/list.html', user=current_user, materiales=materiales)


@admin_bp.route('/materiales/nuevo', methods=['GET', 'POST'])
@admin_required
def materiales_create(current_user):
    if request.method == 'POST':
        data = request.form.to_dict()
        if MateriaPrimaRepository.create(data):
            return redirect(url_for('admin.materiales_list'))
        else:
            return "Error al guardar material"

    proveedores = ProveedorRepository.get_all()
    return render_template('admin/materiales/create.html', user=current_user, proveedores=proveedores)


# --- PRODUCTOS TERMINADOS ---
@admin_bp.route('/productos')
@admin_required
def productos_list(current_user):
    productos = ProductoRepository.get_all()
    return render_template('admin/productos/list.html', user=current_user, productos=productos)


@admin_bp.route('/productos/nuevo', methods=['GET', 'POST'])
@admin_required
def productos_create(current_user):
    if request.method == 'POST':
        data = request.form.to_dict()
        if ProductoRepository.create(data):
            return redirect(url_for('admin.productos_list'))
        else:
            return "Error al guardar producto"

    return render_template('admin/productos/create.html', user=current_user)