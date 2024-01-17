class Students:
    def __init__(self, id, nip, apprentice, id_User, id_Td, id_Tp, id_Promotion, ine):
        self.id = id
        self.nip = nip
        self.apprentice = apprentice
        self.id_User = id_User
        self.id_Td = id_Td
        self.id_Tp = id_Tp
        self.id_Promotion = id_Promotion
        self.ine = ine

    def __str__(self):
        return f"Student id: {self.id}, numero: {self.numero}"

    def jsonify(self):
        return {
            "id": self.id,
            "nip": self.nip,
            "apprentice": self.apprentice,
            "id_User": self.id_User,
            "id_Td": self.id_Td,
            "id_Tp": self.id_Tp,
            "id_Promotion": self.id_Promotion,
            "ine" : self.ine
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