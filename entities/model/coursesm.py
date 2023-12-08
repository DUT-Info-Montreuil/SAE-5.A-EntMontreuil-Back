class CourseModel:
    def __init__(self, id, startTime, endTime, dateCourse, control, id_Resource, id_Tp, id_Td, id_Promotion, id_Teacher, id_classroom, id_Training, training_name, training_semester,
                 resource_name, tp_name, td_name, promotion_year, promotion_level, teacher_initial, classroom_name, resource_color, classroom_capacity, teacher_username):
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
        self.id_Training = id_Training

        # resource
        self.resource_name = resource_name
        self.resource_color = resource_color

        # tp
        self.tp_name = tp_name

        # td
        self.td_name = td_name

        # promotion
        self.promotion_year = promotion_year
        self.promotion_level = promotion_level
        # teacher
        self.teacher_initial = teacher_initial
        self.teacher_username = teacher_username

        # classroom
        self.classroom_name = classroom_name
        self.classroom_capacity = classroom_capacity
        
        # training
        self.training_name = training_name
        self.training_semester = training_semester

    def __str__(self):
        return f"Course id: {self.id}, startTime: {self.startTime}, endTime: {self.endTime}"

    def jsonify(self):
        return {
            "courses" : {
                "id": self.id,
                "startTime": str(self.startTime),
                "endTime": str(self.endTime),
                "dateCourse": str(self.dateCourse),
                "control": self.control
            },
            "resource" :{
                "id_Resource": self.id_Resource,
                "resource_name": self.resource_name,
                "resource_color" : self.resource_color,
            },
            "tp" : {
                "id_Tp": self.id_Tp,
                "tp_name": self.tp_name,
            },
            "td" : {
                "id_Td": self.id_Td,
                "td_name": self.td_name,
            },
            "promotion" : {
                "id_Promotion": self.id_Promotion,
                "promotion_year": self.promotion_year,
                "promotion_level" : self.promotion_level,
            },
            "teacher" : {
                "id_Teacher": self.id_Teacher,
                "teacher_initial": self.teacher_initial,
                "teacher_username" : self.teacher_username
            },
            "classroom" : {
                "id_classroom": self.id_classroom,
                "classroom_name": self.classroom_name,
                "classroom_capacity" : self.classroom_capacity,
            },
            "training" : {
                "training_semester" : self.training_semester,
                "training_name" : self.training_name
            }            
        }
