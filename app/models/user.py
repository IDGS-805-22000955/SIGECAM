class User:
    def __init__(self, id, email, password, role, persona_id, created_at=None, **kwargs):
        self.id = id
        self.email = email
        self.password = password
        self.role = role
        self.persona_id = persona_id
        self.created_at = created_at
        self.extra_data = kwargs

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'role': self.role,
            'persona_id': self.persona_id
        }