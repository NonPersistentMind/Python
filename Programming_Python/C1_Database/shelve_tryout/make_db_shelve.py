import shelve
from Programming_Python.CH1_Database.initdata import bob, sue, tom

db = shelve.open('people-shelve')
db['bob'] = bob
db['sue'] = sue
db['tom'] = tom
db.close()

