class TDModel:
    def __init__(self, id, name, id_Promotion, promotion_year):
        self.id = id
        self.name = name
        self.id_Promotion = id_Promotion

        # promotion
        self.promotion_year = promotion_year

    def __str__(self):
        return f"TD id: {self.id}, name: {self.name}"

    def jsonify(self):
        return {
            "id": self.id,
            "name": self.name,
            "id_Promotion": self.id_Promotion,
            "promotion_year": self.promotion_year
        }