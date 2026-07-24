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