from app.extensions import get_db


class AdminRepository:

    @staticmethod
    def get_dashboard_stats():
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        stats = {}

        try:
            # GET ALL USUARIOS(TABLA)
            cursor.execute("SELECT COUNT(*) as total FROM users")
            stats['usuarios'] = cursor.fetchone()['total']

            # GET ALL PROVEEDORES(TABLA)
            cursor.execute("SELECT COUNT(*) as total FROM proveedor")
            stats['proveedores'] = cursor.fetchone()['total']

            # GET ALL MATERIAS PRIMAS(TABLA)
            cursor.execute("SELECT COALESCE(SUM(cantidad_stock * costo_unitario), 0) as total FROM materias_primas")
            stats['valor_mp'] = cursor.fetchone()['total']

            # GET ALL PRODUCTOS(TABLA)
            cursor.execute("SELECT COUNT(*) as total FROM productos_terminados")
            stats['productos'] = cursor.fetchone()['total']

            return stats
        except Exception as e:
            print(f"Error Stats: {e}")
            return {'usuarios': 0, 'proveedores': 0, 'valor_mp': 0, 'productos': 0}
        finally:
            cursor.close()