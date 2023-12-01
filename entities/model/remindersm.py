class ReminderModel:
    def __init__(self, id, id_User, user_username, reminder_text, reminder_date):
        self.id = id
        self.id_User = id_User
        self.user_username = user_username
        self.reminder_text = reminder_text
        self.reminder_date = reminder_date

    def __str__(self):
        return f"Reminder id: {self.id}, id_User: {self.id_User}"

    def jsonify(self):
        return {
            "reminder": {
                "id": self.id,
                "user": {
                    "id": self.id_User,
                    "username": self.user_username,
                },
                "reminder_text": self.reminder_text,
                "reminder_date": str(self.reminder_date),
            }
        }