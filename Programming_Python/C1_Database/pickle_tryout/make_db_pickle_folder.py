import pickle
from Programming_Python.CH1_Database.initdata import db 
extension='.pkl'

for (key, record) in db.items():
    filename = key+extension
    dbfile=open('db/'+filename, 'wb')
    pickle.dump(record,dbfile)

dbfile.close()

if __name__ == "__main__":
    bob  = pickle.load(open('db/bob.pkl', 'rb'))
    print(bob)