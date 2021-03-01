import random
import itertools
from Professor import Professor
from Room import Room
from Timeslot import Timeslot
from Group import Group
from Course import Course

POPULATION = 25
BEST = int(POPULATION * 0.2)
MUTATION_LEVEL = 10

groups = [
    ("TTP-41", 28),
    ("TTP-42", 29),
    ("TK-4", 30),
    ("MI-4", 32),
]

professors = [
    "Tkachenko",
    "Butenko",
    "Vergunova",
    "Shishatska",
    "Hlybovets",
    "Panchenko",
    "Bugayov",
    "Fedorus",
    "Tymashov",
    "Zarembovskiy",
    "Bogdan",
    "Koval",
    "Trohymchuk",
    "Pashko",
    "Crack",
    "Derevianchenko",
    "Kuliabko",
    "Riabokon",
]

rooms = [
    ("1", 30, False),
    ("2", 30, False),
    ("3", 15, True),
    ("4", 15, True),
    ("204", 18, True),
    ("205", 18, True),
    ("232", 25, True),
    ("234", 18, True),
    ("302", 30, False),
    ("303", 30, False),
    ("304", 30, False),
    ("305", 30, False),
    ("306", 30, False),
    ("307", 30, False),
    ("308", 30, False),
    ("39", 120, False),
    ("40", 60, False),
    ("41", 60, False),
    ("42", 120, False),
]

timeslots = [
    ("08:40", "10:15"),
    ("10:35", "12:10"),
    ("12:20", "13:55")
]

days = [
    "Mon",
    "Tue",
    "Wed",
    "Thu",
    "Fri"
]

courses = [
    ("Intelligence Systems", ["MI-4", "TK-4", "TTP-41", "TTP-42"], "Hlybovets", ["Bugayov", "Fedorus"]),
    ("Management", ["MI-4", "TK-4", "TTP-41", "TTP-42"], "Tymashov", ["Vergunova"]),
    ("Telecomunication Technologies", ["MI-4", "TTP-41", "TTP-42"], "Zarembovskiy", ["Zarembovskiy"]),
    ("Specification Methods", ["TTP-41", "TTP-42"], "Shishatska", None),
    ("KPLP", ["TTP-41", "TTP-42"], "Tkachenko", ["Tkachenko"]),
    ("Business-analytics Systems", ["TTP-41", "TTP-42"], "Panchenko", ["Panchenko"]),
    ("Image Recognition", ["MI-4"], "Ryabokon", None),
    ("Refactoring Problems", ["MI-4"], None, ["Kuliabko"]),
    ("Quantum Computations Theory", ["MI-4"], "Riabokon", None),
    ("OS w/ Time Destribution", ["TK-4"], None, ["Koval"]),
    ("Machine Learning", ["TK-4"], "Trohymchuk", None),
    ("Neural Networks", ["TK-4"], "Pashko", None),
    ("PLKI", ["TK-4"], "Crack", None)
]


# [(name, capacity, is_prac)]
Group.groups = [Group(name, cap) for name, cap in groups]

Professor.professors = [Professor(name) for name in professors]
# [(name, capacity, is_prac)]

Room.rooms = [Room(name, cap, lab) for name, cap, lab in rooms]

# [(name, [groups], lecturer, [practical teacher(s)])]
Course.courses = [Course(name, groups, lect, prac) for name, groups, lect, prac in courses]

# [(start, end, day)]
Timeslot.timeslots = [Timeslot(time[0], time[1], day) for time, day in list(itertools.product(timeslots, days))]


def random_schedule():
    # {(timeslot, group): Course}
    schedule = {(timeslot, group.name): None for timeslot in Timeslot.timeslots for group in Group.groups}

    for course in Course.courses:
        if course.lecturer is not None:
            for group in course.groups:
                schedule[(randomize_timeslot(), group)] = {
                    'course': course,
                    'professor': course.lecturer,
                    'room': random.choice(Room.rooms),
                    'is_prac': False
                }

        if course.practical_teachers is not None:
            for group in course.groups:
                schedule[(randomize_timeslot(), group)] = {
                    'course': course,
                    'professor': random.choice(course.practical_teachers),
                    'room': random.choice(Room.rooms),
                    'is_prac': True
                }
    return schedule


