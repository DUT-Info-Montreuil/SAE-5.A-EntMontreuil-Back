class Users:
    def __init__(self, id, username, last_name, first_name, email , id_Role , isAdmin):
        self.id = id
        self.username = username
        self.last_name = last_name
        self.first_name = first_name
        self.email = email
        self.id_Role = id_Role
        self.isAdmin = isAdmin

    def __str__(self):
        return f"User id: {self.id}, username: {self.username}"

    def jsonify(self):
        return {
            "id": self.id,
            "username": self.username,
            "last_name": self.last_name,
            "first_name": self.first_name,
            "email": self.email,
            "id_Role" : self.id_Role,
            "isAdmin" : self.isAdmin,
        }