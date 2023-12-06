class TrainingModel:
    def __init__(self, id, name, id_Promotion, semester, promotion_year, promotion_level, id_Degree, degree_name):
        self.id = id
        self.name = name
        self.id_Promotion = id_Promotion
        self.semester = semester
        self.promotion_year = promotion_year
        self.promotion_level = promotion_level
        self.id_Degree = id_Degree
        self.degree_name = degree_name

    def __str__(self):
        return f"Training id: {self.id}, name: {self.name}"

    def jsonify(self):
        return {
            "id": self.id,
            "name": self.name,
            "id_Promotion": self.id_Promotion,
            "semester": self.semester,
            "promotion_year" : self.promotion_year,
            "promotion_level" : self.promotion_level,
            "id_Degree" : self.id_Degree,
            "degree_name" : self.degree_name
        }
