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
orders = order.replace('아메리카노, -2, 3000원' , '').replace('주스, 5, 12000' , '').replace('우유, 1, -2000', '')
print(orders)

# 조건3. 텍스트 클렌징 적용
# 각 항목의 앞뒤 공백 제거 
# 가격에서 "원" 제거
# 수량과 가격은 정수형으로 변환
print('-' * 30)
clean_orders = orders.strip() # 이러면 각 항목의 앞뒤 공백 제거
print(clean_orders) # 잘 제거가 되었는지 확인

# 조건4. 전체 매출 뽑아내기 

total_sales = 0 #  총 매출이 들어갈 주머니 

# clean_orders에는 엔터(\n)이 남아있을 테니까 줄바꿈을 기준으로 쪼개서 리스트로
lines = clean_orders.split('\n')

print('-' * 30)
for line in lines :
    # replace로 통째로 날려버려서 생긴 빈 줄은 계산할 수 없으니  무시
    if not line.strip():
        continue

    items = line.split(',') # 쉼표를 기준으로 쪼갬 
    print(items)

    # 혹시라도 다른 데이터에 "원" 글자가 남아있을 수도 있으니 마저 정리 
    quantity = int(items[1])
    price = int(items[2].replace('원' , ''))

    # 수량과 가격을 곱해서 총 매출 주머니에 넣기 
    total_sales += (quantity * price)

    print('-' * 30)
    print(f"전체 매출 : {total_sales} 원")