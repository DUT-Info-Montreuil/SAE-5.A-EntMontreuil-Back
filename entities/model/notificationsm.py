class NotificationModel:
    def __init__(self, id, id_user, content, is_read, created_at, title, icon, icon_color, route):
        self.id = id
        self.id_user = id_user
        self.content = content
        self.is_read = is_read
        self.created_at = created_at
        self.title = title
        self.icon = icon
        self.icon_color = icon_color
        self.route = route

    def __str__(self):
        return f"Notification id: {self.id}, id_user: {self.id_user}"

    def jsonify(self):
        return {
            "notification": {
                "id": self.id,
                "id_user": self.id_user,
                "content": self.content,
                "is_read": self.is_read,
                "created_at": str(self.created_at),
                "title": self.title,
                "icon": self.icon,
                "icon_color": self.icon_color,
                "route": self.route
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