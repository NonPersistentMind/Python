class Course:
    courses = []

    def __init__(self, name, groups: list, lecturer, trainers=None):
        self.name = name
        self.groups = groups
        self.lecturer = lecturer
        self.trainers = trainers

    def __str__(self):
        return "Course: " + self.name

    def __repr__(self):
        return "Course: " + self.name

    @staticmethod
    def get_id(self, name):
        for i in range(len(Course.courses)):
            if Course.courses[i].name == name:
                return i
        return -1

    @staticmethod
    def add(name, groups: list, professors: list):
        Course.courses.append(Course(name, groups, professors))
