def scanner(name, function):
    file = open(name, 'r')
    for line in file:
        function(line)
    file.close()

