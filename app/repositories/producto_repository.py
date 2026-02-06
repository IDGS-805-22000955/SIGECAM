from app.extensions import get_db


class ProductoRepository:

    @staticmethod
    def get_all():
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM productos_terminados ORDER BY created_at DESC"
        try:
            cursor.execute(query)
            return cursor.fetchall()
        finally:
            cursor.close()

    @staticmethod
    def create(data, foto_filename):
        conn = get_db()
        cursor = conn.cursor()
        try:
            query = """
                    INSERT INTO productos_terminados (codigo_sku, nombre, descripcion, precio_venta, \
                                                      cantidad_stock, lote_produccion, fecha_fabricacion, foto_path) \
                    VALUES (%(sku)s, %(nombre)s, %(desc)s, %(precio)s, \
                            %(stock)s, %(lote)s, %(fecha)s, %(foto)s) \
                    """
            params = {
                'sku': data.get('codigo_sku'),
                'nombre': data.get('nombre'),
                'desc': data.get('descripcion'),
                'precio': data.get('precio_venta'),
                'stock': data.get('cantidad_stock', 0),
                'lote': data.get('lote_produccion'),
                'fecha': data.get('fecha_fabricacion') or None,
                'foto': foto_filename
            }
            cursor.execute(query, params)
            conn.commit()
            return True
        except Exception as e:
            print(f"Error Producto Create: {e}")
            return False
        finally:
            cursor.close()