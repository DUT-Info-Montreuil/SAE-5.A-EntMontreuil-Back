class Settings:
    def __init__(self, id_user, notification_mail, notification_website):
        self.id_user = id_user
        self.notification_mail = notification_mail
        self.notification_website = notification_website

    def __str__(self):
            return f"Settings for user: {self.id_user}, notification_mail: {self.notification_mail}, notification_website: {self.notification_website}"  
    
    def jsonify(self):
        return {
            "id_User": self.id_user,
            "notification_mail": self.notification_mail,
            "notification_website": self.notification_website
        }