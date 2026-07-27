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