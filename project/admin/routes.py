from flask import render_template, request, redirect, url_for, current_app, abort, flash
from functools import wraps
import jwt

from models import Cliente
from project.admin import admin_bp
from project.extensions import db
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
    return render_template('admin/materiales/list.html',
                           user=current_user,
                           materiales=materiales)


@admin_bp.route('/materiales/addMaterial', methods=['GET', 'POST'])
@admin_required
def materiales_create(current_user):
    if request.method == 'POST':
        data = request.form.to_dict()
        if MateriaPrimaRepository.create(data):
            return redirect(url_for('admin.materiales_list'))
        else:
            return "Error al guardar material"
    proveedores = ProveedorRepository.get_all()
    return render_template('admin/materiales/create.html',
                           user=current_user,
                           proveedores=proveedores)


@admin_bp.route('/materiales/editMaterial', methods=['POST'])
@admin_required
def materiales_update(current_user):
    data = request.form.to_dict()
    id_mp = data.get('id_mp')

    MateriaPrimaRepository.update(id_mp, data)
    return redirect(url_for('admin.materiales_list'))


@admin_bp.route('/materiales/deleteMaterial', methods=['POST'])
@admin_required
def materiales_delete(current_user):
    id_mp = request.form.get('id_mp')

    MateriaPrimaRepository.delete(id_mp)
    return redirect(url_for('admin.materiales_list'))


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

#---CLIENTES---

@admin_bp.route('/clientes')
def clientes_list():
    clientes = Cliente.query.all()
    return render_template('admin/clientes/list.html', clientes=clientes)

#Agregar nuevo cliente
@admin_bp.route('/clientes/nuevo', methods=['POST'])
def cliente_nuevo():
    # Obtener datos del form
    nombre = request.form.get('nombre_completo')
    email = request.form.get('email')
    telefono = request.form.get('telefono')
    rfc = request.form.get('rfc_datos')
    # Guardar en DB
    nuevo_cliente = Cliente(
        nombre_completo=nombre,
        email=email,
        telefono=telefono,
        rfc_datos=rfc
    )
    try:
        db.session.add(nuevo_cliente)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
    return redirect(url_for('admin.clientes_list'))


# Eliminar cliente
@admin_bp.route('/clientes/eliminar/<int:id>', methods=['POST'])
def cliente_eliminar(id):
    cliente = Cliente.query.get_or_404(id)
    try:
        nombre = cliente.nombre_completo
        db.session.delete(cliente)
        db.session.commit()
        # Mandamos el mensaje de éxito desde Python
        flash(f'Cliente {nombre} eliminado correctamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error al eliminar el cliente', 'error')
    return redirect(url_for('admin.clientes_list'))


# Editar cliente
@admin_bp.route('/clientes/editar/<int:id>', methods=['POST'])
def cliente_editar(id):
    cliente = Cliente.query.get_or_404(id)
    cliente.nombre_completo = request.form.get('nombre_completo')
    cliente.email = request.form.get('email')
    cliente.telefono = request.form.get('telefono')
    cliente.rfc_datos = request.form.get('rfc_datos')

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error al editar: {e}")
    return redirect(url_for('admin.clientes_list'))