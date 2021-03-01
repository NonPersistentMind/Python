import shelve
from person_start import Person
import make_db_classes
db = shelve.open(make_db_classes.shelveFile)

fieldnames = ('name', 'age', 'job', 'pay')
max_fieldLen = max(len(f) for f in fieldnames)
# updater = {fieldname:}

while True:
    key = input('\nKey: ')
    if not key:
        break
    if key in db:
        record = db[key]
    else:
        print('Key "%s" was not found!' % key)

        makeNewRecord = input(
            'Do you want to create new record called "%s"' % key)
        
        if makeNewRecord.lower() == 'y':
            record = Person(name='?', age='?')
        else:
            continue

    print(key)
    for field in fieldnames:
        # print(' '*max_fieldLen, field.ljust(max_fieldLen), '=>', getattr(db[key], field))
        currentVal = getattr(record, field)
        out_str = ' '*max_fieldLen + field.ljust(max_fieldLen) + ' =>'
        print(out_str, currentVal)
        newVal = input(len(out_str)*' ' + ' new? ==> ')
        if newVal:
            try:
                newVal = eval(newVal)
            except:
                pass
            setattr(record, field, newVal)

    db[key] = record


db.close()
