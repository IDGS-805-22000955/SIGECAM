from sqlalchemy import func
from project.extensions import db
from models import Pedido, DetallePedido, Cliente, ProductoTerminado, ModeloZapato

class PedidoRepository:
    
    @staticmethod
    def get_conteos_por_estado():
        """Agrupa y cuenta los pedidos por su estado actual."""
        resultados = db.session.query(
            Pedido.estado_pedido,
            func.count(Pedido.id_pedido)
        ).group_by(Pedido.estado_pedido).all()
        
        # Convertimos la lista de tuplas en un diccionario manejable
        return {estado: conteo for estado, conteo in resultados}

    @staticmethod
    def get_total_pedidos():
        return db.session.query(func.count(Pedido.id_pedido)).scalar() or 0

    @staticmethod
    def get_ultimo_pedido():
        """Obtiene el último pedido y los datos del cliente."""
        return db.session.query(Pedido, Cliente)\
            .join(Cliente, Pedido.id_cliente == Cliente.id_cliente)\
            .order_by(Pedido.fecha_pedido.desc())\
            .first()

    @staticmethod
    def get_detalles_completos(id_pedido):
        """Obtiene los detalles del pedido incluyendo información del modelo y zapato."""
        return db.session.query(DetallePedido, ProductoTerminado, ModeloZapato)\
            .join(ProductoTerminado, DetallePedido.id_pt == ProductoTerminado.id_pt)\
            .join(ModeloZapato, ProductoTerminado.id_modelo == ModeloZapato.id_modelo)\
            .filter(DetallePedido.id_pedido == id_pedido)\
            .all()