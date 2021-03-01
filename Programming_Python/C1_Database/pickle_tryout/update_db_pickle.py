import pickle
filename='pickle-pickle'
dbfile = open(filename, 'rb')

db = pickle.load(dbfile)
dbfile.close()

db['sue']['pay']*=1.2

dbfile=open(filename, 'wb')
pickle.dump(db, dbfile)
