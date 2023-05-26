# class SupMain:
#     # def __init__(self) -> None:
#     #     print("Main constructor")
#     #     print(super())
        
#     def some_method(self):
#         print("Sup Main method")
        
#     def other_method(self):
#         print("Sup Main")
        

# class Sup1(SupMain):
#     # def __init__(self):
#     #     print('Sup1 constructor')
#     #     print(super())
#     #     super().__init__()
    
#     def some_method(self):
#         print("Sup1 method")
#         super().some_method()
        
# class Sup2(SupMain):
#     # def __init__(self):
#     #     print('Sup2 constructor')
#     #     print(super())
#     #     super().__init__()
        
#     def other_method(self):
#         print("Sup2 method")
#         super().other_method()
        
# class Sub(Sup1, Sup2):
#     def some_method(self):
#         super().some_method(), super().other_method()

# print(Sub.__bases__)
# print(Sub.__mro__)

# Sub().some_method()

class aClass:
    def __getattribute__(self, __name: str):
        print("Someone forced me to use", __name)
    def __add__(self,other):
        print("Someone forced me to add")

c1, c2 = aClass(), aClass()
c1+c2
c1.oh
    
