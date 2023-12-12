class CourseModel:
    def __init__(self, id, startTime, endTime, dateCourse, control, id_Resource,resource_name, resource_color, id_Tp, id_Td, id_Promotion, id_Training, 
                  teacher, classroom):
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
        
        # teacher
        self.teacher = teacher

        # classroom
        self.classroom = classroom
        

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
            "tp" :  self.id_Tp,
            "td" :  self.id_Td,
            "promotion" : self.id_Promotion,
            "training" : self.id_Training,
            
            "teacher" : teacher_list,
            "classroom" : classroom_list,
                   
        }
