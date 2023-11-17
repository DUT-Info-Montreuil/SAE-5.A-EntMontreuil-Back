class ClassroomModel:
    def __init__(self, id, name, capacity, materials):
        self.id = id
        self.name = name
        self.capacity = capacity
        self.materials = materials  # Une liste de matériel

    def __str__(self):
        return f"Classroom id: {self.id}, name: {self.name}"

    def jsonify(self):
        materials_json = []
        for material in self.materials:
            materials_json.append({
                "id": material["id"],
                "equipment": material["equipment"],
                "quantity": material["quantity"]
            })

        return {
            "id": self.id,
            "name": self.name,
            "capacity": self.capacity,
            "materials": materials_json
        }
