import shelve
db = shelve.open('people-shelve')

for key in db:
    print(key, '=>\n', db[key])