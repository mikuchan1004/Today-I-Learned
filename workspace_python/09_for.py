for i in range(5) :
    print(i, end=' ')
print()
for i in reversed(range(5)) :
    print(i, end=' ')

# 구구단을 출력해보자
num = 2 # 먼저 2단부터
for i in range(1, 10) : # 1부터 10까지 반복
    print(num , '*' , i , '=' , num * i) 

num = 3
for i in range(1, 10) : 
    print(num, '*' , i , '=' , num * i )

num = 4
for i in range(1, 10) : 
    print(num, '*' , i , '=' , num * i )

print('-' * 8)

for k in range(2, 10):
    print(k ,'단')
    for i in range(1, 10) : 
        print(k, '*' , i , '=' , k * i )

print('-' * 8)

# 구구단을 3단씩 쪼개서 나열해보자
k = 9
for i in range(2, k+1, 3):
    for j in range(1, 9+1) :
        for m in range(3) :
            if i+m <= k:
                print(f'{i+m}x{j}={(i+m)*j}' , end = '\t')
        print()
    print()

import random
print(random.random())
print(random.randint(1, 6))

# 주사위 3이 몇번만에 나오는지 출력
dice = -1
count = 0
while dice != 3:
    dice = random.randint(1, 6)
    count += 1
    if dice == 3 :
        print(count)
