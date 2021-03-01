ff = open('/dev/tty')
print('Tell me something')
print(ff.readline()[:-1])