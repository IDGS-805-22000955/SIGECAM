from app.extensions import get_db


class MateriaPrimaRepository:


    @staticmethod
    def get_all():
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT mp.id, \
                       mp.codigo_interno, \
                       mp.nombre, \
                       mp.cantidad_stock, \
                       mp.unidad_medida, \
                       mp.costo_unitario, \
                       mp.foto_path, \
                       GROUP_CONCAT(p.nombre_empresa SEPARATOR ', ') as proveedor
                FROM materias_primas mp
                         LEFT JOIN proveedor_materia_prima pmp ON mp.id = pmp.materia_prima_id
                         LEFT JOIN proveedor p ON pmp.proveedor_id = p.id
                GROUP BY mp.id
                ORDER BY mp.nombre ASC \
                """
        try:
            cursor.execute(query)
            return cursor.fetchall()
        finally:
            cursor.close()

    @staticmethod
    def create(data, foto_filename):
        conn = get_db()
        try:
            conn.commit()
        except Exception:
            pass

        conn.start_transaction()
        cursor = conn.cursor()

        try:
            query_mp = """
                       INSERT INTO materias_primas (codigo_interno, nombre, descripcion, cantidad_stock, \
                                                    unidad_medida, costo_unitario, lote, fecha_caducidad, \
                                                    foto_path) \
                       VALUES (%(codigo)s, %(nombre)s, %(desc)s, %(stock)s, \
                               %(unidad)s, %(costo)s, %(lote)s, %(caducidad)s, \
                               %(foto)s) \
                       """

            params_mp = {
                'codigo': data.get('codigo_interno'),
                'nombre': data.get('nombre'),
                'desc': data.get('descripcion'),
                'stock': data.get('cantidad_stock', 0),
                'unidad': data.get('unidad_medida'),
                'costo': data.get('costo_unitario'),
                'lote': data.get('lote'),
                'caducidad': data.get('fecha_caducidad') or None,
                'foto': foto_filename
            }

            cursor.execute(query_mp, params_mp)
            new_mp_id = cursor.lastrowid

            proveedor_id = data.get('proveedor_id')
            if proveedor_id:
                query_rel = """
                            INSERT INTO proveedor_materia_prima
                                (proveedor_id, materia_prima_id, costo_unitario)
                            VALUES (%s, %s, %s) \
                            """
                cursor.execute(query_rel, (proveedor_id, new_mp_id, params_mp['costo']))

            conn.commit()
            return True

        except Exception as e:
            conn.rollback()
            print(f"Error MP Create: {e}")
            return False
        finally:
            cursor.close()