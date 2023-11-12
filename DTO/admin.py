class Admin:
    def __init__(self, id, id_User):
        self.id = id
        self.id_User = id_User

    def __str__(self):
        return f"Admin id: {self.id}"

    def jsonify(self):
        return {
            "id": self.id,
            "id_User": self.id_User,
        }
