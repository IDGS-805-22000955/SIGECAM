from app.extensions import get_db


class ProveedorRepository:


    # Get all proveedores
    @staticmethod
    def get_all():

        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        query = """
                SELECT prov.id, \
                       prov.nombre_empresa, \
                       per.nombre as contacto_nombre, \
                       per.apellido_paterno, \
                       per.email, \
                       per.telefono, \
                       per.rfc
                FROM proveedor prov
                         INNER JOIN persona per ON prov.persona_id = per.id
                ORDER BY prov.created_at DESC \
                """
        try:
            cursor.execute(query)
            return cursor.fetchall()
        finally:
            cursor.close()


    # Nuevo proveedor
    @staticmethod
    def create(cursor, persona_id, nombre_empresa):

        query = "INSERT INTO proveedor (persona_id, nombre_empresa) VALUES (%s, %s)"
        cursor.execute(query, (persona_id, nombre_empresa))
        return cursor.lastrowid