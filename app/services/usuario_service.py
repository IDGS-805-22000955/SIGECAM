from app.extensions import get_db, bcrypt
from app.repositories.persona_repository import PersonaRepository
from app.repositories.user_repository import UserRepository
import mysql.connector


class UsuarioService:

    @staticmethod
    def create_user(data):

        conn = get_db()

        try:
            conn.commit()
        except Exception:
            pass

        conn.start_transaction()
        cursor = conn.cursor()

        try:
            persona_id = PersonaRepository.create(cursor, data)

            email = data.get('email')
            raw_password = data.get('password')

            password_hash = bcrypt.generate_password_hash(raw_password).decode('utf-8')

            UserRepository.create(cursor, email, password_hash, persona_id)

            conn.commit()
            return {"success": True}

        except mysql.connector.Error as err:
            conn.rollback()
            if err.errno == 1062:
                return {"success": False, "message": "El correo electrónico ya está registrado."}
            return {"success": False, "message": f"Error BD: {err}"}

        except Exception as e:
            conn.rollback()
            return {"success": False, "message": f"Error interno: {str(e)}"}

        finally:
            cursor.close()

    @staticmethod
    def update_user(user_id, data):
        conn = get_db()
        try:
            conn.commit()
        except:
            pass

        conn.start_transaction()
        cursor = conn.cursor()

        try:
            current = UserRepository.get_full_user_by_id(user_id)
            if not current:
                return {"success": False, "message": "Usuario no encontrado"}

            query_persona = """
                            UPDATE persona \
                            SET nombre=%(nombre)s, \
                                apellido_paterno=%(ap_pat)s, \
                                apellido_materno=%(ap_mat)s, \
                                telefono=%(tel)s, \
                                calle=%(calle)s, \
                                colonia=%(col)s, \
                                codigo_postal=%(cp)s
                            WHERE id = %(pid)s \
                            """
            params_p = {
                'nombre': data['nombre'], 'ap_pat': data['apellido_paterno'],
                'ap_mat': data.get('apellido_materno'), 'tel': data.get('telefono'),
                'calle': data.get('calle'), 'col': data.get('colonia'),
                'cp': data.get('codigo_postal'), 'pid': current['persona_id']
            }
            cursor.execute(query_persona, params_p)


            if data.get('foto'):
                cursor.execute("UPDATE persona SET foto_path=%s WHERE id=%s", (data['foto'], current['persona_id']))


            email = data['email']
            role = data.get('role', 'user')

            password_hash = None
            if data.get('password'):
                password_hash = bcrypt.generate_password_hash(data['password']).decode('utf-8')

            UserRepository.update_credentials(cursor, user_id, email, role, password_hash)

            conn.commit()
            return {"success": True}

        except Exception as e:
            conn.rollback()
            return {"success": False, "message": str(e)}
        finally:
            cursor.close()

    @staticmethod
    def delete_user(user_id):
        return UserRepository.delete(user_id)