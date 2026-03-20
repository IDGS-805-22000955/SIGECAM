from flask import request, jsonify
from project.modules.ventas import ventas_bp
from project.services.venta_service import VentaService


@ventas_bp.route('/')
def index(current_user):
    # stats = AdminRepository.get_dashboard_stats()
    # return render_template('admin/dashboard.html', user=current_user, stats=stats)
    return "Ventas"

@ventas_bp.route('/api/ventas/procesar', methods=['POST'])
# @login_required (Asegúrate de proteger tu ruta)
def procesar_venta(current_user):
    datos_venta = request.json
    
    # Asumimos que tienes el ID del usuario actual en session o JWT
    id_usuario = current_user['user_id'] 
    
    resultado = VentaService.procesar_venta_mostrador(datos_venta, id_usuario)
    
    if resultado['success']:
        return jsonify(resultado), 200
    else:
        return jsonify(resultado), 400