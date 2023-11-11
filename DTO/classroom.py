class Classroom:
    def __init__(self, id, name, capacity, equipment, id_Course):
        self.id = id
        self.name = name
        self.capacity = capacity
        self.equipment = equipment
        self.id_Course = id_Course

    def __str__(self):
        return f"Classroom id: {self.id}, name: {self.name}"
    
    def jsonify(self):
        return {
            "id": self.id,
            "name": self.name,
            "capacity": self.capacity,
            "equipment": self.equipment,
            "id_Course": self.id_Course
        }
