class AbsencesModel:
    def __init__(self, id_Student, id_Course, reason, document, justify, student_last_name, student_first_name,
                 course_start_time, course_end_time, resource_name, course_date):
        self.id_Student = id_Student
        self.id_Course = id_Course
        self.reason = reason
        self.document = document
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
            "document": self.document,
            "justify": self.justify,
            "resource_name": self.resource_name,
            "student_last_name": self.student_last_name,
            "student_first_name": self.student_first_name,
            "course_start_time": str(self.course_start_time),
            "course_end_time": str(self.course_end_time),
            "course_date": str(self.course_date)  # Include course date in JSON output
        }
"""ENT Montreuil is a Desktop Working Environnement for the students of the IUT of Montreuil
    Copyright (C) 2024  Steven CHING, Emilio CYRIAQUE-SOURISSEAU ALVARO-SEMEDO, Ismail GADA, Yanis HAMANI, Priyank SOLANKI

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details."""