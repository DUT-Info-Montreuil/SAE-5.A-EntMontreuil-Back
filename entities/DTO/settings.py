class Settings:
    def __init__(self, id_user, notification_mail, notification_website):
        self.id_user = id_user
        self.notification_mail = notification_mail
        self.notification_website = notification_website

    def __str__(self):
            return f"Settings for user: {self.id_user}, notification_mail: {self.notification_mail}, notification_website: {self.notification_website}"  
    
    def jsonify(self):
        return {
            "id_User": self.id_user,
            "notification_mail": self.notification_mail,
            "notification_website": self.notification_website
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