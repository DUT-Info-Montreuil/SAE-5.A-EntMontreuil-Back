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
