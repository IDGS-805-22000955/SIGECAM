import jwt
import datetime
from flask import current_app
from app.extensions import bcrypt, get_db
from app.repositories.user_repository import UserRepository
from app.repositories.token_repository import TokenRepository
from app.repositories.persona_repository import PersonaRepository
import mysql.connector


class AuthService:

    # LOGIN
    @staticmethod
    def login_user(email, password):
        user = UserRepository.get_by_email(email)

        if user and bcrypt.check_password_hash(user.password, password):
            token_payload = {
                'user_id': user.id,
                'role': user.role,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
            }
            token = jwt.encode(
                token_payload,
                current_app.config['SECRET_KEY'],
                algorithm="HS256"
            )


            return {
                "success": True,
                "token": token,
                "role": user.role
            }

        return {"success": False, "message": "Credenciales inválidas"}


    # NUEVO USUARIO
    @staticmethod
    def register_user(user_data):
        email = user_data.get('email')
        password = user_data.get('password')
        if UserRepository.get_by_email(email):
            return {"success": False, "message": "El usuario ya existe"}
        conn = get_db()
        try:
            conn.commit()
        except Exception:
            pass

        conn.start_transaction()
        cursor = conn.cursor()
        try:
            hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
            persona_id = PersonaRepository.create(cursor, user_data)
            UserRepository.create(cursor, email, hashed_pw, persona_id)
            conn.commit()
            return {"success": True}
        except mysql.connector.Error as err:
            conn.rollback()
            print(f"Error de transacción: {err}")
            return {"success": False, "message": f"Error en base de datos: {err}"}
        except Exception as e:
            conn.rollback()
            print(f"Error general: {e}")
            return {"success": False, "message": f"Error interno: {str(e)}"}
        finally:
            cursor.close()


    # CERRAR SESIÓN
    @staticmethod
    def logout_user(token):
        try:
            data = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms=["HS256"],
                options={"verify_exp": False}
            )
            TokenRepository.add_to_blacklist(token, data['user_id'])
            return True
        except Exception as e:
            print(f"Error en logout service: {e}")
            return False