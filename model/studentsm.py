class StudentsModel:
    def __init__(self, id, apprentice, id_User, id_Td, id_Tp, id_Promotion, user_last_name, user_first_name,
                 td_name, tp_name, promotion_year):
        self.id = id
        self.apprentice = apprentice
        self.id_User = id_User
        self.id_Td = id_Td
        self.id_Tp = id_Tp
        self.id_Promotion = id_Promotion

        # user
        self.user_last_name = user_last_name
        self.user_first_name = user_first_name

        # td
        self.td_name = td_name

        # tp
        self.tp_name = tp_name

        # promotion
        self.promotion_year = promotion_year

    def __str__(self):
        return f"Student id: {self.id}, apprentice: {self.apprentice}"

    def jsonify(self):
        return {
            "id": self.id,
            "apprentice": self.apprentice,
            "id_User": self.id_User,
            "id_Td": self.id_Td,
            "id_Tp": self.id_Tp,
            "id_Promotion": self.id_Promotion,
            "user_last_name": self.user_last_name,
            "user_first_name": self.user_first_name,
            "td_name": self.td_name,
            "tp_name": self.tp_name,
            "promotion_year": self.promotion_year
        }