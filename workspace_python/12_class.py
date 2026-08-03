
class Person : 

    # __init__
    # 클래스가 생성될 때
    # 자동으로 먼저 실행되는 메서드
    def __init__(self):
        print(1)
        self.hello = '안녕하세요'

    def greeting(self) :
        print(self.hello)
        
    def hello(self) :
        self.greeting()

print(0)
james = Person()
print(2)
james.greeting()

print(james)
print(type(james))

class Person2 : 

    def __init__(self, name, age):
        print('__init__실행')
        self.hello = '안녕하세요'
        self.name = name
        self.age = age

    def greeting(self) :
        print(f'{self.hello}! 저는 {self.name}이고 나이는 {self.age}입니다.')

a = Person2('이름', 20)
a.greeting()
print(a.hello)
print(a.name)

b = Person2('다른 이름' , 30)
b.greeting()
print(b.name)

b.addr = '천안'
print(b.addr)

# print(a.addr)

b.__init__(1,2) # 실행 됨

class Person3 :
    def __init__(self, money):
        self.hello = '안녕하세요'
        self.__money = money

    def pay(self, price) :
        self.__money -= price
        print('남은 돈 :' , self.__money)
        self.__study()

    def __study(self) :
        print('히히 나 혼자 레벨 업')

a = Person3(10000)
a.pay(3000)
print(a.hello)
# print(a.__money) # 비공개 속성은 밖에서 접근 불가
# a.__study()

# __붙은 변수나 함수는 
# 내부에서는 접근 가능하고
# 외부로 노출되지 않는다
# 캡슐화, 은닉화
# print(a.___money) # __ + _money라서 안된다