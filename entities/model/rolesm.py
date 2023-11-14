class RoleModel:
    def __init__(self, id, name, isAdmin, id_User, user_username, user_last_name, user_first_name):
        self.id = id
        self.name = name
        self.isAdmin = isAdmin
        self.id_User = id_User
        self.user_username = user_username
        self.user_last_name = user_last_name
        self.user_first_name = user_first_name

    def __str__(self):
        return f"Role id: {self.id}, name: {self.name}"

    def jsonify(self):
        return {
            "id": self.id,
            "name": self.name,
            "isAdmin": self.isAdmin,
            "id_User": self.id_User,
            "user_username": self.user_username,
            "user_last_name": self.user_last_name,
            "user_first_name": self.user_first_name,
        }
