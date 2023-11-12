class HistoriqueModel:
    def __init__(self, id, id_User, modification, user_last_name, user_first_name):
        self.id = id
        self.id_User = id_User
        self.modification = modification

        # user
        self.user_last_name = user_last_name
        self.user_first_name = user_first_name

    def __str__(self):
        return f"Historique id: {self.id}, modification: {self.modification}"

    def jsonify(self):
        return {
            "id": self.id,
            "id_User": self.id_User,
            "modification": self.modification,
            "user_last_name": self.user_last_name,
            "user_first_name": self.user_first_name
        }
