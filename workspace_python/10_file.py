#  w : 수정 가능
file = open('hello.txt', 'w')
file.write('eng\n123\n한글')
file.flush() #  버퍼가 꽉 차지 않아도 내보내기
                       # 즉시 반영
file.close()

# 한글 캐릭터셋
# utf-8 , euc-kr, cp949
file = open('hello2.txt', 'w' , encoding='utf-8')
file.write('eng\n123\n한글')
file.close()

# r : 읽기 전용
file = open('hello.txt', 'r')
s  = file.read()
file.close()
print(s)

file = open('hello2.txt', 'r' , encoding='utf-8')
s  = file.read()
file.close()
print(s)

print('-' * 20)
file = open('hello.txt', 'r')
s  = file.read(10)
file.close()
print(s)

print('-' * 20)
file = open('hello.txt', 'r' , buffering=1)
s  = file.read()
file.close()
print(s)

text = ''
file = open('hello.txt', 'r')
while True :
    chunk = file.read(2)
    if not chunk :
        break 
    text += chunk
    print(chunk)
file.close()
print(text)

file = open('a.webp' , 'rb' )
s = file.read()
file.close()
print(s)

file = open('hello.txt', 'r')
s  = file.read()
file.close()
print(s)

with open('hello.txt' , 'r')  as file:
    s = file.read()
    print(s)

a = [1, 2, 3, 4]
with open('array1.txt' , 'w') as file :
    file.write(str(file))
print(str(a))

with open('array1.txt' , 'r') as file:
    b = file.read()
    print(type(b) , b)
    c = list(b)
    print(type(c) , c)

import pickle
name = 'eng'
age = 20
address = '한글'
arr = [1, 2, 3, 4]
score = {
    'k' : 1,
    'k2' : 'val'
}

with open('pickle.p' , 'wb') as file : 
    pickle.dump(name , file)
    pickle.dump(age , file)
    pickle.dump(address , file)
    pickle.dump(arr , file)
    pickle.dump(score , file)

with open('pickle.p'  , 'rb') as file :
  # dump 순서대로 꺼낸다
  p1 =  pickle.load(file)
  print(p1)
  p2 =  pickle.load(file)
  print(p2, type(p2))
  p2 =  pickle.load(file)
  print(p2, type(p2))
  p2 =  pickle.load(file)
  print(p2, type(p2))
  p2 =  pickle.load(file)
  print(p2, type(p2))
  print(p2['k'])

 # dump한 만큼만 꺼낼 수 있다
 # p2 = pickle.load(f)
 # print(p2, type(p2))

 # pickle 보다 대용량에 특화된 라이브러리 
#  import joblib

#a : 이어 쓰기 
# with open('hello.txt' , 'a') as file : 
#     file.write('123')
#     file.read()

# +
# 쓰기 계열에 붙어있으면 읽기 가능해짐 
# 읽기 계열에 붙어있으면 쓰기 가능해짐

# 단어 중 대소문자 구분없이 c를 포함하는 단어를 출력하시오. 단, ,.은 출력하지 마시오.

# 먼저 파일을 가져와서 읽기 
with open ('word.txt', 'r') as file :
    text = file.read() 

    # 공백을 기준으로 단어를 쪼개기
    words = text.split()

    # 단어를 하나씩 꺼내서 검사.
    for word in words :
       tmp = word.split('c')
       if len(tmp) > 1:
           a = word.split('.')
           b = ''.join(a)
           c = b.split(',')
           d = ''.join(c)
           print(d)

print('-' * 30)
with open ('word.txt', 'r') as file :
    text = file.read() 

    words = text.split()

    for word in words :
        if word.find('c') != -1 :
           a = word.replace(',' , '').replace('.' , '')
           print(a)

# 8월 3일 평가 문제 연습 
print('-' * 30)
# 조건1. order.txt를 읽기 모드로 읽기. 
with open ('order.txt' , 'r' , encoding='utf-8' ) as file :
    order = file.read()
    print(order) # 잘 읽었는지 확인

print('-' * 30)
# 조건2. 이상치 제거 
# 가격이 0보다 작은 경우
# 가격이 10000보다 큰 경우
# 개수가 0보다 작은 경우
# 파이썬에서 읽어온 텍스트 내용 중 원하는 문자나 문자열을 제거하려면 replace() , strip() 또는 조건문 필터링을 사용하면 된다고 합니다 
# (출처 : 구글 검색)
orders = order.replace('아메리카노, -2, 3000원' , '').replace('주스, 5, 12000' , '').replace('우유, 1, -2000', '').replace(',' , '')
print(orders)

# 조건3. 텍스트 클렌징 적용
# 각 항목의 앞뒤 공백 제거 
# 가격에서 "원" 제거
# 수량과 가격은 정수형으로 변환
print('-' * 30)
clean_orders = orders.strip() # 이러면 각 항목의 앞뒤 공백 제거
print(clean_orders) # 잘 제거가 되었는지 확인

# 조건4. 전체 매출 뽑아내기 
# 전체 매출을 뽑아내려면 문자열 그대로 int로 변환을 한다거나 아니면 다른 자료형으로 바꾸면 될거같은데....

# 전체 매출을 내는데 상품명은 필요가 없으니까 replace로 날려버리자
print('-' * 30)
total_incomes =  clean_orders.replace('아메리카노' , '').replace('카페라테' , '').replace('물', '').replace('탄산음료' , '')
print(total_incomes) # 잘 날라갔는지 확인

# int 함수에 공백과 줄바꿈이 포함된 여러 개의 숫자가 한 번에 들어가거나 빈 줄이 포함되면 오류가 발생하니까 
# 공백을 기준으로 쪼개고 빈 줄을 걸러내야 함

result = [int(i) for i in total_incomes.split()]
print(type(result),result)

total_income = sum(result) # 전체 매출을 계산
print(total_income)

