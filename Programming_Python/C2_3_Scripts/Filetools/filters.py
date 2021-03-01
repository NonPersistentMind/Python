import sys
def filter_stream(function):
    for line in sys.stdin:
        print(function(line), end='')

def filter_file(name, function):
    # file_obj = open(name, 'r')
    # output = open(name+'.out', 'w')
    with open(name, 'r') as file_obj, open(name+'.out', 'w') as output:
        for line in file_obj:
            output.write(function(line))
        output.close()
        file_obj.close()

if __name__ == "__main__":
    filter_stream(lambda line: line)
