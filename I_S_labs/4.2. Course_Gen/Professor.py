class Professor:
    professors = []

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "Professor: " + self.name

    def __repr__(self):
        return "Professor: " + self.name
