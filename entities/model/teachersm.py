class TeachersModel:
    def __init__(self, id, initital, desktop, timetable_manager, id_User, user_last_name, user_first_name):
        self.id = id
        self.initital = initital
        self.desktop = desktop
        self.timetable_manager = timetable_manager
        self.id_User = id_User

        # user
        self.user_last_name = user_last_name
        self.user_first_name = user_first_name

    def __str__(self):
        return f"Teacher id: {self.id}, initital: {self.initital}"

    def jsonify(self):
        return {
            "id": self.id,
            "initital": self.initital,
            "desktop": self.desktop,
            "timetable_manager": self.timetable_manager,
            "id_User": self.id_User,
            "user_last_name": self.user_last_name,
            "user_first_name": self.user_first_name
        }