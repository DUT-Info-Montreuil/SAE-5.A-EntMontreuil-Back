class Classroom:
    def __init__(self, id, name, capacity, id_Material):
        self.id = id
        self.name = name
        self.capacity = capacity
        self.id_Material = id_Material

    def __str__(self):
        return f"Classroom id: {self.id}, name: {self.name}"

    def jsonify(self):
        return {
            "id": self.id,
            "name": self.name,
            "capacity": self.capacity,
            "id_Material": self.id_Material,
        }
