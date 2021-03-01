class Course:
    courses = []

    def __init__(self, name, groups: list, lecturer=None, practical_teachers=None):
        self.name = name
        self.groups = groups
        self.lecturer = lecturer
        self.practical_teachers = practical_teachers

    def __str__(self):
        return "Course: " + self.name

    def __repr__(self):
        return "Course: " + self.name
