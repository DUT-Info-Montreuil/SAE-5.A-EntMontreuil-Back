class Absences:
    def __init__(self, id_Student, id_Course, reason, document, justify):
        self.id_Student = id_Student
        self.id_Course = id_Course
        self.reason = reason
        self.document = document
        self.justify = justify

    def __str__(self):
        return f"Absence for student {self.id_Student} in course {self.id_Course}"
    
    def jsonify(self):
        return {
            "id_Student": self.id_Student,
            "id_Course": self.id_Course,
            "reason": self.reason,
            "document": self.document,  
            "justify": self.justify
        }