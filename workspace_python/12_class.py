
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

class Knotted:

    brand = '노티드-디저트맛집'

    def __init__(self, name, addr):
        # self.brand = '노티드-디저트맛집'
        self.name = name
        self.addr = addr
    def info(self):
        print(self.name)

k1 =  Knotted('천안점' , '천안')
k2 = Knotted('아산점' , '아산')

print(k1.name, k1.brand)
print(k2.name, k2.brand)

print(k1.name, Knotted.brand)
print(k2.name, Knotted.brand)

class Calc :
    PI = 3.141592

    def __init__(self):
        self.meat = 200

    @staticmethod
    def add(x, y) :
        return x + y

    def plus(self, x, y) :
       Calc.add(x, y) 

print(Calc.add(1,2) * Calc.PI)

class Person4:
    count = 0

    def __init__(self):
        Person4.count += 1

    @classmethod
    def print_count(cls) :
        print(f'{Person4.count}명 생성됨')

p1 = Person4()
p2 = Person4()
p3 = Person4()
Person4.print_count()

'''
문제1
멜론 차트 관리 시스템
모든 곡을 리스트로 관리
한 곡에 해당하는 클래스부터 만들자
- 제목, 가수명, 앨범명, 가사

두 곡 이상 정보를 저장
각 곡의 '제목-가수명'을 출력
'''

# 먼저 한 곡에 해당하는 클래스를 만들어보자 

class Melon_chart:

    def __init__(self, title, singer, album_name, lyrics):
        self.title = title # 제목
        self.singer = singer # 가수명
        self.album_name = album_name # 앨범명
        self.lyrics = lyrics # 가사 (가사를 전부 긁어올수는 없으니까 딱 한 줄만)

first_sing = Melon_chart('LOVE ATTACK' , 'RESCENE' , 'SCENEDROME' , 'Feeling love attack...')
second_sing = Melon_chart('갑자기' , '아이오아이(I.O.I)' ,'I.O.I 3rd MINI ALBUM[I.O.I : LOOP]' , '어쩌면 잘된 일이야, 빨간 노을빛처럼...')

melon_chart = [first_sing, second_sing]
for list in melon_chart :
    print(f'{list.title} - {list.singer}')

'''
문제2
휴먼잡스 계정 관리 시스템
내 계정에는 id, pw, 주소가 있다
모두 접근 제한된 private 변수입니다.

메소드를 이용해서 주소를 변경하거나
주소를 return하는 메소드를 만들기
'''

class HumanJobs :

    def __init__(self):
        self.__id = ''
        self.__pw = ''
        self.__address = ''

    def setAddr(self, address):
        self.__address = address

    def getAddr(self):
        return self.__address

h1 = HumanJobs()
h1.setAddr('천안')
h1_addr = h1.getAddr()
print(h1_addr)

'''
문제3
디저트 카페 노티드 창업을 위한 클래스
 - 상호, 자본금이 필수 요소

노티드를 두군데에 창업할 것이다.
하나를 창업할 때 필수 요소를 꼭 넣어야 생성되도록 만드세요
'''

class Knotted2 :
    def __init__(self, brand, account) :
        self.brand = brand
        self.account = account

shop1 = Knotted2('노티드 천안점', 1500000 )
shop2 = Knotted2('노티드 아산점', 1500000 )

print(shop1.brand , shop1.account)
print(shop2.brand , shop2.account)

class Melon :
    def __init__(self) :
        self.songList = []

    def appendSong(self, song) :
        self.songList.append(song)

m = Melon()
m.appendSong(first_sing)