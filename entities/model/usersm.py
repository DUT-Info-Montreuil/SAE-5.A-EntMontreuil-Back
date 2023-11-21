class UsersModel:
    def __init__(self, id, password, username, last_name, first_name, email , id_Role ,role_name, isAdmin):
        self.id = id
        self.password = password
        self.username = username
        self.last_name = last_name
        self.first_name = first_name
        self.email = email
        self.id_Role = id_Role
        self.role_name = role_name
        self.isAdmin = isAdmin

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
                }
            }
            
            
        }