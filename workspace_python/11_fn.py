
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
    if a2 > 3:
        print(a2)
        b2 = 5
    print(b2)

local_var()