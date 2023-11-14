class UsersModel:
    def __init__(self, id, username, password, last_name, first_name, email, id_Role, role_name, role_isAdmin):
        self.id = id
        self.username = username
        self.password = password
        self.last_name = last_name
        self.first_name = first_name
        self.email = email
        self.id_Role = id_Role
        self.role_name = role_name
        self.role_isAdmin = role_isAdmin
        

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
            "id_Role": self.id_Role,
            "role_name": self.role_name,
            "role_isAdmin": self.role_isAdmin,
        }