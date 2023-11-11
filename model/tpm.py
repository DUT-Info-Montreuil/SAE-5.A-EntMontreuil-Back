class TPModel:
    def __init__(self, id, name, id_Td, td_name):
        self.id = id
        self.name = name
        self.id_Td = id_Td

        # td
        self.td_name = td_name

    def __str__(self):
        return f"TP id: {self.id}, name: {self.name}"

    def jsonify(self):
        return {
            "id": self.id,
            "name": self.name,
            "id_Td": self.id_Td,
            "td_name": self.td_name
        }