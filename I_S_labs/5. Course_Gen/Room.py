class Room:
    rooms = []

    def __init__(self, number, size, is_lab=False):
        self.number = number
        self.size = size
        self.is_lab = is_lab

    def __str__(self):
        return "Room: " + str(self.number) + " (size: " + str(self.size) + ")"

    def __repr__(self):
        return "Room: " + str(self.number) + " (size: " + str(self.size) + ")"

    def __eq__(self, other):
        return self.number == other.number

    @staticmethod
    def get_id(number):
        for i in range(len(Room.rooms)):
            if Room.rooms[i].number == number:
                return i
        return -1

    @staticmethod
    def add(number, size, is_lab=False):
        Room.rooms.append(Room(number, size, is_lab))
