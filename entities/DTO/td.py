class TD:
    def __init__(self, id, name, id_Promotion, id_Training):
        self.id = id
        self.name = name
        self.id_Promotion = id_Promotion
        self.id_Training = id_Training

    def __str__(self):
        return f"TD id: {self.id}, name: {self.name}"

    def jsonify(self):
        return {
            "id": self.id,
            "name": self.name,
            "id_Promotion": self.id_Promotion,
            "id_Training": self.id_Training,
        }
