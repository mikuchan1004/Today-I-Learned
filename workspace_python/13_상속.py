class Person:
    def __init__(self):
        self.hello = '안녕'

    def greeting(self):
        print('안녕하세요.')

class Student(Person) :
    def __init__(self):
        super().__init__()

    def study(self):
        print('공부하기')
        self.greeting()
        print(self.hello)

s1 = Student()
s1.study()
s1.greeting()

class Person2 :
    def __init__(self):
        print('Person2 __init__ 실행')
        self.hello = '안녕'

class Student2(Person2) :
    def __init__(self):
        print('Student2 __init__ 실행')
        super().__init__()
        self.school = '휴먼'

s2 = Student2()
print(s2.school)
print(s2.hello)

class Student3(Person2):
   def test(self):
       print('테스트')
print('-' * 30)
a = Student3()

class Person3 :
    # 기본 생성자의 
    # super의 __init__ 전달 인자는 없으므로
    # 전달 인자가 필수인 경우 생략 불가능

    def __init__(self, str):
        print('Person3 __init__ 실행')
        self.hello = '안녕'
        self.str = str

class Student4(Person3):
    def __init__(self) :
        super().__init__(None)
    
s4 = Student4()
print(s4.hello)


class Person5:
    def hi(self):
        print('안녕하시오')

class Student5(Person5):
    def hi(self):
        print('야호')

s5 = Student5()
s5.hi()

class Champ:
    def attack(self):
        print('기본 공격')

class Lux(Champ) :
    def attack(self):
        super().attack()
        print('데마시~~~~~~~~아!!!')

class Jax(Champ):
    def defence(self):
        print('절대 지켜')

c1 = Lux()
c2 = Jax()
cList = [c1, c2]

for c in cList:
    c.attack()

# 문제4 메서드 오버라이딩
'''
부모 Car 클래스가 있음 
def start(self)
    print('시동을 켭니다')
def accel(self)
    print('속도를 높입니다')

자식 람보르기니

시동걸면 "바랑~"
액셀을 밟으면 "스~아~앙"

자식 티코

액셀을 밟으면 "부다다당"

'''

# 부모 Car 클래스 생성

class Car:
    def start(self):
        print('시동을 켭니다')

    def accel(self):
        print('속도를 높입니다')

class Lambo(Car) :
    def start(self):
        super().start()
        print('바랑')

    def accel(self):
        super().accel()
        print('스~아~앙')

class Tico(Car):
    def accel(self):
        super().accel()
        print('부다다당')

car1 = Lambo()
car2 = Tico()
car1.start()
car1.accel()
car2.accel()