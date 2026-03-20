from project.extensions import db
from models import TokenSeguridad
from datetime import datetime

class TokenRepository:

    @staticmethod
    def add_to_blacklist(token, id_usuario):
        try:
            nuevo_token_invalido = TokenSeguridad(
                id_usuario=id_usuario,
                token_hash=token,
                tipo='2FA',
                fecha_expiracion=datetime.utcnow(),
                usado=True
            )
            db.session.add(nuevo_token_invalido)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error Blacklist: {e}")
            return False


    @staticmethod
    def is_blacklisted(token):
        token_record = TokenSeguridad.query.filter_by(token_hash=token, usado=True).first()
        return token_record is not None