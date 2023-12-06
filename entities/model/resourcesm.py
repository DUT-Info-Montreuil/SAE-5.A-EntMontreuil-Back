class ResourceModel:
    def __init__(self, id, name, id_Training, color, training_name, training_sermester ):
        self.id = id
        self.name = name
        self.id_Training = id_Training
        self.color = color
        self.training_name = training_name
        self.training_sermester = training_sermester

    def __str__(self):
        return f"Resource id: {self.id}, name: {self.name}"

    def jsonify(self):
        return {
            "id": self.id,
            "name": self.name,
            "id_Training": self.id_Training,
            "color": self.color,
            "training_name" : self.training_name,
            "training_sermester" : self.training_sermester
        }
