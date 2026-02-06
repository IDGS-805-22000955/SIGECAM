class Persona:
    def __init__(self, id, nombre, apellido_paterno, **kwargs):
        self.id = id
        self.nombre = nombre
        self.apellido_paterno = apellido_paterno
        self.otros_datos = kwargs

    def to_dict(self):
        base = {
            'id': self.id,
            'nombre': self.nombre,
            'apellido_paterno': self.apellido_paterno
        }

        return {**base, **self.otros_datos}