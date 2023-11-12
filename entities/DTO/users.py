class Users:
    def __init__(self, id, username, password, type, last_name, first_name, email):
        self.id = id
        self.username = username
        self.password = password
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
            "password": self.password,
            "type": self.type,
            "last_name": self.last_name,
            "first_name": self.first_name,
            "email": self.email,
        }