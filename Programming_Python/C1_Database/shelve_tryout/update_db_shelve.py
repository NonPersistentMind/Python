import shelve
db = shelve.open('people-shelve', writeback=True)

sue  = db['sue']
sue['pay'] *= 1.13
# db['sue'] = sue
 
db.close()