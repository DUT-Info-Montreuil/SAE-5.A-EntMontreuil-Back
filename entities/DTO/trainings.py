class Training:
    def __init__(self, id, name, id_Promotion, semester):
        self.id = id
        self.name = name
        self.id_Promotion = id_Promotion
        self.semester = semester

    def __str__(self):
        return f"Training id: {self.id}, name: {self.name}"

    def jsonify(self):
        return {
            "id": self.id,
            "name": self.name,
            "id_Promotion": self.id_Promotion,
            "semester" : self.semester
        }
