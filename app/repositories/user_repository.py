from app.extensions import get_db
from app.models.user import User


class UserRepository:

    # BUSCA EL USUARIO POR ELE CORREO
    @staticmethod
    def get_by_email(email):
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user_data = cursor.fetchone()

            if user_data:
                return User(**user_data)
            return None
        finally:
            cursor.close()

    # CREA UN NUEVO USUARIO Y PERSONA A LA PAR
    @staticmethod
    def create(cursor, email, password_hash, persona_id):

        query = """
                INSERT INTO users (email, password, role, persona_id)
                VALUES (%s, %s, 'user', %s) \
                """
        cursor.execute(query, (email, password_hash, persona_id))

    # GET ALL USUARIOS
    @staticmethod
    def get_all_with_persona():
        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        query = """
                SELECT u.id, \
                       u.email, \
                       u.role, \
                       u.created_at, \
                       p.nombre, \
                       p.apellido_paterno, \
                       p.apellido_materno, \
                       p.telefono, \
                       p.foto_path 
                FROM users u
                         INNER JOIN persona p ON u.persona_id = p.id
                ORDER BY u.created_at DESC \
                """
        try:
            cursor.execute(query)
            return cursor.fetchall()
        finally:
            cursor.close()

    # GET ALL USUARIOS POR EL ID
    @staticmethod
    def get_full_user_by_id(user_id):
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT u.id as user_id, \
                       u.email, \
                       u.role,
                       p.id as persona_id, \
                       p.nombre, \
                       p.apellido_paterno, \
                       p.apellido_materno,
                       p.telefono, \
                       p.calle, \
                       p.colonia, \
                       p.codigo_postal, \
                       p.foto_path
                FROM users u
                         INNER JOIN persona p ON u.persona_id = p.id
                WHERE u.id = %s \
                """
        try:
            cursor.execute(query, (user_id,))
            return cursor.fetchone()
        finally:
            cursor.close()


    # ACTUALIZAR CREDENCIALES
    @staticmethod
    def update_credentials(cursor, user_id, email, role, password_hash=None):
        if password_hash:
            query = "UPDATE users SET email=%s, role=%s, password=%s WHERE id=%s"
            cursor.execute(query, (email, role, password_hash, user_id))
        else:
            query = "UPDATE users SET email=%s, role=%s WHERE id=%s"
            cursor.execute(query, (email, role, user_id))


    # ELIMINAR USUARIO
    @staticmethod
    def delete(user_id):
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT persona_id FROM users WHERE id = %s", (user_id,))
            res = cursor.fetchone()

            if res:
                persona_id = res['persona_id']
                cursor.execute("DELETE FROM persona WHERE id = %s", (persona_id,))
                conn.commit()
                return True
            return False
        except Exception as e:
            conn.rollback()
            print(f"Error Delete User: {e}")
            return False
        finally:
            cursor.close()