from project.extensions import db
from models import Proveedor


class ProveedorRepository:

    # GET ALL PROVEEDORES
    @staticmethod
    def get_all():
        return Proveedor.query.order_by(Proveedor.id_proveedor.desc()).all()

    # NUEVO PROVEEDOR
    @staticmethod
    def create(data):
        try:
            nuevo_proveedor = Proveedor(
                razon_social=data.get('razon_social'),
                rfc=data.get('rfc'),
                telefono=data.get('telefono'),
                email=data.get('email')
            )

            db.session.add(nuevo_proveedor)
            db.session.commit()

            return nuevo_proveedor.id_proveedor

        except Exception as e:
            db.session.rollback()
            print(f"Error Proveedor Create: {e}")
            return None