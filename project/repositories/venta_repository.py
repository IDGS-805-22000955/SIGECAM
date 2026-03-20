from project.extensions import db
from models import Venta, DetalleVenta, ProductoTerminado

class ProductoRepository:
    @staticmethod
    def get_by_id(id_pt):
        return ProductoTerminado.query.get(id_pt)

class VentaRepository:
    @staticmethod
    def guardar_venta_completa(nueva_venta, detalles, registros_kardex):
        """
        Guarda la venta, sus detalles, actualiza el stock y guarda en Kardex 
        todo en una sola transacción segura.
        """
        try:
            db.session.add(nueva_venta)
            db.session.flush() # Obtenemos el id_venta generado

            for detalle in detalles:
                detalle.id_venta = nueva_venta.id_venta
                db.session.add(detalle)
                
            for kardex in registros_kardex:
                db.session.add(kardex)

            db.session.commit()
            return nueva_venta
        except Exception as e:
            db.session.rollback() # Si algo falla, se cancela TODO (evita datos corruptos)
            raise e