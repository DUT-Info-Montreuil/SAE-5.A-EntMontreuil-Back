class Material:
    def __init__(self, id, equipment, quantity):
        self.id = id
        self.equipment = equipment
        self.quantity = quantity

    def __str__(self):
        return f"Material id: {self.id}, equipment: {self.equipment}"

    def jsonify(self):
        return {
            "id": self.id,
            "equipment": self.equipment,
            "quantity": self.quantity
        }
