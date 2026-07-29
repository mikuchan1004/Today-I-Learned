'''
문제1
numbers = [3, 7, 10, 15, 22, 8, 13]
문제1-1 : 짝수만 따로 리스트로 만들어서 출력
문제1-2 : 홀수의 합

'''
numbers = [3, 7, 10, 15, 22, 8, 13]

a = [ i for i in numbers if i % 2 == 0]
print(a) # [10, 22, 8]

b = [i for i in numbers if i % 2 == 1]
print(b) # [3, 7, 15, 13]
c = sum(b)
print(c) # 38

'''
문제 2
cart = {
    '사과': {
        '가격': 1000,
        '개수': 3
    },
    '바나나': {
        '가격': 2000,
        '개수': 4
    },
    '복숭아': {
        '가격': 1500,
        '개수': 2
    },
    '키위': {
        '가격': 2200,
        '개수': 5
    }
}
다 샀을 때 가격은?

'''
cart = {
    '사과': {
        '가격': 1000,
        '개수': 3
    },
    '바나나': {
        '가격': 2000,
        '개수': 4
    },
    '복숭아': {
        '가격': 1500,
        '개수': 2
    },
    '키위': {
        '가격': 2200,
        '개수': 5
    }
}

apple_price = cart.get('사과').get('가격')
apple_count = cart.get('사과').get('개수')
apple_totalPrice = cart['사과']['가격'] * cart['사과']['개수']
a = apple_totalPrice # 사과의 총 가격 
banana_price = cart.get('바나나').get('가격')
banana_count = cart.get('바나나').get('개수')
banana_totalPrice = cart['바나나']['가격'] * cart['바나나']['개수']
b = banana_totalPrice # 바나나의 총 가격
peach_price = cart.get('복숭아').get('가격')
peach_count = cart.get('복숭아').get('개수')
peach_totalPrice = cart['복숭아']['가격'] * cart['복숭아']['개수']
c = peach_totalPrice # 복숭아의 총 가격 
kiwi_price = cart.get('키위').get('가격')
kiwi_count = cart.get('키위').get('개수')
kiwi_totalPrice = cart['키위']['가격'] * cart['키위']['개수']
d = kiwi_totalPrice # 키위의 총 가격 
print('사과의 총 가격 :' , a , '원')
print('바나나의 총 가격 :' , b , '원')
print('복숭아의 총 가격 :' , c , '원')
print('키위의 총 가격 :' , d , '원')

cart_totalPrice = a + b + c + d

print('다 샀을 때의 가격은? : ' , cart_totalPrice , '원')

'''
문제3
UP/DOWN 게임 만들기
단, 맞추면 몇번째에 맞췄는지도 출력
'''
import random

correct_answer = random.randint(1, 99) # 정답 숫자는 랜덤으로 생성

user_input = '' # 입력받은 숫자를 정답과 비교하기 위해 만든 변수

count = 0 # 시도 횟수 저장 변수

# 답을 맞출때까지 계속 돌아야 하기 때문에, while문을 사용.

while True: # 답을 맞출때까지 계속 실행! 
    user_input = int(input('1~99 사이의 정수를 입력해주세요 : '))
    count += 1 # 시도할때마다 횟수가 1씩 증가

    if correct_answer > user_input :
        print('입력하신 숫자가 정답보다 작습니다')
    elif correct_answer < user_input :
        print('입력하신 숫자가 정답보다 큽니다')
    else :
        print('축하합니다! 정답을 맞추셨습니다. 시도 하신 횟수는 : ' , count , '회 입니다.')
        break
'''
문제4
users = {
    "admin": "1234",
    "guest": "guest",
    "user1": "abcd"
}
이런 경우 
id/pw를 입력 받거나 변수에 넣어두고
id/pw가 맞는지 틀리는지 판단해서
"아이디가 없습니다", "비번이 틀립니다", "로그인 성공"

'''
users = {
    "admin": "1234",
    "guest": "guest",
    "user1": "abcd"
}

# 성공할 때까지 무한 반복을 해야하니까 While문!

while True:
    user_id = input('아이디를 입력해주세요 : ')
    user_pw = input('비밀번호를 입력해주세요 :')

    # 아이디가 딕셔너리의 키 중에 없는 경우에는..
    if user_id not in users:
        print('아이디가 없습니다')

    # 아이디는 있는데, 딕셔너리에 저장된 해당 아이디의 비밀번호가 다른 경우에는..
    elif users[user_id] != user_pw:
        print('비번이 틀립니다')

    # 아이디도 있고, 비밀번호가 맞으면
    else : 
        print('로그인 성공')
        break # 로그인 성공했으니까 While문 종료!

'''
문제5
랜덤 투표 시스템
한번에 a, b, c 대상에 랜덤으로 투표
문제5-1 : 100번의 투표 결과를 출력하시오
문제5-2 : 그 중 가장 득표 많은 사람의 이름과 득표 수 출력

'''

