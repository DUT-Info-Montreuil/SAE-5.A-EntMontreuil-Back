class TrainingModel:
    def __init__(self, id, name, id_Degree, degree_name):
        self.id = id
        self.name = name
        self.id_Degree = id_Degree
        self.degree_name = degree_name

    def __str__(self):
        return f"Training id: {self.id}, name: {self.name}"

    def jsonify(self):
        return {
            "id": self.id,
            "name": self.name,
            "id_Degree": self.id_Degree,
            "degree_name": self.degree_name,
        }
