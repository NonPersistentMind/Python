class Group:
    groups = []

    def __init__(self, name, size):
        self.name = name
        self.size = size

    def __str__(self):
        return "Group: " + self.name + " (" + str(self.size) + " persons)"

    def __repr__(self):
        return "Group: " + self.name + " (" + str(self.size) + " persons)"

    @staticmethod
    def get_id(name):
        for i in range(len(Group.groups)):
            if Group.groups[i].name == name:
                return i
        return -1
