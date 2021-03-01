import pickle
from Programming_Python.CH1_Database.initdata import db 
dbfile = open('pickle-pickle', 'wb')
pickle.dump(db,dbfile)
dbfile.close()