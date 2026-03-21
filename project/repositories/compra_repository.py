from datetime import datetime, date
from sqlalchemy import func
from project.extensions import db
from models import Compra, DetalleCompra, Proveedor, MateriaPrima, Usuario

class CompraRepository:
    
    @staticmethod
    def get_todas_las_compras():
        """Obtiene todas las compras ordenadas de la más reciente a la más antigua."""
        return db.session.query(Compra, Proveedor, Usuario)\
            .join(Proveedor, Compra.id_proveedor == Proveedor.id_proveedor)\
            .join(Usuario, Compra.id_usuario == Usuario.id_usuario)\
            .order_by(Compra.fecha_compra.desc())\
            .all()

    @staticmethod
    def get_compras_hoy():
        """Obtiene las compras realizadas en el día actual."""
        hoy = date.today()
        return db.session.query(Compra)\
            .filter(func.date(Compra.fecha_compra) == hoy)\
            .all()

    @staticmethod
    def get_totales_historicos():
        """Devuelve la cantidad total de compras y la suma total de dinero invertido."""
        resultado = db.session.query(
            func.count(Compra.id_compra).label('cantidad_compras'),
            func.sum(Compra.total_compra).label('inversion_total')
        ).first()
        
        return {
            'cantidad_compras': resultado.cantidad_compras or 0,
            'inversion_total': float(resultado.inversion_total or 0)
        }

    @staticmethod
    def get_ultima_compra_con_detalles():
        """Obtiene la compra más reciente junto con los datos del proveedor y usuario."""
        compra = db.session.query(Compra, Proveedor, Usuario)\
            .join(Proveedor, Compra.id_proveedor == Proveedor.id_proveedor)\
            .join(Usuario, Compra.id_usuario == Usuario.id_usuario)\
            .order_by(Compra.fecha_compra.desc())\
            .first()
            
        if not compra:
            return None, []

        # compra[0] es el objeto Compra
        detalles = db.session.query(DetalleCompra, MateriaPrima)\
            .join(MateriaPrima, DetalleCompra.id_mp == MateriaPrima.id_mp)\
            .filter(DetalleCompra.id_compra == compra[0].id_compra)\
            .all()
            
        return compra, detalles