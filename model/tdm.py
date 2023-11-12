class TDModel:
    def __init__(self, id, name, id_Promotion, id_Training, promotion_year, training_name):
        self.id = id
        self.name = name
        self.id_Promotion = id_Promotion
        self.id_Training = id_Training
        self.promotion_year = promotion_year
        self.training_name = training_name

    def __str__(self):
        return f"TD id: {self.id}, name: {self.name}"

    def jsonify(self):
        return {
            "id": self.id,
            "name": self.name,
            "id_Promotion": self.id_Promotion,
            "id_Training": self.id_Training,
            "promotion_year": self.promotion_year,
            "training_name": self.training_name,
        }
