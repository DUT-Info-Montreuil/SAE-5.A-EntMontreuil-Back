class CourseModel:
    def __init__(self, id, startTime, endTime, dateCourse, control, id_Resource, id_Tp, id_Td, id_Promotion, id_Teacher, id_classroom,
                 resource_name, tp_name, td_name, promotion_year, teacher_initial, classroom_name, resource_color):
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
        self.id_classroom = id_classroom

        # resource
        self.resource_name = resource_name
        self.resource_color = resource_color

        # tp
        self.tp_name = tp_name

        # td
        self.td_name = td_name

        # promotion
        self.promotion_year = promotion_year

        # teacher
        self.teacher_initial = teacher_initial

        # classroom
        self.classroom_name = classroom_name

    def __str__(self):
        return f"Course id: {self.id}, startTime: {self.startTime}, endTime: {self.endTime}"

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
            "id_Teacher": self.id_Teacher,
            "id_classroom": self.id_classroom,
            "resource_name": self.resource_name,
            "tp_name": self.tp_name,
            "td_name": self.td_name,
            "promotion_year": self.promotion_year,
            "teacher_initial": self.teacher_initial,
            "classroom_name": self.classroom_name,
            "resource_color" : self.resource_color
        }
