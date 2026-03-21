from project.extensions import db
from models import MateriaPrima


class MateriaPrimaRepository:

    @staticmethod
    def get_all():
        return MateriaPrima.query.order_by(MateriaPrima.nombre.asc()).all()

    @staticmethod
    def create(data):
        try:
            nueva_mp = MateriaPrima(
                nombre=data.get('nombre'),
                unidad_medida=data.get('unidad_medida', 'Piezas'),
                porcentaje_merma=data.get('porcentaje_merma', 0.0),
                stock_actual=data.get('stock_actual', 0.0),
                stock_minimo=data.get('stock_minimo', 0.0),
                costo_unitario=data.get('costo_unitario', 0.00)
            )

            db.session.add(nueva_mp)
            db.session.commit()
            return True

        except Exception as e:
            db.session.rollback()
            print(f"Error MP Create: {e}")
            return False