class Promotion:
    def __init__(self, id, year, id_Degree):
        self.id = id
        self.year = year
        self.id_Degree = id_Degree

    def __str__(self):
        return f"Promotion id: {self.id}, year: {self.year}"

    def jsonify(self):
        return {
            "id": self.id,
            "year": self.year,
            "id_Degree": self.id_Degree,
        }
