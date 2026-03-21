from flask import render_template
from project.modules.compras import compras_bp
from project.services.compra_service import CompraService
from project.decorators import admin_required

@compras_bp.route('/')
@admin_required
def index(current_user):
    
    # Obtenemos todos los datos reales procesados por el servicio
    datos_compras = CompraService.obtener_datos_dashboard()

    # Si por alguna razón la BD está vacía (no hay compras), 
    # nuestro layout tiene filtros "default" en Jinja para no romperse,
    # pero aquí le pasamos el diccionario real.
    return render_template(
        'admin/compras/index.html',
        user=current_user,
        **datos_compras
    )