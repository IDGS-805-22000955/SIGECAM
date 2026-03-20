from project.extensions import db
from models import ProductoTerminado


class ProductoRepository:

    @staticmethod
    def get_all():
        return ProductoTerminado.query.order_by(ProductoTerminado.id_pt.desc()).all()

    @staticmethod
    def create(data):
        try:
            nuevo_pt = ProductoTerminado(
                id_modelo=data.get('id_modelo'),
                talla=data.get('talla'),
                precio_venta=data.get('precio_venta'),
                stock_disponible=data.get('stock_disponible', 0)
            )

            db.session.add(nuevo_pt)
            db.session.commit()
            return True

        except Exception as e:
            db.session.rollback()
            print(f"Error Producto Create: {e}")
            return False