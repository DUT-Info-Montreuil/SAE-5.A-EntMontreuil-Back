
class CommentaryModel:
    def __init__(self, id, id_Teacher, teacher_initial, id_Course, comment_text, modification_date):
        self.id = id
        self.id_Teacher = id_Teacher
        self.teacher_initial = teacher_initial
        self.id_Course = id_Course
        self.comment_text = comment_text
        self.modification_date = modification_date

    def __str__(self):
        return f"Commentary id: {self.id}, id_Teacher: {self.id_Teacher}"

    def jsonify(self):
        return {
            "commentary": {
                "id": self.id,
                "teacher": {
                    "id": self.id_Teacher,
                    "initial": self.teacher_initial,
                },
                "id_Course": self.id_Course,
                "comment_text": self.comment_text,
                "modification_date": str(self.modification_date),
            }
        }