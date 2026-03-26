from flask import render_template
from project.modules.shop import shop_bp
from project.services.pedido_service import PedidoService
from project.decorators import admin_required

@shop_bp.route('/')
def index():
    return render_template(
        'shop/index.html'
    )