class Commentary:
    def __init__(self, id, id_Teacher, id_Course, comment_text, modification_date):
        self.id = id
        self.id_Teacher = id_Teacher
        self.id_Course = id_Course
        self.comment_text = comment_text
        self.modification_date = modification_date

    def __str__(self):
        return f"Commentary id: {self.id}, id_Teacher: {self.id_Teacher}"

    def jsonify(self):
        return {
            "id": self.id,
            "id_Teacher": self.id_Teacher,
            "id_Course": self.id_Course,
            "comment_text": self.comment_text,
            "modification_date": str(self.modification_date),
        }