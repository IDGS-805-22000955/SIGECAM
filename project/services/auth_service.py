import jwt
import datetime
from flask import current_app
from project.extensions import bcrypt, db
from project.repositories.user_repository import UserRepository
from project.repositories.token_repository import TokenRepository


class AuthService:

    # LOGIN
    @staticmethod
    def login_user(nombre_usuario, password):
        user = UserRepository.get_by_username(nombre_usuario)

        if user and bcrypt.check_password_hash(user.password_hash, password):
            token_payload = {
                'user_id': user.id_usuario,
                'role': user.rol,
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
                "role": user.rol
            }

        return {"success": False, "message": "Credenciales inválidas"}

    # REGISTRO
    @staticmethod
    def register_user(user_data):
        nombre_usuario = user_data.get('nombre_usuario')
        password = user_data.get('password')
        rol = user_data.get('rol', 'Ventas')

        if UserRepository.get_by_username(nombre_usuario):
            return {"success": False, "message": "El usuario ya existe"}

        try:
            hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')

            UserRepository.create(nombre_usuario, hashed_pw, rol)

            return {"success": True}

        except Exception as e:
            db.session.rollback()
            print(f"Error general: {e}")
            return {"success": False, "message": f"Error interno: {str(e)}"}

    # LOGOUT
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