def randomize_timeslot():
    return random.choice(Timeslot.timeslots)


def generate_schedules(n):
    return [random_schedule() for i in range(n)]


def room_overlap_penalty(schedule):
    penalty = 0
    for room in Room.rooms:
        for timeslot in Timeslot.timeslots:
            temp = sum(
                1 if schedule[(timeslot, group.name)] is not None and schedule[(timeslot, group.name)]['room'] == room
                else 0 for group in Group.groups)
            penalty += 0 if temp == 1 else temp
    return penalty


def professor_overlap_penalty(schedule):
    penalty = 0
    for professor in Professor.professors:
        for timeslot in Timeslot.timeslots:
            temp = sum(
                1 if schedule[(timeslot, group.name)] is not None and schedule[(timeslot, group.name)]['professor'] == professor
                else 0 for group in Group.groups)
            penalty += 0 if temp == 1 else temp
    return penalty


def course_overlap_penalty(schedule):
    penalty = 0
    for course in Course.courses:
        for timeslot in Timeslot.timeslots:
            temp = sum(
                1 if schedule[(timeslot, group.name)] is not None and schedule[(timeslot, group.name)]['course'] == course
                else 0 for group in Group.groups)
            penalty += 0 if temp == 1 else temp
    return penalty


def null_schedule_key_penalty(schedule):
    counts = 0
    for key, value in schedule.items():
        # this case penalty is more valuable
        counts += 10 if schedule[key] is None else 0
    return counts


def room_size_and_type_penalty(schedule):
    penalty = 0
    for key, value in schedule.items():
        _, group = key
        penalty += 1 if value is not None and Group.groups[Group.get_id(group)].size > value['room'].size else 0
        penalty += 1 if value is not None and value['is_prac'] == value['room'].is_prac else 0
    return penalty
# ***END OF PENALTY CALCULATING***


# ***FITNESS FUNCTION***
# 1 if all penalties are zero e.g perfect solution
def schedule_fitness(schedule):

    return 1 / (1 + course_overlap_penalty(schedule) + professor_overlap_penalty(schedule)
                + room_overlap_penalty(schedule) + room_size_and_type_penalty(schedule)
                + null_schedule_key_penalty(schedule))


# random mutations e.g crossbreeding between two individuals
def mutate(schedule_1, schedule_2):
    s1, s2 = schedule_1.copy(), schedule_2.copy()
    for key, _ in s1.items():

        if random.choice([True, False]) and (s1[key] is not None) and (s2[key] is not None):
            s1[key]['room'], s2[key]['room'] = s2[key]['room'], s1[key]['room']

        if random.choice([True, False]) and (s1[key] is not None) and (s2[key] is not None):
            # practical lessons can`t be for more than 1 group at a time
            if (s1[key]['is_prac'] == 0 and len(s1[key]['course'].groups) > 1) \
                    or (s2[key]['is_prac'] == 0 and len(s2[key]['course'].groups) > 1):
                continue
            else:
                s1[key]['course'], s2[key]['course'] = s2[key]['course'], s1[key]['course']
                s1[key]['professor'], s2[key]['professor'] = s2[key]['professor'],  s1[key]['professor']
                s1[key]['is_prac'], s2[key]['is_prac'] = s2[key]['is_prac'], s1[key]['is_prac']
        else:
            s1[key], s2[key] = s2[key], s1[key]
    return [s1, s2]


def mutate_with_random(schedule):
    rand_schedule = random_schedule()
    return mutate(schedule, rand_schedule)


def filterTimeslots(filteredKey, masterSlot, masterGroup):
    timeslot, group = filteredKey
    masterGroupVal = masterGroup[0]
    if timeslot == masterSlot and group != masterGroupVal:
        return True
    else:
        return False

