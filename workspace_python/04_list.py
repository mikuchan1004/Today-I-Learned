a = []
b = list()
print(type(a))
print(type(b))

a = [1, 2, 3]
print(a)

# range
# 전달인자 1개 : 0부터 몇개(0 ~ 바로 앞까지)
c = range(10)
print(c)
print(list(c)) 

# 전달인자 2개 : 첫 번째 부터 두 번째 바로 앞까지 
d = range(5, 12)
print(list(d))

e = range(12, 5) # []
print(list(e))

# 전달인자 3개 : 첫 번째 부터 두 번째 바로 앞까지, 세 번째씩 건너뛰면서
f = range(-4, 10, 2)
print(list(f))

a = [0, 1, 2, 3, 4, 5]
# range(6)
a = list(range(6)) 
del a[3]
print(a)

a = a + [6]
print(a)

a += [7]
print(a)

a.append(8)
print(a)

b = [9, 10]
a.append(b)
print (a)

print('-='*30)
c = [654, 156, 964, 15, 35]
c.sort() # 오름차순
print(c)
c.sort(reverse=True)
print(c)

c = c[::-1]
print(c)

c.reverse()
print(c)

c.insert(0, 100)
print(c)

c.insert(10, 200) # index를 벗어나면 걍 끝에 
print(c)

c.extend([1, 2]) # 리스트를 합쳐준다
print(c)

a = [1, 2, 3, 4, 2]
a.remove(2) # 처음 만나는 값을 찾아서 지워준다
print(a)

if 5 in a :         
    a.remove(5) # 없는 값은 에러난다

a = [1, 2, 3, 4, 2, 4]
b = a.index(2)
print(b)
# b = a.index(5) # 없는 값은 에러

c = a.count(4)
print(c)

a.reverse()
print(a)

a.clear()
print(a)
a = []

a = [1, 2, 3]
print (a[len(a):])
print(a[3:])

# a[3:] = 4
a[3:] = [4, 5, 6]
print(a)

a = [1, 2, 3, 4, 5]
b = a
print(b)
b[2] = 30
print(b)
print(a)
b = a.copy()
b[2] = 30
print(b)
print(a)

print('-=' * 30)
a = [1, 2, 3, 4, 5]
b = a.copy()
b[2] = 30
print(b)
print(a)

c = (1, 2)
a = c[0]
b = c[1]

a, b = (1,2)

a = [10, 20, 30]
for i in a:
    print(i)

# 이번 턴의 index와 value를 한번에 뽑아 줌
for index, value in enumerate(a) :
    print(index, value)

# 시작 인덱스 지정 가능
for index, value in enumerate(a, start=100) :
    print(index, value)

a = [7, 3, 5, 8, 4]
# 가장 큰 수 찾기
a.sort(reverse=True) # sort는 기본적으로 오름차순인데, reverse=True를 하면 내림차순으로!
print(a[0]) # 내림차순으로 하면 리스트의 첫 번째 요소가 가장 큰 수가 된다.

a = [i for i in range(10)] # 0부터 9까지 숫자를 생성하여 리스트 생성
print(a)

a = [i for i in range(10) if i % 2 == 0] # 0~9 숫자 중 2의 배수(짝수)로
print(a) # 리스트 생성

a = [1.2 , 2.5 , 3.7 , 4.6 , -3.5]
for i, value in enumerate(a) :
    a[i] = int(value)
print(a)

# 두 번째 반복되는 것을 하나씩 꺼내서 
# 첫 번째 함수에 넣고 
# 결과를 배열로 만들어준다.
a = list(map(int, a))
print(a)

a = [
    [10, 20],
    [30, 40],
    [50, 60]
]
print(len(a))
print(a[1][0])