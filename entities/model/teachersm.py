class TeachersModel:
    def __init__(self, id, initital, desktop, id_User, user_last_name, user_first_name, user_username, user_email, user_isAdmin):
        self.id = id
        self.initital = initital
        self.desktop = desktop
        self.id_User = id_User

        # user
        self.user_last_name = user_last_name
        self.user_first_name = user_first_name
        self.user_username = user_username
        self.user_email = user_email
        self.user_isAdmin = user_isAdmin

    def __str__(self):
        return f"Teacher id: {self.id}, initital: {self.initital}"

    def jsonify(self):
        return {
            "id": self.id,
            "initital": self.initital,
            "desktop": self.desktop,
            "id_User": self.id_User,
            "user_last_name": self.user_last_name,
            "user_first_name": self.user_first_name,
            "user_username": self.user_username,
            "user_email" : self.user_email,
            "user_isAdmin": self.user_isAdmin
        }