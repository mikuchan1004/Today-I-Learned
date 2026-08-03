
class Person : 
    def greeting(self) :
        print('Hello Class')
        
    def hello(self) :
        self.greeting()

james = Person()
james.greeting()

print(james)
print(type(james))