class Courses:
    def __init__(self, id, startTime, endTime, dateCourse, control, id_Resource, id_Tp, id_Td, id_Promotion, id_Teacher):
        self.id = id
        self.startTime = startTime
        self.endTime = endTime
        self.dateCourse = dateCourse
        self.control = control
        self.id_Resource = id_Resource
        self.id_Tp = id_Tp
        self.id_Td = id_Td
        self.id_Promotion = id_Promotion
        self.id_Teacher = id_Teacher

    def __str__(self):
        return f"Course id: {self.id}, start time: {self.startTime}, end time: {self.endTime}"

    def jsonify(self):
        return {
            "id": self.id,
            "startTime": str(self.startTime),
            "endTime": str(self.endTime),
            "dateCourse": str(self.dateCourse),
            "control": self.control,
            "id_Resource": self.id_Resource,
            "id_Tp": self.id_Tp,
            "id_Td": self.id_Td,
            "id_Promotion": self.id_Promotion,
            "id_Teacher": self.id_Teacher
        }