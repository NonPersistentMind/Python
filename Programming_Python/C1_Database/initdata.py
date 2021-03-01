# import pprint
# =================================== Records ====================================
bob = dict(name="Bob Smith", age=40, job='dev', pay=30000)
sue = dict(name = 'Sue Jones', age = 45, pay=40000, job= 'hdw')
tom = dict(name='Tom', age=30, pay=0, job = None)

# =================================== DataBase ===================================
db = {}
db['bob'] = bob
db['sue'] = sue
db['tom'] = tom

# =================================== Testing ====================================
if __name__ == "__main__":
    for name in db:
        print(name, ' =>\n', db[name])
