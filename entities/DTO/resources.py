class Resource:
    def __init__(self, id, name, id_Training, color):
        self.id = id
        self.name = name
        self.id_Training = id_Training
        self.color = color

    def __str__(self):
        return f"Resource id: {self.id}, name: {self.name}"

    def jsonify(self):
        return {
            "id": self.id,
            "name": self.name,
            "id_Training": self.id_Training,
            "color" :self.color
        }
