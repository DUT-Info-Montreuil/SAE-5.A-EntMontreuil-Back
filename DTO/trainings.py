class Training:
    def __init__(self, id, name, id_Degree):
        self.id = id
        self.name = name
        self.id_Degree = id_Degree

    def __str__(self):
        return f"Training id: {self.id}, name: {self.name}"

    def jsonify(self):
        return {
            "id": self.id,
            "name": self.name,
            "id_Degree": self.id_Degree,
        }
