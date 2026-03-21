from project.extensions import db
from models import Venta, DetalleVenta, ProductoTerminado, Cliente
from sqlalchemy import func
from datetime import date

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
            db.session.rollback() # Si algo falla, se cancela TODO
            raise e

    @staticmethod
    def get_estadisticas_dashboard():
        """Obtiene las métricas para las tarjetas superiores."""
        hoy = date.today()
        
        # Filtramos ventas de hoy
        ventas_hoy_query = db.session.query(Venta).filter(func.date(Venta.fecha_venta) == hoy).all()
        
        ventas_hoy = len(ventas_hoy_query)
        ingresos_hoy = sum([float(v.total_venta) for v in ventas_hoy_query])
        
        # Histórico general
        total_ventas_historico = db.session.query(Venta).count()
        todas_ventas = db.session.query(Venta).all()
        ingresos_totales = sum([float(v.total_venta) for v in todas_ventas])
        
        ticket_promedio = (ingresos_totales / total_ventas_historico) if total_ventas_historico > 0 else 0

        return {
            "ventas_hoy": ventas_hoy,
            "ingresos_hoy": round(ingresos_hoy, 2),
            "total_ventas": total_ventas_historico,
            "ticket_promedio": round(ticket_promedio, 2)
        }

    @staticmethod
    def get_ultima_venta():
        """Obtiene el último registro de venta para mostrar en el ticket."""
        return db.session.query(Venta).order_by(Venta.id_venta.desc()).first()

    @staticmethod
    def get_detalles_venta(id_venta):
        """Obtiene los detalles (productos) de una venta específica."""
        return db.session.query(DetalleVenta).filter_by(id_venta=id_venta).all()