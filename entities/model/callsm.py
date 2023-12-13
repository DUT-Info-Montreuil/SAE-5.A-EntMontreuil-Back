# entities/model/callm.py
class CallsModel:
    def __init__(self, id, id_Course, id_Student, is_present, student_last_name, student_first_name ):
        self.id = id
        self.id_Course = id_Course
        self.id_Student = id_Student
        self.is_present = is_present
        self.student_last_name = student_last_name
        self.student_first_name = student_first_name

    def jsonify(self):
        return {
            "id": self.id,
            "id_Course": self.id_Course,
            "id_Student": self.id_Student,
            "is_present": self.is_present,
            "student_last_name": self.student_last_name,
            "student_first_name": self.student_first_name,
        }
