from project.extensions import db
from models import Usuario

class UserRepository:

    @staticmethod
    def get_by_username(nombre_usuario):
        return Usuario.query.filter_by(nombre_usuario=nombre_usuario).first()

    @staticmethod
    def get_by_id(id_usuario):
        return Usuario.query.get(id_usuario)

    @staticmethod
    def get_all():
        return Usuario.query.all()

    @staticmethod
    def create(nombre_usuario, password_hash, rol):
        nuevo_usuario = Usuario(
            nombre_usuario=nombre_usuario,
            password_hash=password_hash,
            rol=rol
        )
        db.session.add(nuevo_usuario)
        db.session.commit()
        return nuevo_usuario

    @staticmethod
    def update_credentials(id_usuario, nombre_usuario, rol, password_hash=None):
        usuario = Usuario.query.get(id_usuario)
        if usuario:
            usuario.nombre_usuario = nombre_usuario
            usuario.rol = rol
            if password_hash:
                usuario.password_hash = password_hash
            db.session.commit()
            return True
        return False

    @staticmethod
    def delete(id_usuario):
        usuario = Usuario.query.get(id_usuario)
        if usuario:
            db.session.delete(usuario)
            db.session.commit()
            return True
        return False