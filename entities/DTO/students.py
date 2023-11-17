class Students:
    def __init__(self, id, nip, apprentice, id_User, id_Td, id_Tp, id_Promotion, ine):
        self.id = id
        self.nip = nip
        self.apprentice = apprentice
        self.id_User = id_User
        self.id_Td = id_Td
        self.id_Tp = id_Tp
        self.id_Promotion = id_Promotion
        self.ine = ine

    def __str__(self):
        return f"Student id: {self.id}, numero: {self.numero}"

    def jsonify(self):
        return {
            "id": self.id,
            "nip": self.nip,
            "apprentice": self.apprentice,
            "id_User": self.id_User,
            "id_Td": self.id_Td,
            "id_Tp": self.id_Tp,
            "id_Promotion": self.id_Promotion,
            "ine" : self.ine
        }
