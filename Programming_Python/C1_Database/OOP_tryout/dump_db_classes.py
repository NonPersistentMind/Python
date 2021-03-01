import shelve
from make_db_classes import shelveFile
db = shelve.open(shelveFile)

for name in db:
    print(name, '=>\n', db[name])