import random
import time

from pprint import pprint

from Professor import Professor
from Room import Room
from Slot import Slot
from Group import Group
from Course import Course

from simpleai.search import CspProblem, backtrack, min_conflicts, MOST_CONSTRAINED_VARIABLE, HIGHEST_DEGREE_VARIABLE, \
    LEAST_CONSTRAINING_VALUE

Group.groups = [
    Group("MI-4", 23),
    Group("TK-4", 12),
    Group("TTP-42", 25),
    Group("MI-3", 18),
    Group("K-26", 20)
]

Professor.professors = [
    Professor("Taranukha"),
    Professor("Fedorus"),
    Professor("Hlybovets"),
    Professor("Radyvonenko"),
    Professor("Bugayov"),
    Professor("Ryabokon"),
    Professor("Kulyabko"),
    Professor("Zavadsky"),
    Professor("Tereschchenko"),
    Professor("Tymashoff"),
    Professor("Vergunova"),
    Professor("Panchenko"),
    Professor("Pashko"),
    Professor("Fedorova"),
    Professor("Kuzenko"),
    Professor("Letychevsky")
]

Room.rooms = [
    Room("202", 20, is_lab=True),
    Room("203", 20, is_lab=True),
    Room("204", 18, is_lab=True),
    Room("205", 18, is_lab=True),
    Room("206", 18, is_lab=True),
    Room("231", 25, is_lab=True),
    Room("232", 25, is_lab=True),
    Room("233", 25, is_lab=True),
    Room("234", 25, is_lab=True),
    Room("221", 60, is_lab=False),
    Room("222", 20, is_lab=True),
    Room("302", 30, is_lab=False),
    Room("303", 30, is_lab=False),
    Room("304", 30, is_lab=False),
    Room("305", 30, is_lab=False),
    Room("306", 30, is_lab=False),
    Room("307", 30, is_lab=False),
    Room("308", 30, is_lab=False),
    Room("309", 30, is_lab=False),
    Room("310", 30, is_lab=False),
    Room("39", 120, is_lab=False),
    Room("43", 120, is_lab=False),
    Room("42", 60, is_lab=False),
    Room("40", 60, is_lab=False),
    Room("704", 35, is_lab=False),
    Room("705", 18, is_lab=True)
]

Course.courses = [
    Course("Intelligence Systems", ["MI-4", "TK-4", "TTP-42"], "Hlybovets", ["Taranukha", "Fedorus", "Bugayov"]),
    Course("Machine Learning", ["MI-4"], "Radyvonenko"),
    Course("Image Recognition", ["MI-4"], "Ryabokon"),
    Course("Refactoring Problems", ["MI-4"], "Kulyabko"),
    Course("Management", ["MI-4", "TK-4", "TTP-42"], "Tymashoff", ["Vergunova"]),
    Course("Algorithms", ["K-26"], "Zavadsky", ["Taranukha", "Zavadsky"]),
    Course("DBMS", ["K-26"], "Kulyabko", ["Kulyabko", "Taranukha", "Zavadsky"]),
    Course("Computational Geometry", ["MI-3"], "Tereschenko", ["Tereschenko"]),
    Course("Quantum Computation", ["MI-3"], "Zavadsky"),
    Course("Operating Systems", ["MI-3"], "Panchenko", ["Panchenko", "Fedorova"]),
    Course("QA", ["TTP-42"], "Kuzenko", ["Kuzenko", "Fedorova"]),
    Course("Programming Paradigms", ["TK-4"], "Letychevsky", ["Pashko"])
]

Slot.slots = [
    Slot("08:40", "10:15", "Mon"),
    Slot("10:35", "12:10", "Mon"),
    Slot("12:20", "13:55", "Mon"),
    Slot("08:40", "10:15", "Tue"),
    Slot("10:35", "12:10", "Tue"),
    Slot("12:20", "13:55", "Tue"),
    Slot("08:40", "10:15", "Wed"),
    Slot("10:35", "12:10", "Wed"),
    Slot("12:20", "13:55", "Wed"),
    Slot("08:40", "10:15", "Thu"),
    Slot("10:35", "12:10", "Thu"),
    Slot("12:20", "13:55", "Thu"),
    Slot("08:40", "10:15", "Fri"),
    Slot("10:35", "12:10", "Fri"),
    Slot("12:20", "13:55", "Fri"),
]

variables = []  # (course, lecture/practice, professor, groups
for course in Course.courses:
    variables.append((course, 0, course.lecturer, tuple(course.groups)))
    if course.trainers:
        for group in course.groups:
            variables.append((course, 1, random.choice(course.trainers), tuple([group])))
variables = {i: variables[i] for i in range(len(variables))}

values = []  # (slot, room)
for slot in Slot.slots:
    for room in Room.rooms:
        values.append((slot, room))

domains = {}
for key, var in variables.items():
    domains[key] = []
    for j in range(len(values)):
        slot, room = values[j]
        if room.size >= sum(Group.groups[Group.get_id(group)].size for group in var[3]) \
                and room.is_lab == var[1]:
            domains[key].append(j)
    random.shuffle(domains[key])

def pretty_print(schedule, variables, values):
    by_group = {group.name: [] for group in Group.groups}
    for key_sch, value_sch in schedule.items():
        key_sch = variables[key_sch]
        value_sch = values[value_sch]
        for group in key_sch[3]:
            by_group[group].append({'course': key_sch[0],
                                    'is_lab': key_sch[1],
                                    'professor': key_sch[2],
                                    'slot': value_sch[0],
                                    'room': value_sch[1]})

    for key, values in by_group.items():
        print('----------> {}'.format(key))
        for slot in sorted(Slot.slots):
            for gr_value in values:
                if gr_value['slot'] == slot:
                    print("|-> {}: {}, {} ({}) ({})".format(gr_value['slot'], gr_value['course'],
                                                            gr_value['professor'], gr_value['room'],
                                                            'P' if gr_value['is_lab'] else 'L'))
        print("---------->\n")


def const_different(_variables, _values):
    if _values[0] == _values[1]:
        return False
    if values[_values[0]][0] == values[_values[1]][0]:
        if set(variables[_variables[0]][3]).intersection(set(variables[_variables[1]][3])):
            return False
        elif (variables[_variables[0]][2] == variables[_variables[1]][2]):
            return False
    return True

constraints = [
    ((i, j), const_different) for i in range(len(variables)) for j in range(i, len(variables)) if i != j

]

my_problem = CspProblem(variables.keys(), domains, constraints)

t1 = time.time()
res = backtrack(my_problem, variable_heuristic=MOST_CONSTRAINED_VARIABLE)
print('\n\n\n\nMinimum remaining value: {}s'.format(time.time() - t1))
pretty_print(res, variables, values)

t1 = time.time()
res = backtrack(my_problem, variable_heuristic=HIGHEST_DEGREE_VARIABLE)
print('\n\n\n\nDegree heuristic: {}s'.format(time.time() - t1))
pretty_print(res, variables, values)

t1 = time.time()
res = backtrack(my_problem, value_heuristic=LEAST_CONSTRAINING_VALUE)
print('\n\n\n\nLeast constraining value: {}s'.format(time.time() - t1))
pretty_print(res, variables, values)

t1 = time.time()
res = min_conflicts(my_problem)
print('\n\n\n\nForward checking: {}s'.format(time.time() - t1))
pretty_print(res, variables, values)

t1 = time.time()
res = result = backtrack(my_problem, inference=False)
print('\n\n\n\nConstraint propagation: {}s'.format(time.time() - t1))
pretty_print(res, variables, values)

