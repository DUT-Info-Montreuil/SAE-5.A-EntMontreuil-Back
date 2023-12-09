class CourseModel:
    def __init__(self, id, startTime, endTime, dateCourse, control, id_Resource, id_Tp, id_Td, id_Promotion, id_Training, training_name, training_semester,
                 resource_name, tp_name, td_name, promotion_year, promotion_level, resource_color, teacher, classroom):
        self.id = id
        self.startTime = startTime
        self.endTime = endTime
        self.dateCourse = dateCourse
        self.control = control
        self.id_Resource = id_Resource
        self.id_Tp = id_Tp
        self.id_Td = id_Td
        self.id_Promotion = id_Promotion
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
        self.teacher = teacher

        # classroom
        self.classroom = classroom
        
        # training
        self.training_name = training_name
        self.training_semester = training_semester

    def __str__(self):
        return f"Course id: {self.id}, startTime: {self.startTime}, endTime: {self.endTime}"

    def jsonify(self):
        teacher_list=[]
        for t in self.teacher :
            teacher_list.append({
                "id" : t["id"],
                "first_name" : t["first_name"],
                "last_name" : t["last_name"],
                "username" : t["username"],
                "initial" : t["initial"]
            })
        classroom_list=[]
        for c in self.classroom :
            classroom_list.append({
                "id" : c["id"],
                "name" : c["name"],
                "capacity" : c["capacity"]
            })
        return {
            "courses" : {
                "id": self.id,
                "startTime": str(self.startTime),
                "endTime": str(self.endTime),
                "dateCourse": str(self.dateCourse),
                "control": self.control
            },
            "resource" :{
                "id": self.id_Resource,
                "name": self.resource_name,
                "color" : self.resource_color,
            },
            "tp" : {
                "id": self.id_Tp,
                "name": self.tp_name,
            },
            "td" : {
                "id": self.id_Td,
                "name": self.td_name,
            },
            "promotion" : {
                "id": self.id_Promotion,
                "year": self.promotion_year,
                "level" : self.promotion_level,
            },
            "teacher" : teacher_list,
            "classroom" : classroom_list,
            "training" : {
                "id" : self.id_Training,
                "semester" : self.training_semester,
                "name" : self.training_name
            }            
        }
