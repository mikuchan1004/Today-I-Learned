
a = [0, 10, 20, 30, 40]
print (20 in a)
print (200 in a)
print(not(200 in a))
print (200 not in a)

a = [1,2,3]
b = [4,5,6]
c = a + b
print (c)

a = 'hello'
b = 'world'
c = a + b
print (c)

# c = a + 3
# print (c)

c = a + str(3)
print (c)

print ('-' * 10)

print (len(a))

hello = '안녕하세요'
b = hello.encode('utf-8')
print (len(b))
print (hello[0])

a = [1,2,3,4]
print(a[0])
print(a[-2])

# print(a[100]) # IndexError

a = (1,2,3)
print (a[0])
# a[0] = 3 # 튜플의 값은 바꿀 수 없다.

a = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
print(a[1:4])
print(a[4:-1])
print(a[4:100]) # 범위를 벗어나도 에러 없음

print(a[1:9:2])

print(a[:7])
print(a[5:])
print(a[:])

print(a[7:3])
print(a[7:3:-1])

print(a[-4:8])
print(a[-4:-2])

print(a)
a[2:5] = ['a' , 'b' , 'c']
print(a)

print(a[2:5])
a[2:5] = [10, 20, 30, 40, 50]
print(a)

ko = ['책' , '알약' , '철판']
en = ['book' , 'pill' , 'plate']

view = ko
view = en

print(view[0])

a = 'hello'

print (a[5::-1])