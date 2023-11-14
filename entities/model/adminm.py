class AdminModel:
    def __init__(self, id, id_User, user_last_name, user_first_name, user_email):
        self.id = id
        self.id_User = id_User

        # user
        self.user_last_name = user_last_name
        self.user_first_name = user_first_name
        self.user_email = user_email

    def __str__(self):
        return f"Admin id: {self.id}"

    def jsonify(self):
        return {
            "id": self.id,
            "id_User": self.id_User,
            "user_last_name": self.user_last_name,
            "user_first_name": self.user_first_name,
            "user_email": self.user_email,
        }
