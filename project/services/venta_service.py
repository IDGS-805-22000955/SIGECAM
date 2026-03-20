from models import Venta, DetalleVenta, Kardex, FichaTecnica
from project.repositories.venta_repository import VentaRepository
from project.repositories.producto_repository import ProductoRepository

class VentaService:
    @staticmethod
    def procesar_venta_mostrador(datos_venta, id_usuario):
        carrito = datos_venta.get('carrito', []) # Lista de productos a comprar
        if not carrito:
            return {"success": False, "message": "El carrito está vacío."}

        total_venta = 0
        detalles_a_guardar = []
        kardex_a_guardar = []

        try:
            # 1. Validar productos y stock
            for item in carrito:
                producto = ProductoRepository.get_by_id(item['id_pt'])
                cantidad_solicitada = int(item['cantidad'])

                if not producto:
                    return {"success": False, "message": "Producto no encontrado."}
                
                if producto.stock_disponible < cantidad_solicitada:
                    return {"success": False, "message": f"Stock insuficiente. Solo hay {producto.stock_disponible} disponibles."}

                # 2. Calcular costos históricos
                costo_produccion_actual = 0
                if producto.ficha_tecnica_rel:
                    costo_produccion_actual = producto.ficha_tecnica_rel.costo_produccion
                
                subtotal = producto.precio_venta * cantidad_solicitada
                total_venta += subtotal

                # 3. Preparar Detalle de Venta (usando el precio real de la BD, no el del frontend)
                detalle = DetalleVenta(
                    id_pt=producto.id_pt,
                    cantidad=cantidad_solicitada,
                    precio_venta_historico=producto.precio_venta,
                    costo_produccion_historico=costo_produccion_actual,
                    subtotal=subtotal
                )
                detalles_a_guardar.append(detalle)

                # 4. Descontar Inventario (Regla del PDF)
                producto.stock_disponible -= cantidad_solicitada

                # 5. Preparar registro en Kardex
                kardex = Kardex(
                    tipo_movimiento='Salida',
                    id_pt=producto.id_pt,
                    cantidad=cantidad_solicitada,
                    id_usuario=id_usuario
                )
                kardex_a_guardar.append(kardex)

            # 6. Crear la cabecera de la Venta
            nueva_venta = Venta(
                id_usuario=id_usuario,
                id_cliente=datos_venta.get('id_cliente'), # Puede ser nulo
                total_venta=total_venta,
                origen_venta='Mostrador'
            )

            # 7. Mandar al repositorio para guardar todo junto
            VentaRepository.guardar_venta_completa(nueva_venta, detalles_a_guardar, kardex_a_guardar)

            return {"success": True, "id_venta": nueva_venta.id_venta}

        except Exception as e:
            return {"success": False, "message": f"Error interno: {str(e)}"}