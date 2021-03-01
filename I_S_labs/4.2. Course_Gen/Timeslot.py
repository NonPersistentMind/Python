class Timeslot:
    timeslots = []

    def __init__(self, start, end, day):
        self.start = start
        self.end = end
        self.day = day

    def __str__(self):
        return self.start + " - " + self.end + " (" + self.day + ")"

    def __repr__(self):
        return self.start + " - " + self.end + " (" + self.day + ")"
