class TDModel:
    def __init__(self, id, name, id_Promotion, id_Training, promotion_year, training_name, training_promotion):
        self.id = id
        self.name = name
        self.id_Promotion = id_Promotion
        self.id_Training = id_Training
        self.promotion_year = promotion_year
        self.training_name = training_name
        self.training_promotion = training_promotion

    def __str__(self):
        return f"TD id: {self.id}, name: {self.name}"

    def jsonify(self):
        return {
            "id": self.id,
            "name": self.name,
            "id_Promotion": self.id_Promotion,
            "id_Training": self.id_Training,
            "promotion_year": self.promotion_year,
            "training_name": self.training_name,
            "training_promotion" : self.training_promotion
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