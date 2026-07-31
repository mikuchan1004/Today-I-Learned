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
