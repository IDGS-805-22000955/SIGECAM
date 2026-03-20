from project.repositories.proveedor_repository import ProveedorRepository


class ProveedorService:

    @staticmethod
    def create_proveedor(data):
        try:
            proveedor_id = ProveedorRepository.create(data)

            if proveedor_id:
                return {"success": True}

            return {"success": False, "message": "No se pudo crear el proveedor."}

        except Exception as e:
            return {"success": False, "message": f"Error interno: {str(e)}"}