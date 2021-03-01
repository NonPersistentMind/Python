ENDREC = '%%ENDREC%%'
RECSEP = ' => '
db_filename = 'people-db'

def storeDbase(db, file_name = db_filename):
    """
    Assuming db is a dictionary of dictionaries, also that it has no values equal to '%%ENDREC%%' or ' => '
    """
    file = open(file_name, 'w')
    for name in db:
        print(name, file = file)
        for (key, value) in db[name].items():
            print(key, RECSEP, repr(value), file=file, sep='')
    file.close()

def loadDbase(file_name = db_filename):
    file = open(file_name)
    db = {}
    record = {}
    name = ''
    for line in file:
        if RECSEP in line:
            key, value = line.split(RECSEP)
            record[key] = eval(value)
        else:
            if name:
                old_name = name
                name = line.strip()
                db[old_name] = record
                record = {}
            else:
                name = line.strip()
    else:
        db[name] = record

    return db 



if __name__ == "__main__":
    from initdata import db
    storeDbase(db)
    print(loadDbase(db_filename))