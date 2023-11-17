class Roles:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __str__(self):
        return f"Role id: {self.id}, name: {self.name}"

    def jsonify(self):
        return {
            "id": self.id,
            "name": self.name
        }