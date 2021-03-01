class Professor:
    professors = []

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "Professor: " + self.name

    def __repr__(self):
        return "Professor: " + self.name

    def __eq__(self, other):
        return self.name == other.name

    @staticmethod
    def get_id(name):
        for i in range(len(Professor.professors)):
            if Professor.professors[i].name == name:
                return i
        return -1

    @staticmethod
    def add(name):
        Professor.professors.append(Professor(name))
