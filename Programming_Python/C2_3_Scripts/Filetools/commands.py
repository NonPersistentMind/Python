from sys import argv
from scanfile import scanner
class UnknownCommand(Exception): pass

def processLine(line):
    commands={'+':'Mr.', '*':'Ms.'}
    try:
        print(commands[line[0]], line[1:-1])
    except KeyError:
        raise UnknownCommand(line)

filename = 'data.txt'
if len(argv) == 2 : filename = argv[1]
scanner(filename, processLine)
