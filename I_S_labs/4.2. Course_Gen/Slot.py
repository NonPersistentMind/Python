class Slot:
    slots = []

    def __init__(self, start, end, day):
        self.start = start
        self.end = end
        self.day = day

    def __str__(self):
        return self.start + " - " + self.end + " (" + self.day + ")"

    def __repr__(self):
        return self.start + " - " + self.end + " (" + self.day + ")"

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
    def add(start, end, day):
        Slot.slots.append(Slot(start, end, day))
