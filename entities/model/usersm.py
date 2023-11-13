class UsersModel:
    def __init__(self, id, username, type, last_name, first_name, email):
        self.id = id
        self.username = username
        self.type = type
        self.last_name = last_name
        self.first_name = first_name
        self.email = email

    def __str__(self):
        return f"User id: {self.id}, username: {self.username}"

    def jsonify(self):
        return {
            "id": self.id,
            "username": self.username,
            "type": self.type,
            "last_name": self.last_name,
            "first_name": self.first_name,
            "email": self.email,
        }
        
        