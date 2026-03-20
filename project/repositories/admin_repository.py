from project.extensions import db
from models import Usuario, Proveedor, MateriaPrima, ProductoTerminado
from sqlalchemy import func


class AdminRepository:

    @staticmethod
    def get_dashboard_stats():
        try:
            usuarios_count = Usuario.query.count()
            proveedores_count = Proveedor.query.count()
            productos_count = ProductoTerminado.query.count()

            total_stock_mp = db.session.query(func.sum(MateriaPrima.stock_actual)).scalar() or 0

            return {
                'usuarios': usuarios_count,
                'proveedores': proveedores_count,
                'valor_mp': float(total_stock_mp),
                'productos': productos_count
            }
        except Exception as e:
            print(f"Error Stats: {e}")
            return {'usuarios': 0, 'proveedores': 0, 'valor_mp': 0, 'productos': 0}