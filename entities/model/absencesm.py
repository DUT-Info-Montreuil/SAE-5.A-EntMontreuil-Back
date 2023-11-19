class AbsencesModel:
    def __init__(self, id_Student, id_Course, reason, justify, student_last_name, student_first_name,
                 course_start_time, course_end_time, resource_name, course_date):
        self.id_Student = id_Student
        self.id_Course = id_Course
        self.reason = reason
        self.justify = justify
        self.resource_name = resource_name  # Existing attribute for resource name

        # student
        self.student_last_name = student_last_name
        self.student_first_name = student_first_name

        # course
        self.course_start_time = course_start_time
        self.course_end_time = course_end_time
        self.course_date = course_date  # New attribute for course date

    def __str__(self):
        return f"Absence for student {self.id_Student} in course {self.id_Course} on {self.course_date}"

    def jsonify(self):
        return {
            "id_Student": self.id_Student,
            "id_Course": self.id_Course,
            "reason": self.reason,
            "justify": self.justify,
            "resource_name": self.resource_name,
            "student_last_name": self.student_last_name,
            "student_first_name": self.student_first_name,
            "course_start_time": str(self.course_start_time),
            "course_end_time": str(self.course_end_time),
            "course_date": str(self.course_date)  # Include course date in JSON output
        }
