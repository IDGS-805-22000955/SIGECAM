from project.extensions import bcrypt
from project.repositories.user_repository import UserRepository


class UsuarioService:

    @staticmethod
    def create_user(data):
        try:
            nombre_usuario = data.get('nombre_usuario')
            raw_password = data.get('password')
            rol = data.get('rol', 'Ventas')

            if UserRepository.get_by_username(nombre_usuario):
                return {"success": False, "message": "El nombre de usuario ya está registrado."}

            password_hash = bcrypt.generate_password_hash(raw_password).decode('utf-8')
            usuario_creado = UserRepository.create(nombre_usuario, password_hash, rol)

            if usuario_creado:
                return {"success": True}

            return {"success": False, "message": "No se pudo crear el usuario."}

        except Exception as e:
            return {"success": False, "message": f"Error interno: {str(e)}"}

    @staticmethod
    def update_user(id_usuario, data):
        try:
            nombre_usuario = data.get('nombre_usuario')
            rol = data.get('rol')

            password_hash = None
            if data.get('password'):
                password_hash = bcrypt.generate_password_hash(data['password']).decode('utf-8')

            actualizado = UserRepository.update_credentials(id_usuario, nombre_usuario, rol, password_hash)

            if actualizado:
                return {"success": True}

            return {"success": False, "message": "Usuario no encontrado."}

        except Exception as e:
            return {"success": False, "message": f"Error interno: {str(e)}"}

    @staticmethod
    def delete_user(id_usuario):
        return UserRepository.delete(id_usuario)