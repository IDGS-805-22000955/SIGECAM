from flask import render_template, request, jsonify, session 
from project.modules.ventas import ventas_bp
from project.services.venta_service import VentaService

from project.admin import admin_bp
from project.repositories.admin_repository import AdminRepository

from project.decorators import admin_required

@ventas_bp.route('/')
@admin_required
def index(current_user):

    # Obtener la data procesada del Service
    datos_dashboard = VentaService.obtener_datos_dashboard()
    
    return render_template(
        'admin/ventas/index.html', # <- Asegúrate de que coincida con la ruta de tu archivo html
        user=current_user,
        ventas_hoy=datos_dashboard['stats']['ventas_hoy'],
        ingresos_hoy=datos_dashboard['stats']['ingresos_hoy'],
        total_ventas=datos_dashboard['stats']['total_ventas'],
        ticket_promedio=datos_dashboard['stats']['ticket_promedio'],
        venta_actual=datos_dashboard['venta_actual'],
        productos_venta=datos_dashboard['productos_venta']
    )

@ventas_bp.route('/api/ventas/procesar', methods=['POST'])
# @login_required 
def procesar_venta():
    datos_venta = request.json
    
    # Reemplaza esto con cómo extraes el ID real de la sesión/token de tu app
    id_usuario = session.get('user_id', 1) 
    
    resultado = VentaService.procesar_venta_mostrador(datos_venta, id_usuario)
    
    if resultado['success']:
        return jsonify(resultado), 200
    else:
        return jsonify(resultado), 400