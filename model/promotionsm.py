class PromotionsModel:
    def __init__(self, id, year, id_Training, training_name):
        self.id = id
        self.year = year
        self.id_Training = id_Training

        # training
        self.training_name = training_name

    def __str__(self):
        return f"Promotion id: {self.id}, year: {self.year}"

    def jsonify(self):
        return {
            "id": self.id,
            "year": self.year,
            "id_Training": self.id_Training,
            "training_name": self.training_name
        }