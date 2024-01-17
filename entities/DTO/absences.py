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