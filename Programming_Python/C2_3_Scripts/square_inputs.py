#!/usr/bin/python3
print('Hi there')
while True:
    try:
        res = input('Enter a number: ')
    except EOFError:
        break
    res = int(res)
    print(res, 'is squared to', res**2)

print('Thanks for trying')
