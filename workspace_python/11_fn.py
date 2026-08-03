
def hello() :
    print('hello world')

hello()

def add(a, b) :
    # __doc 
    # 함수 첫줄의 주석 글씨를 출력해준다
    "a + b를 출력"
    print(a+b)
add(1,2) 
print(add.__doc__)

def add2(a, b) :
    return a+b
c = add2(1,2)
print(c)

def 아낌없이주는함수() :
    return 100

def not_ten (a) :
    if a == 10:
        return
    print(a)
b = not_ten(10)
print('b:', b)

def add_sub(a, b) :
    x = a + b
    y = a - b
    return x, y
c = add_sub(1, 2)
print(type(c) , c)
d, e = add_sub(1, 2)

# x = add_sub(1, 2, 3)

def print_numbers(a, b, c) :
    print(a)
    print(b)
    print(c)
a = [1, 2, 3]
print(*a)
print_numbers(*a)

def print_numbers2(*a) :
    print(type(a) , a)
    for b in a :
        print(b)

print_numbers2(1)
print_numbers2(1, 2, 3, 4)

def print_numbers3(c, *a) :
    print(c)
    for b in a :
        print(b)
# def print_numbers3(*a, c) : 

def minus(x, y) :
    print(x - y)

minus(5, 2)
minus(y = 5, x = 2)

x = {
    'name' : '김상우' ,
    'age' : 28
}
def info(age, name) :
    print(age, name )

info(*x) # 딕셔너리의 경우 *는 key만 추출 (.keys()와 같다)
info(**x) # key = value, key = value

def info2(**a) :
    for k , v in a.items() :
        print (k, v)
info2(**x)

def info3(name, age, addr='비공개') :
    print(name, age, addr)

info3(1, 2, 3)
info3(1, 2)


'''

def 파일출력(경로) :
    경로 안의 모든 목록 뽑아오기 
    if not folder :
        print(경로, 파일명)
    elif folder : 
        파일출력(folder)


'''

def local_var() :
    a2 = 10
    print(a2)

local_var()
# print(a2) a2는 local_var의 지역 변수라서 현 시점엔 없다.  

def ref(a) :
    a.append(4)
    return a

b = [1, 2, 3]
ref(b)
print(b)

def fn1(a) :
    return a+10
def fn2(a) :
    return a*10
c = 10
b = fn1(c) # 20
d = fn2(b) # 200
print(d)

e = fn2( fn1(c) )
print(e)

print(fn1)
# print = 2

def ten(x) :
    return x + 10

ten2 = lambda x : x + 10
print(ten2(5))
print ((lambda x : x + 10) (5))

a = ['1' , '2']
b = [int(a[0]) ,int(a[1])]
c = list(map(int, a))
print(a, b, c)

d = list(map(ten2, c))
print(d)

e = list(map(lambda x : x + 10, c))
print(e)

def square(x) :
    return x * x 

sqr = lambda x : x **2

def sum(x , y) :
    return x + y

add= lambda x, y : x + y 

info = [{
    'name' : '이름1',
    'age' : 25
} , {
    'name' : '이름2',
    'age' : 23
} , {
    'name' : '이름3',
    'age' : 30
}]

# 함수로
# 나이만 출력
def print_age (info) :
    for person in info :
        print(person['age'])
print_age(info)
# lambda로도 만들어보자
print_age2 = lambda info : [person['age'] for person in info]
print(print_age2(info))

info.sort(key  = lambda x : x['age'])
print(info)

x = 10 #  전역변수, global 변수 
def foo() :
    x = 20 # 지역변수
    print('foo 안에서 x:' , x)
foo()
print('foo 밖에서 x:' , x)

def foo2():
    print('foo2 안에서 x:' , x) # 전역 변수 읽기는 됨
foo2()

def foo3() :
    global x 
    x = 20
foo3()
print('foo3 이후에 x:' , x)

# 함수 안에서 변수 우선 순위 
'''
1. 먼저 지역 변수 찾기
2. 없으면 전역 변수 찾기
3. 없으면 에러

'''
x = 10
def test(z) :
    return  z + 2 
x = test(x)

def test2() :
    global x 
    x = x + 2

x = 10
y = 20
def test3() :
    global x , y
    x = 11
    y = 12


def A() : 
    x = 10
    y = 20

    def B() :
        x = 30
        
        def C() :
            nonlocal x, y 
            print(x)
            print(y)
        C()
    B()   
A()