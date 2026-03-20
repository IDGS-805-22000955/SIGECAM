from models import Venta, DetalleVenta, Kardex, FichaTecnica, Cliente
from project.repositories.venta_repository import VentaRepository, ProductoRepository

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
                # Omitimos relación compleja por ahora y creamos un fallback
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

    @staticmethod
    def procesar_venta_mostrador(datos_venta, id_usuario):
        carrito = datos_venta.get('carrito', []) 
        if not carrito:
            return {"success": False, "message": "El carrito está vacío."}

        total_venta = 0
        detalles_a_guardar = []
        kardex_a_guardar = []

        try:
            for item in carrito:
                producto = ProductoRepository.get_by_id(item['id_pt'])
                cantidad_solicitada = int(item['cantidad'])

                if not producto:
                    return {"success": False, "message": "Producto no encontrado."}
                
                if producto.stock_disponible < cantidad_solicitada:
                    return {"success": False, "message": f"Stock insuficiente. Solo hay {producto.stock_disponible} disponibles."}

                costo_produccion_actual = 0
                if producto.ficha_tecnica_rel:
                    costo_produccion_actual = producto.ficha_tecnica_rel.costo_produccion
                
                subtotal = producto.precio_venta * cantidad_solicitada
                total_venta += subtotal

                detalle = DetalleVenta(
                    id_pt=producto.id_pt,
                    cantidad=cantidad_solicitada,
                    precio_venta_historico=producto.precio_venta,
                    costo_produccion_historico=costo_produccion_actual,
                    subtotal=subtotal
                )
                detalles_a_guardar.append(detalle)

                producto.stock_disponible -= cantidad_solicitada

                kardex = Kardex(
                    tipo_movimiento='Salida',
                    id_pt=producto.id_pt,
                    cantidad=cantidad_solicitada,
                    id_usuario=id_usuario
                )
                kardex_a_guardar.append(kardex)

            nueva_venta = Venta(
                id_usuario=id_usuario,
                id_cliente=datos_venta.get('id_cliente'), 
                total_venta=total_venta,
                origen_venta='Mostrador'
            )

            VentaRepository.guardar_venta_completa(nueva_venta, detalles_a_guardar, kardex_a_guardar)

            return {"success": True, "id_venta": nueva_venta.id_venta}

        except Exception as e:
            return {"success": False, "message": f"Error interno: {str(e)}"}