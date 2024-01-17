class TeachersModel:
    def __init__(self, id, initial, desktop, id_User, user_last_name, user_first_name, user_username, user_email, user_isAdmin, id_role, role_name, user_isTTManager):
        self.id = id
        self.initial = initial
        self.desktop = desktop
        self.id_User = id_User

        # user
        self.user_last_name = user_last_name
        self.user_first_name = user_first_name
        self.user_username = user_username
        self.user_email = user_email
        self.user_isAdmin = user_isAdmin
        self.id_role = id_role
        self.role_name = role_name
        self.user_isTTManager = user_isTTManager

    def __str__(self):
        return f"Teacher id: {self.id}, initital: {self.initital}"

    def jsonify(self):
        return {
            "personal_info" : {
                "initial" : self.initial,
                "desktop" : self.desktop,
                "id" : self.id
            },
            "user" : {
                "id": self.id_User,
                "last_name": self.user_last_name,
                "first_name": self.user_first_name,
                "username": self.user_username,
                "email" : self.user_email,
                "isAdmin": self.user_isAdmin,
                "role" : {
                    "id" : self.id_role,
                    "name" : self.role_name,
                },
                "isTTManager" : self.user_isTTManager
                
            },
                
                
            
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