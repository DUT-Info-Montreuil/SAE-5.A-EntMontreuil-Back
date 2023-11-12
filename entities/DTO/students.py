class Student:
    def __init__(self, id, apprentice, id_User, id_Td, id_Tp, id_Promotion):
        self.id = id
        self.apprentice = apprentice
        self.id_User = id_User
        self.id_Td = id_Td
        self.id_Tp = id_Tp
        self.id_Promotion = id_Promotion

    def __str__(self):
        return f"Student id: {self.id}, apprentice: {self.apprentice}"

    def jsonify(self):
        return {
            "id": self.id,
            "apprentice": self.apprentice,
            "id_User": self.id_User,
            "id_Td": self.id_Td,
            "id_Tp": self.id_Tp,
            "id_Promotion": self.id_Promotion
        }
