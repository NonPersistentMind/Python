class Slot:
    slots = []

    def __init__(self, start, end, day):
        self.start = start
        self.end = end
        self.day = day

    def __str__(self):
        return "(" + self.day + "): " + self.start + " - " + self.end

    def __repr__(self):
        return "(" + self.day + "): " + self.start + " - " + self.end

    def __eq__(self, other):
        if self.day == other.day and self.start == other.start:
            return True
        return False

    def __lt__(self, other):
        if self.is_less(self.day, other.day):
            return True
        if self.is_less(other.day, self.day):
            return False
        else:
            return self.start < other.start

    @staticmethod
    def is_less(day1, day2):
        priority = {
            'Mon': 0,
            'Tue': 1,
            'Wed': 2,
            'Thu': 3,
            'Fri': 4
        }
        return priority[day1] < priority[day2]

    @staticmethod
    def get_id(slot):
        for i in range(len(Slot.slots)):
            if Slot.slots[i].day == slot.day and Slot.slots[i].start == slot.start:
                return i
        return -1

    @staticmethod
    def add(start, end, day):
        Slot.slots.append(Slot(start, end, day))
