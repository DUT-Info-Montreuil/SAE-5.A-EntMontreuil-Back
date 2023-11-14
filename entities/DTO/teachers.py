class Teachers:
    def __init__(self, id, initital, desktop, timetable_manager, id_User):
        self.id = id
        self.initital = initital
        self.desktop = desktop
        self.id_User = id_User

    def __str__(self):
            return f"Teacher id: {self.id}, initital: {self.initital}"  
    
    def jsonify(self):
        return {
            "id": self.id,
            "initital": self.initital,
            "desktop": self.desktop,
            "id_User": self.id_User
        }