def filterGroupTimeslotClass(filteredKey, masterSlot, masterGroup):
    timeslot, group = filteredKey
    masterGroupVal = masterGroup[0]
    if timeslot == masterSlot and group == masterGroupVal:
        return True
    else:
        return False

def filterDuplicates(key, value, masterKey, masterValue):
    if not masterValue:
        return False
    if not value:
        return False
    sameProf = value['professor'] == masterValue['professor']
    sameRoom = value['room'] == masterValue['room']
    samePractive = value['is_prac'] == masterValue['is_prac']
    if (sameProf and (not sameRoom or not samePractive)) or (sameRoom and (not sameProf or not samePractive)):
        return True
    else:
        return False

def hasDuplicates(schedule, groups):
    for group in groups.items():
        for timeslot in Timeslot.timeslots:
            sameTimeslotsOtherGroups = {k: v for k, v in schedule.items() if filterTimeslots(k, timeslot, group)}
            thisGroupTimeslotClass = {k: v for k, v in schedule.items() if filterGroupTimeslotClass(k, timeslot, group)}
            if not sameTimeslotsOtherGroups or not thisGroupTimeslotClass:
                break
            masterKey = list(thisGroupTimeslotClass.keys())[0]
            if not masterKey:
                break
            masterValue = thisGroupTimeslotClass[masterKey]
            if not masterValue:
                break
            checkSet = {k: v for k, v in sameTimeslotsOtherGroups.items() if filterDuplicates(k, v, masterKey, masterValue)}
            if len(checkSet) != 0:
                return True
    return False

def print_schedule(schedule):

    by_group = {group.name: [] for group in Group.groups}
    if hasDuplicates(schedule, by_group):
        print('Duplicates occured.')
        return

    for key, value in schedule.items():
        timeslot, group = key
        if value:
            by_group[group].append({'course': value['course'],
                                    'professor': value['professor'],
                                    'room': value['room'],
                                    'is_prac': value['is_prac'],
                                    'timeslot': timeslot})
        else:
            by_group[group].append({'course': ' ',
                                    'professor': ' ',
                                    'room': ' ',
                                    'is_prac': ' ',
                                    'timeslot': timeslot})

    for key, values in by_group.items():
        print('********{}********'.format(key))
        per_day = {day: [] for day in days}
        for value in values:
            per_day[value['timeslot'].day].append(value)
        for day in days:
            print('|---- DAY: {}'.format(day.upper()))
            for el in per_day[day]:

                if el['course'] != ' ':
                    print("|-- {} - {}: {}, {} ({}) ({})".format(el['timeslot'].start, el['timeslot'].end, el['course'],
                                                                 el['professor'], el['room'], 'P' if el['is_prac'] else 'L'))
                else:
                    print("|-- {} - {}: None".format(el['timeslot'].start, el['timeslot'].end))
        print("*******************\n\n")


def genetic_algorithm(times):
    population = generate_schedules(POPULATION)
    population = list(sorted(population, key=lambda x: schedule_fitness(x), reverse=True))

    best_individual = {
        'individual': population[0],
        'fitness': schedule_fitness(population[0])
    }

    i = 0
    while i < times:
        i += 1
        for individual in population:
            if schedule_fitness(individual) == 1:
                return individual
            if schedule_fitness(individual) > best_individual['fitness']:
                best_individual['individual'] = individual
                best_individual['fitness'] = schedule_fitness(individual)
        best_individuals = population[:BEST].copy()
        ordinary_individuals = population[BEST:POPULATION].copy()

        population = best_individuals.copy()
        for best in best_individuals:
            for ordinary in ordinary_individuals:
                population.extend(mutate(best, ordinary))
        for individual in random.sample(best_individuals + ordinary_individuals, MUTATION_LEVEL):
            population.extend(mutate_with_random(individual))
    return best_individual


if __name__ == '__main__':
        times = input("Enter number of iterations:\n")
        individual = genetic_algorithm(int(times))
        printable = individual['individual']
        print(schedule_fitness(individual['individual']))
        print_schedule(individual['individual'])
