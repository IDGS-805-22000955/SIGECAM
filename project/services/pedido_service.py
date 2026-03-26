from project.repositories.pedido_repository import PedidoRepository
from datetime import timedelta

class PedidoService:
    
    @staticmethod
    def obtener_datos_dashboard():
        # Obtener conteos de métricas
        conteos = PedidoRepository.get_conteos_por_estado()
        
        pendientes = conteos.get('Pendiente', 0)
        en_produccion = conteos.get('En Producción', 0)
        completados = conteos.get('Terminado', 0) + conteos.get('Entregado', 0) 
        total_pedidos = PedidoRepository.get_total_pedidos()

        # Obtener el último pedido para mostrar el detalle
        ultimo_pedido_info = PedidoRepository.get_ultimo_pedido()
        
        pedido_actual = None
        productos_pedido = []
        total_calculado = 0.0

        if ultimo_pedido_info:
            p_obj, c_obj = ultimo_pedido_info
            
            # Buscamos los detalles de ese pedido
            detalles = PedidoRepository.get_detalles_completos(p_obj.id_pedido)
            
            for det_obj, pt_obj, mod_obj in detalles:
                # Calculamos el precio por producto (precio_venta * cantidad)
                subtotal = float(pt_obj.precio_venta) * det_obj.cantidad
                total_calculado += subtotal
                
                productos_pedido.append({
                    'nombre': mod_obj.nombre,
                    'talla': float(pt_obj.talla),
                    'cantidad': det_obj.cantidad,
                    'precio': float(pt_obj.precio_venta),
                    'foto': mod_obj.foto_modelo
                })

            #  'fecha_entrega', la simulamos agregando 7 días a la fecha del pedido
            fecha_entrega_estimada = p_obj.fecha_pedido + timedelta(days=7)

            pedido_actual = {
                'id': p_obj.id_pedido,
                'cliente': c_obj.nombre_completo,
                'estado': p_obj.estado_pedido,
                'fecha': p_obj.fecha_pedido.strftime("%d/%m/%Y"),
                'fecha_entrega': fecha_entrega_estimada.strftime("%d/%m/%Y"),
                'total': round(total_calculado, 2)
            }

        return {
            'total_pedidos': total_pedidos,
            'pendientes': pendientes,
            'en_produccion': en_produccion,
            'completados': completados,
            'pedido_actual': pedido_actual,
            'productos_pedido': productos_pedido
        }