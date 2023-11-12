class Resource:
    def __init__(self, id, name, id_Promotion):
        self.id = id
        self.name = name
        self.id_Promotion = id_Promotion

    def __str__(self):
        return f"Resource id: {self.id}, name: {self.name}"

    def jsonify(self):
        return {
            "id": self.id,
            "name": self.name,
            "id_Promotion": self.id_Promotion,
        }
