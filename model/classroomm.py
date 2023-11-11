class ClassroomModel:
    def __init__(self, id, name, capacity, equipment, id_Course, course_start_time, course_end_time):
        self.id = id
        self.name = name
        self.capacity = capacity
        self.equipment = equipment
        self.id_Course = id_Course

        # course
        self.course_start_time = course_start_time
        self.course_end_time = course_end_time

    def __str__(self):
        return f"Classroom id: {self.id}, name: {self.name}"

    def jsonify(self):
        return {
            "id": self.id,
            "name": self.name,
            "capacity": self.capacity,
            "equipment": self.equipment,
            "id_Course": self.id_Course,
            "course_start_time": str(self.course_start_time),
            "course_end_time": str(self.course_end_time)
        }