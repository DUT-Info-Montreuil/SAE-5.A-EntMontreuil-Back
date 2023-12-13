# entities/DTO/call.py
class Calls:
    def __init__(self, id_Course, id_Student, is_present):
        self.id_Course = id_Course
        self.id_Student = id_Student
        self.is_present = is_present

    def jsonify(self):
        return {
            "id_Course": self.id_Course,
            "id_Student": self.id_Student,
            "is_present": self.is_present,
        }
