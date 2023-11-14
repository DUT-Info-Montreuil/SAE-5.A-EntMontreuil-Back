class Role:
    def __init__(self, id, name, isAdmin, id_User):
        self.id = id
        self.name = name
        self.isAdmin = isAdmin
        self.id_User = id_User

    def __str__(self):
        return f"Role id: {self.id}, name: {self.name}"

    def jsonify(self):
        return {
            "id": self.id,
            "name": self.name,
            "isAdmin": self.isAdmin,
            "id_User": self.id_User,
        }
