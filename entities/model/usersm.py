class UsersModel:
    def __init__(self, id, password, username, last_name, first_name, email , id_Role ,role_name, isAdmin, isTTManager):
        self.id = id
        self.password = password
        self.username = username
        self.last_name = last_name
        self.first_name = first_name
        self.email = email
        self.id_Role = id_Role
        self.role_name = role_name
        self.isAdmin = isAdmin
        self.isTTManager = isTTManager

    def __str__(self):
        return f"User id: {self.id}, username: {self.username}"

    def jsonify(self):
        return {
            "user" : {
                "id": self.id,
                "password" : self.password,
                "username": self.username,
                "last_name": self.last_name,
                "first_name": self.first_name,
                "email": self.email,
                "isAdmin" : self.isAdmin,
                "role": {
                    "id" : self.id_Role,
                    "name" : self.role_name,
                },
                "isTTManager" : self.isTTManager
            }
            
            
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