class Reminders:
    def __init__(self, id, id_User, reminder_text, reminder_date):
        self.id = id
        self.id_User = id_User
        self.reminder_text = reminder_text
        self.reminder_date = reminder_date

    def __str__(self):
        return f"Reminder id: {self.id}, id_User: {self.id_User}"

    def jsonify(self):
        return {
            "id": self.id,
            "id_User": self.id_User,
            "reminder_text": self.reminder_text,
            "reminder_date": str(self.reminder_date),
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