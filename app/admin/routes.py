import os
from werkzeug.utils import secure_filename
from flask import render_template, request, redirect, url_for, current_app, abort
from functools import wraps
import jwt
from app.admin import admin_bp
from app.repositories.token_repository import TokenRepository
from app.repositories.admin_repository import AdminRepository
from app.repositories.proveedor_repository import ProveedorRepository
from app.repositories.user_repository import UserRepository
from app.repositories.producto_repository import ProductoRepository
from app.repositories.materia_prima_repository import MateriaPrimaRepository


from app.services.proveedor_service import ProveedorService
from app.services.usuario_service import UsuarioService


# RUTA A LOGIN DE ADMIN
def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('access_token')
        if not token or TokenRepository.is_blacklisted(token):
            return redirect(url_for('auth.login_page'))

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            if data['role'] != 'admin':
                return abort(403, description="Acceso denegado: Se requieren permisos de Administrador")
            current_user = data
        except Exception:
            return redirect(url_for('auth.login_page'))

        return f(current_user, *args, **kwargs)

    return decorated


# RUTA AL DASHBOARD
@admin_bp.route('/dashboard')
@admin_required
def dashboard(current_user):
    stats = AdminRepository.get_dashboard_stats()
    return render_template('admin/dashboard.html', user=current_user, stats=stats)


# RUTA A PROVEEDORES
@admin_bp.route('/proveedores')
@admin_required
def proveedores_list(current_user):
    proveedores = ProveedorRepository.get_all()
    return render_template('admin/proveedores/list.html', user=current_user, proveedores=proveedores)


# RUTA A NUEVO PROVEEDOR
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


# RUTA A USUARIOS
@admin_bp.route('/usuarios')
@admin_required
def usuarios_list(current_user):
    users = UserRepository.get_all_with_persona()
    return render_template('admin/usuarios/list.html', user=current_user, users=users)


# RUTA A NUEVO USUARIO
@admin_bp.route('/usuarios/nuevo', methods=['GET', 'POST'])
@admin_required
def users_create(current_user):
    if request.method == 'POST':
        data = request.form.to_dict()

        file = request.files.get('foto')
        if file and file.filename:
            filename = secure_filename(file.filename)
            save_path = os.path.join(current_app.root_path, 'static/uploads/usuarios', filename)
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            file.save(save_path)

            data['foto'] = filename
        else:
            data['foto'] = None

        result = UsuarioService.create_user(data)

        if result['success']:
            return redirect(url_for('admin.usuarios_list'))
        else:
            return f"Error: {result['message']}"

    return render_template('admin/usuarios/create.html', user=current_user)


# RUTA A EDITAR USUARIO
@admin_bp.route('/usuarios/editar/<int:user_id>', methods=['GET', 'POST'])
@admin_required
def users_edit(current_user, user_id):
    if request.method == 'POST':
        data = request.form.to_dict()

        file = request.files.get('foto')
        if file and file.filename:
            filename = secure_filename(file.filename)
            save_path = os.path.join(current_app.root_path, 'static/uploads/usuarios', filename)
            file.save(save_path)
            data['foto'] = filename

        result = UsuarioService.update_user(user_id, data)

        if result['success']:
            return redirect(url_for('admin.usuarios_list'))
        else:
            user_to_edit = UserRepository.get_full_user_by_id(user_id)
            return render_template('admin/usuarios/edit.html', user=current_user, edit_user=user_to_edit,
                                   error=result['message'])

    user_to_edit = UserRepository.get_full_user_by_id(user_id)
    if not user_to_edit:
        return redirect(url_for('admin.usuarios_list'))

    return render_template('admin/usuarios/edit.html', user=current_user, edit_user=user_to_edit)


# RUTA A ELIMINAR USUARIO
@admin_bp.route('/usuarios/eliminar/<int:user_id>', methods=['POST'])
@admin_required
def users_delete(current_user, user_id):

    if user_id == current_user['user_id']:
        return "No puedes eliminar tu propia cuenta", 400

    if UsuarioService.delete_user(user_id):
        return redirect(url_for('admin.usuarios_list'))
    else:
        return "Error al eliminar usuario", 500


# RUTA A MATERIALES
@admin_bp.route('/materiales')
@admin_required
def materiales_list(current_user):
    materiales = MateriaPrimaRepository.get_all()
    return render_template('admin/materiales/list.html', user=current_user, materiales=materiales)


# RUTA A NUEVO MATERIAL
@admin_bp.route('/materiales/nuevo', methods=['GET', 'POST'])
@admin_required
def materiales_create(current_user):
    if request.method == 'POST':
        data = request.form.to_dict()
        file = request.files.get('foto')

        filename = None
        if file and file.filename:
            filename = secure_filename(file.filename)
            save_path = os.path.join(current_app.root_path, 'static/uploads/materias_primas', filename)
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            file.save(save_path)

        if MateriaPrimaRepository.create(data, filename):
            return redirect(url_for('admin.materiales_list'))
        else:
            return "Error al guardar material"

    proveedores = ProveedorRepository.get_all()
    return render_template('admin/materiales/create.html', user=current_user, proveedores=proveedores)



# RUTA A PRODUCTOS
@admin_bp.route('/productos')
@admin_required
def productos_list(current_user):
    productos = ProductoRepository.get_all()
    return render_template('admin/productos/list.html', user=current_user, productos=productos)


# RUTA A  NUEVO PRODUCTO
@admin_bp.route('/productos/nuevo', methods=['GET', 'POST'])
@admin_required
def productos_create(current_user):
    if request.method == 'POST':
        data = request.form.to_dict()
        file = request.files.get('foto')

        filename = None
        if file and file.filename:
            filename = secure_filename(file.filename)
            save_path = os.path.join(current_app.root_path, 'static/uploads/productos', filename)
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            file.save(save_path)

        if ProductoRepository.create(data, filename):
            return redirect(url_for('admin.productos_list'))
        else:
            return "Error al guardar producto"

    return render_template('admin/productos/create.html', user=current_user)