class Room:
    rooms = []

    def __init__(self, name, size, is_prac=False):
        self.name = name
        self.size = size
        self.is_prac = is_prac

    def __str__(self):
        return "Room: " + str(self.name) + " (size: " + str(self.size) + ")"

    def __repr__(self):
        return "Room: " + str(self.name) + " (size: " + str(self.size) + ")"
