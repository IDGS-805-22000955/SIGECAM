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

    @staticmethod
    def update(id_mp, data):
        try:
            mp = MateriaPrima.query.get(id_mp)
            if not mp:
                return False
            mp.nombre = data.get('nombre')
            mp.unidad_medida = data.get('unidad_medida')
            mp.porcentaje_merma = data.get('porcentaje_merma', 0.0)
            mp.stock_actual = data.get('stock_actual', 0.0)
            mp.stock_minimo = data.get('stock_minimo', 0.0)
            mp.costo_unitario = data.get('costo_unitario', 0.0)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error MP Update: {e}")
            return False

    @staticmethod
    def delete(id_mp):
        try:
            mp = MateriaPrima.query.get(id_mp)
            if not mp:
                return False
            db.session.delete(mp)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error MP Delete: {e}")
            return False