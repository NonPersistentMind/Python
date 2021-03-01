import pickle
dbfile = open('pickle-pickle', 'rb')
db = pickle.load(dbfile)

for key in db:
    print(key, '=> \n', db[key])