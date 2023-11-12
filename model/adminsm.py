class AdminModel:
    def __init__(self, id_Admin, id_User, user_username, user_type, user_first_name,
                 user_last_name, user_email):
        self.id_Admin = id_Admin
        self.id_User = id_User

        # user
        self.user_username = user_username
        self.user_type = user_type
        self.user_first_name = user_first_name
        self.user_last_name = user_last_name
        self.user_email = user_email

    def __str__(self):
        return f"Admin id : {self.id_Admin}"

    def jsonify(self):
        return {
            "id_Admin": self.id_Admin,
            "id_User": self.id_User,
            "user_username": self.user_username,
            "user_type": self.user_type,
            "user_first_name": self.user_first_name,
            "user_last_name": self.user_last_name,
            "user_email": self.user_email
        }