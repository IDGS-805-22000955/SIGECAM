from flask import render_template, request, redirect, url_for, flash, session
from project.modules.compras import compras_bp
from project.services.compra_service import CompraService
from project.decorators import admin_required

# importar repositorios de provedor
from project.repositories.proveedor_repository import ProveedorRepository

@compras_bp.route('/')
@admin_required
def index(current_user):
    
    datos_compras = CompraService.obtener_datos_dashboard()

    return render_template(
        'admin/compras/index.html',
        user=current_user,
        **datos_compras
    )
    
@compras_bp.route('/agregar', methods=['GET'])
@admin_required
def agregar(current_user):
    if 'compra_temporal' not in session:
        session['compra_temporal'] = {
            'proveedor_id': '',
            'fecha': '',
            'notas': '',
            'materiales': []
        }
    proveedores = ProveedorRepository.get_all()
    catalogo_materiales = {"1": "Cuero Premium", "2": "Hilo de Nylon", "3": "Suela de Goma"}
    
    compra_actual = session['compra_temporal']
    lista_materiales = compra_actual.get('materiales', [])
    gran_total = sum(item['cantidad'] * item['precio'] for item in lista_materiales)
    
    return render_template(
        'admin/compras/agregarCompra.html', 
        user=current_user, 
        compra_actual=compra_actual,
        lista_materiales=lista_materiales,
        gran_total=gran_total,
        proveedores=proveedores, 
        catalogo_materiales=catalogo_materiales
    )
    
    
@compras_bp.route('/agregar/material', methods=['POST'])
@admin_required
def agregar_material(current_user):
    _guardar_estado_general(request.form)
    
    catalogo_materiales = {"1": "Cuero Premium", "2": "Hilo de Nylon", "3": "Suela de Goma"}
    
    material_id = request.form.get('nuevo_material_id')
    cantidad = float(request.form.get('nueva_cantidad', 0) or 0)
    precio = float(request.form.get('nuevo_precio', 0) or 0)

    if material_id and cantidad > 0 and precio >= 0:
        nombre = catalogo_materiales.get(material_id, "Desconocido")
        session['compra_temporal']['materiales'].append({
            'material_id': material_id,
            'nombre': nombre,
            'cantidad': cantidad,
            'precio': precio,
            'subtotal': cantidad * precio
        })
        session.modified = True

    return redirect(url_for('compras.agregar'))

@compras_bp.route('/agregar/eliminar_material/<int:index>', methods=['POST'])
@admin_required
def eliminar_material(current_user, index):
    _guardar_estado_general(request.form)
    
    if 0 <= index < len(session['compra_temporal']['materiales']):
        session['compra_temporal']['materiales'].pop(index)
        session.modified = True
        
    return redirect(url_for('compras.agregar'))

@compras_bp.route('/agregar/guardar', methods=['POST'])
@admin_required
def guardar_compra(current_user):
    _guardar_estado_general(request.form)
    compra_data = session.get('compra_temporal')
    
    # validar y guardar en la base de datos:
    # CompraService.crear_compra(compra_data)

    # Una vez guardado, limpiamos la sesión
    session.pop('compra_temporal', None)
    return redirect(url_for('compras.index'))

@compras_bp.route('/agregar/cancelar', methods=['GET'])
@admin_required
def cancelar_compra(current_user):
    """Limpia la sesión si el usuario se arrepiente y cancela."""
    session.pop('compra_temporal', None)
    return redirect(url_for('compras.index'))



def _guardar_estado_general(form):
    if 'compra_temporal' not in session:
        session['compra_temporal'] = {'materiales': []}
        
    session['compra_temporal']['proveedor_id'] = form.get('proveedor_id', '')
    session['compra_temporal']['fecha'] = form.get('fecha', '')
    session['compra_temporal']['notas'] = form.get('notas', '')
    session.modified = True