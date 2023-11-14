class Users:
    def __init__(self, id, username, password, last_name, first_name, email, isAdmin, id_Role):
        self.id = id
        self.username = username
        self.password = password
        self.last_name = last_name
        self.first_name = first_name
        self.email = email
        self.isAdmin = isAdmin
        self.id_Role = id_Role

    def __str__(self):
        return f"User id: {self.id}, username: {self.username}"

    def jsonify(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "last_name": self.last_name,
            "first_name": self.first_name,
            "email": self.email,
            "isAdmin": self.isAdmin,
            "id_Role": self.id_Role,
        }