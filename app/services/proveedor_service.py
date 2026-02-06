from app.extensions import get_db
from app.repositories.persona_repository import PersonaRepository
from app.repositories.proveedor_repository import ProveedorRepository
import mysql.connector


class ProveedorService:

    @staticmethod
    def create_proveedor(data):

        conn = get_db()

        try:
            conn.commit()
        except Exception:
            pass

        conn.start_transaction()
        cursor = conn.cursor()

        try:
            persona_id = PersonaRepository.create(cursor, data)

            nombre_empresa = data.get('nombre_empresa')
            ProveedorRepository.create(cursor, persona_id, nombre_empresa)

            conn.commit()
            return {"success": True}

        except mysql.connector.Error as err:
            conn.rollback()
            return {"success": False, "message": f"Error BD: {err}"}
        except Exception as e:
            conn.rollback()
            return {"success": False, "message": f"Error: {str(e)}"}
        finally:
            cursor.close()