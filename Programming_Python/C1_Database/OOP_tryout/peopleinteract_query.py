import shelve
import make_db_classes
db = shelve.open(make_db_classes.shelveFile)

fieldnames = ('name', 'age', 'job', 'pay')
max_fieldLen = max(len(f) for f in fieldnames)

while True:
    key = input('\nKey: ')
    if not key:
        break
    try:
        record = db[key]
    except:
        print('Key "%s" was not found!' % key)
    else:
        print(key)
        for field in fieldnames:
            print(' '*max_fieldLen, field.ljust(max_fieldLen), '=>', getattr(db[key], field))


