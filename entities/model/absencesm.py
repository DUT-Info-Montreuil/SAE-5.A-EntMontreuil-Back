class AbsencesModel:
    def __init__(self, id_Student, id_Course, reason, justify, student_last_name, student_first_name,
                 course_start_time, course_end_time):
        self.id_Student = id_Student
        self.id_Course = id_Course
        self.reason = reason
        self.justify = justify

        # student
        self.student_last_name = student_last_name
        self.student_first_name = student_first_name

        # course
        self.course_start_time = course_start_time
        self.course_end_time = course_end_time

    def __str__(self):
        return f"Absence for student {self.id_Student} in course {self.id_Course}"

    def jsonify(self):
        return {
            "id_Student": self.id_Student,
            "id_Course": self.id_Course,
            "reason": self.reason,
            "justify": self.justify,
            "student_last_name": self.student_last_name,
            "student_first_name": self.student_first_name,
            "course_start_time": str(self.course_start_time),
            "course_end_time": str(self.course_end_time)
        }