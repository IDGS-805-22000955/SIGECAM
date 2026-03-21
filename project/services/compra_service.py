from project.repositories.compra_repository import CompraRepository

class CompraService:
    
    @staticmethod
    def obtener_datos_dashboard():
        """
        Recopila y formatea todos los datos necesarios para la vista principal
        de Gestión de Compras (tarjetas superiores y detalle de la última compra).
        """
        # 1. Métricas de Hoy
        compras_hoy_list = CompraRepository.get_compras_hoy()
        compras_hoy_count = len(compras_hoy_list)
        gasto_hoy = sum(float(c.total_compra) for c in compras_hoy_list)

        # 2. Métricas Históricas
        totales = CompraRepository.get_totales_historicos()

        # 3. Detalle de la Última Compra
        compra_info, detalles_info = CompraRepository.get_ultima_compra_con_detalles()
        
        compra_actual = None
        materiales_compra = []

        if compra_info:
            c_obj, p_obj, u_obj = compra_info
            
            compra_actual = {
                'id': c_obj.id_compra,
                'proveedor': p_obj.razon_social,
                'fecha': c_obj.fecha_compra.strftime("%d/%m/%Y, %H:%M:%S"),
                'total': float(c_obj.total_compra),
                'registrado_por': u_obj.nombre_usuario
            }
            
            # Formateamos los detalles de la compra
            for det_obj, mp_obj in detalles_info:
                materiales_compra.append({
                    'nombre': mp_obj.nombre,
                    'precio': float(det_obj.costo_unitario),
                    'cantidad': float(det_obj.cantidad),
                    'unidad': mp_obj.unidad_medida,
                    'subtotal': float(det_obj.subtotal)
                })

        # 4. Retornamos el diccionario listo para Jinja
        return {
            'compras_hoy': compras_hoy_count,
            'gasto_hoy': round(gasto_hoy, 2),
            'total_compras': totales['cantidad_compras'],
            'inversion_total': round(totales['inversion_total'], 2),
            'compra_actual': compra_actual,
            'materiales_compra': materiales_compra
        }