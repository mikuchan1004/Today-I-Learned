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

c = [654, 156, 964, 15, 35]
c.sort() # 오름차순
print(c)

c = c[::-1]
print(c)

c.reverse()
print(c)

c.insert(0, 100)
print(c)

c.insert(10, 200) # index를 벗어나면 걍 끝에 
print(c)