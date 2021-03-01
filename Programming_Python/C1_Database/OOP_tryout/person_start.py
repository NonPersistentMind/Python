class Person:
    def __init__(self, name, age, job=None, pay=0):
        self.name = name
        self.job = job
        self.age = age
        self.pay = pay

    def lastname(self):
        return self.name.split()[-1]

    def giveRaise(self, percent):
        self.pay *= 1 + percent/100

    def __str__(self):
        return '<%s => %s>' % (self.__class__.__name__, self.__dict__ )


class Manager(Person):
    def __init__(self, name, age, pay):
        Person.__init__(self, name, age, job='Manager', pay=pay)

    def giveRaise(self, percent, bonus=10):
        Person.giveRaise(self, percent+bonus)



if __name__ == "__main__":
    bob = Person('Bob Smith', 40, 'software', 30000)
    sue = Person('Sue Jones', 45, 'hardware', 40000)
    tom = Manager('Tom Brilliant', 39, 44000)

    print(bob)
    print('Sue gets:', sue.pay)
    print('Tom gets:', tom.pay)
    print('==============================================')

    sue.giveRaise(20)
    tom.giveRaise(20)
    
    print('Sue gets:', sue.pay)
    print(tom)

