from flask import render_template
from project.modules.pedidos import pedidos_bp
from project.services.pedido_service import PedidoService
from project.decorators import admin_required

@pedidos_bp.route('/')
@admin_required
def index(current_user):
    
    # Obtenemos todos los datos procesados
    datos_pedidos = PedidoService.obtener_datos_dashboard()

    return render_template(
        'admin/pedidos/index.html',
        user=current_user,
        **datos_pedidos
    )