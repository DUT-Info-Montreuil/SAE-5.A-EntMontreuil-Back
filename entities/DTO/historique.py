class Historique:
    def __init__(self, id, id_User, modification):
        self.id = id
        self.id_User = id_User
        self.modification = modification

    def __str__(self):
        return f"Historique id: {self.id}, modification: {self.modification}"

    def jsonify(self):
        return {
            "id": self.id,
            "id_User": self.id_User,
            "modification": self.modification
        }
