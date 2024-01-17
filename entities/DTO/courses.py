class Course:
    def __init__(self, id, startTime, endTime, dateCourse, control, id_Resource, id_Tp, id_Td, id_Training, id_Promotion, id_Teacher, id_classroom):
        self.id = id
        self.startTime = startTime
        self.endTime = endTime
        self.dateCourse = dateCourse
        self.control = control
        self.id_Resource = id_Resource
        self.id_Tp = id_Tp
        self.id_Td = id_Td
        self.id_Training = id_Training
        self.id_Promotion = id_Promotion
        self.id_Teacher = id_Teacher
        self.id_classroom = id_classroom

    def __str__(self):
        return f"Course id: {self.id}, startTime: {self.startTime}, endTime: {self.endTime}"

    def jsonify(self):
        return {
            "id": self.id,
            "startTime": str(self.startTime),
            "endTime": str(self.endTime),
            "dateCourse": str(self.dateCourse),
            "control": self.control,
            "id_Resource": self.id_Resource,
            "id_Tp": self.id_Tp,
            "id_Td": self.id_Td,
            "id_Promotion": self.id_Promotion,
            "id_Teacher": self.id_Teacher,
            "id_classroom": self.id_classroom,
            "id_Training" : self.id_Training
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