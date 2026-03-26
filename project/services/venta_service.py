from models import Venta, DetalleVenta, Kardex, FichaTecnica, Cliente, ProductoTerminado
from project.repositories.venta_repository import VentaRepository, ProductoRepository
from datetime import datetime

class VentaService:
    @staticmethod
    def obtener_datos_dashboard():
        """Prepara todos los datos necesarios para renderizar la vista de Punto de Venta"""
        stats = VentaRepository.get_estadisticas_dashboard()
        ultima_venta = VentaRepository.get_ultima_venta()
        
        venta_actual_data = {}
        productos_venta_data = []
        
        if ultima_venta:
            # Obtener el cliente si existe
            cliente_nombre = "Mostrador"
            if ultima_venta.id_cliente:
                cliente = Cliente.query.get(ultima_venta.id_cliente)
                if cliente:
                    cliente_nombre = cliente.nombre_completo

            # Preparar diccionario de la venta para Jinja
            venta_actual_data = {
                "id": ultima_venta.id_venta,
                "cliente": cliente_nombre,
                "fecha": ultima_venta.fecha_venta.strftime('%d/%m/%Y, %H:%M:%S'),
                "metodo_pago": "Efectivo", # Se puede hacer dinámico posteriormente
                "total": round(float(ultima_venta.total_venta), 2)
            }
            
            # Formatear los productos para el ticket
            detalles = VentaRepository.get_detalles_venta(ultima_venta.id_venta)
            for det in detalles:
                producto = ProductoRepository.get_by_id(det.id_pt)
                # Omitimos relación compleja y creamos un fallback
                nombre_prod = f"Producto ID: {producto.id_pt}" 
                
                productos_venta_data.append({
                    "nombre": nombre_prod,
                    "precio": round(float(det.precio_venta_historico), 2),
                    "cantidad": det.cantidad,
                    "subtotal": round(float(det.subtotal), 2)
                })
                
        return {
            "stats": stats,
            "venta_actual": venta_actual_data,
            "productos_venta": productos_venta_data
        }

    