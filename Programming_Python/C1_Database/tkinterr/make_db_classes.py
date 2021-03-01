import shelve
from person_start import Person, Manager
shelveFile = 'class-shelve'

if __name__ == "__main__":
        
    bob = Person('Bob Smith', 40, 'software', 30000)
    sue = Person('Sue Jones', 44, 'hardware', 40000)
    tom = Manager('Tom Cruse', 39, 54000)
    edgar = Manager('Edgar Allan Po', 55, 70000)

    db = shelve.open(shelveFile)
    db['bob'] = bob
    db['sue'] = sue
    db['tom'] = tom
    db['edgar'] = edgar
    db.close()

