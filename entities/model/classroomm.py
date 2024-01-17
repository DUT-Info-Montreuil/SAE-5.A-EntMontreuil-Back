class ClassroomModel:
    def __init__(self, id, name, capacity, materials):
        self.id = id
        self.name = name
        self.capacity = capacity
        self.materials = materials  # Une liste de matériel

    def __str__(self):
        return f"Classroom id: {self.id}, name: {self.name}"

    def jsonify(self):
        materials_json = []
        for material in self.materials:
            materials_json.append({
                "id": material["id"],
                "equipment": material["equipment"],
                "quantity": material["quantity"]
            })

        return {
            "id": self.id,
            "name": self.name,
            "capacity": self.capacity,
            "materials": materials_json
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