class Degrees:
    def __init__(self, id, name, id_Training):
        self.id = id
        self.name = name
        self.id_Training = id_Training

    def __str__(self):
        return f"Degree id: {self.id}, name: {self.name}"

    def jsonify(self):
        return {
            "id": self.id,
            "name": self.name,
            "id_Training": self.id_Training
        }