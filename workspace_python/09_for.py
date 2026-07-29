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


# 산 모양으로 별 출력하기

# 계단식으로 별을 출력해보기 (오른쪽)

for i in range(5) :
    for j in range(5) :
        if j <= i:
            print('*', end='')
    print()

# 역삼각형 모양으로 별을 출력해보기 

for i in range(5):
    for j in range(5):
        if i <= j:
            print('*' , end='')
    print()

# 산 모양으로 별 출력하기

for i in range(5):
    # 먼저 빈칸을 4, 3, 2, 1, 0개 순으로 찍기
    for j in range(4 - i):
        print(' ', end='')
    # 그 다음 별을 1, 3, 5, 7, 9개 순으로 이어서 찍기
    for k in range(2 * i + 1):
        print('*' , end='')

    # 빈칸과 별을 다 찍었으니 한 줄 마무리
    print()

# FizzBuzz (책 220페이지)

for i in range(1, 101): # 1부터 100까지 100번 반복
    if i % 3 == 0 and i % 5 == 0: # 3과 5의 공배수일 때
        print('FizzBuzz') # FizzBuzz 출력
    elif i % 3 == 0 : # 3의 배수일 때 
        print('Fizz') # Fizz 출력
    elif i % 5 == 0: # 5의 배수일 때
        print('Buzz') # Buzz 출력
    else : 
        print(i) # 아무것도 해당되지 않을 때 숫자 출력


# import turtle as t
# t.shape('turtle')

# while True :
#     print(1)