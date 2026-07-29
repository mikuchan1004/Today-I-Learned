# 딕셔너리 선언
a = ()
a = dict()
print (type(a))

b = {
    '이름' : '호랑이심장',
    '직업' : '마법사',
    '직업2' : '전사' ,
    '스킬' : {
        '공격' : '고백' ,
        '방어' : '철벽남' , 
        'javascript' : '중'
    }
}

print(b)

c = dict(a=10, b=20)
print(c)

print(b['이름'])

print(b.get('이름'))
print(b.get('이름2')) # 없으면 None
print(b.get('이름2', '이름없음')) # 없으면 두번째 값으로 대체 

print(b['스킬']['공격'])
print(b.get('스킬').get('공격'))

print(b.get('스킬2' , {}).get('공격', 0)) 

b['직업'] = '도적'
print(b)

b['직업2'] = '도적2' # 없으면 key 만들어 줌 
print(b)

print('스킬' in b)

print ('공격' in b['스킬'])

print(len(b)) # key의 개수

e = b.keys()
print (e)

f = b.values()
print(f)

g = b.items()
print(g)

a = 'hello'
print(list(a))
print(set(a))
# set
# 중복을 제거해서 관리한다.
# 순서는 보장하지 않는다.

b = {
    '이름' : '호랑이심장',
    '직업' : '마법사',
    '직업2' : '전사' ,
    '스킬' : {
        '공격' : '고백' ,
        '방어' : '철벽남' , 
        'javascript' : '중'
    }
}
b.update(이름 = '타이거' , 직업 = '강사')
print (b)
b.update(이름 = '타이거' , 직업 = '강사' , 나이 = '20')
print(b)

c = b.pop('나이')
print(b)
print(c)
# c = b.pop('나이')
c = b.pop('나이' , 0) # 없으면 두 번째 값을 사용
print(c)
# c = b.pop() # 전달인자 필수
c = b.popitem()
print(c)
print(b)

a = ['a' , 'b' , 'c']
b = {
    'a' : 0,
    'b' : 0,
    'c' : 0
}
b = {}
b[a[0]] = 0
b[a[1]] = 0

c = dict.fromkeys(a)
print(c)

# key만 나온다 
for i in c :
    print(i)
    print(c[i]) 

for k , v in c.items() :
    print (k, v)

