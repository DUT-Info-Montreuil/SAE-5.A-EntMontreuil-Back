class Classroom:
    def __init__(self, id, name, capacity):
        self.id = id
        self.name = name
        self.capacity = capacity


    def __str__(self):
        return f"Classroom id: {self.id}, name: {self.name}"

    def jsonify(self):
        return {
            "id": self.id,
            "name": self.name,
            "capacity": self.capacity,
        }
