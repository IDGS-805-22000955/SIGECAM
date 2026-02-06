from app.extensions import get_db
from app.models.persona import Persona


class PersonaRepository:

    # Nuevo usuario
    @staticmethod
    def create(cursor, data):
        query = """
                INSERT INTO persona (nombre, apellido_paterno, apellido_materno, curp, rfc, \
                                     fecha_nacimiento, genero, telefono, celular, email, \
                                     calle, numero_exterior, numero_interior, colonia, \
                                     municipio, estado, codigo_postal, foto_path, pais) \
                VALUES (%(nombre)s, %(apellido_paterno)s, %(apellido_materno)s, %(curp)s, %(rfc)s, \
                        %(fecha_nacimiento)s, %(genero)s, %(telefono)s, %(celular)s, %(email)s, \
                        %(calle)s, %(numero_exterior)s, %(numero_interior)s, %(colonia)s, \
                        %(municipio)s, %(estado)s, %(codigo_postal)s, %(foto_path)s, 'México')
                """

        # Mapeo de nuevo usuario
        params = {
            'nombre': data.get('nombre'),
            'apellido_paterno': data.get('apellido_paterno'),
            'apellido_materno': data.get('apellido_materno'),
            'curp': data.get('curp'),
            'rfc': data.get('rfc'),
            # Manejo de fechas vacías: si viene vacío, enviamos None
            'fecha_nacimiento': data.get('fecha_nacimiento') if data.get('fecha_nacimiento') else None,
            'genero': data.get('genero'),
            'telefono': data.get('telefono'),
            'celular': data.get('celular'),
            'email': data.get('email'),
            'calle': data.get('calle'),
            'numero_exterior': data.get('numero_exterior'),
            'numero_interior': data.get('numero_interior'),
            'colonia': data.get('colonia'),
            'municipio': data.get('municipio'),
            'estado': data.get('estado'),
            'codigo_postal': data.get('codigo_postal'),

            # --- CORRECCIÓN AQUÍ ---
            # La llave debe ser 'foto_path' (como en el SQL),
            # pero el valor viene de data.get('foto') (como en la ruta)
            'foto_path': data.get('foto')
        }

        cursor.execute(query, params)
        return cursor.lastrowid

    # Get all usuarios
    @staticmethod
    def get_all():
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM persona")
        result = cursor.fetchall()
        cursor.close()
        return [Persona(**row) for row in result]

    # Get usuario específico
    @staticmethod
    def get_by_id(id):
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM persona WHERE id = %s", (id,))
        row = cursor.fetchone()
        cursor.close()
        if row:
            return Persona(**row)
        return None

    # Actualizar usuario
    @staticmethod
    def update(id, data):
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM persona WHERE id = %s", (id,))
            current_data = cursor.fetchone()
            if not current_data:
                return False

            query = """
                    UPDATE persona
                    SET nombre           = %(nombre)s,
                        apellido_paterno = %(apellido_paterno)s,
                        telefono         = %(telefono)s,
                        email            = %(email)s
                    WHERE id = %(id)s \
                    """

            # Mapeo de nuevo usuario(actualizado)
            params = {
                'nombre': data.get('nombre', current_data['nombre']),
                'apellido_paterno': data.get('apellido_paterno', current_data['apellido_paterno']),
                'telefono': data.get('telefono', current_data['telefono']),
                'email': data.get('email', current_data['email']),
                'id': id
            }

            cursor.execute(query, params)
            conn.commit()
            return True
        except Exception as e:
            print(f"Error update: {e}")
            return False
        finally:
            cursor.close()

    # Borrar usuario
    @staticmethod
    def delete(id):
        conn = get_db()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM persona WHERE id = %s", (id,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error delete: {e}")
            return False
        finally:
            cursor.close()