class Commentary:
    def __init__(self, id, id_User, id_Degree, date, title, comment_text, modification_date):
        self.id = id
        self.id_User = id_User
        self.id_Degree = id_Degree
        self.date = date
        self.title = title
        self.comment_text = comment_text
        self.modification_date = modification_date

    def __str__(self):
        return f"Commentary id: {self.id}, id_User: {self.id_User}"

    def jsonify(self):
        return {
            "id": self.id,
            "id_User": self.id_User,
            "id_Degree": self.id_Degree,
            "date": self.date,
            "title": self.title,
            "comment_text": self.comment_text,
            "modification_date": str(self.modification_date),
        }