class Role:
    def __init__(self, id, name, id_User):
        self.id = id
        self.name = name
        self.id_User = id_User

    def __str__(self):
        return f"Role id: {self.id}, name: {self.name}"

    def jsonify(self):
        return {
            "id": self.id,
            "name": self.name,
            "id_User": self.id_User,
        }
