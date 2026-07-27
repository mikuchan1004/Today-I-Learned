a = 'hello'
b = 'world'

c  = '''여기에
여러 줄 
넣을 수 있다'''

d = """여러 줄
가능"""

'''
여러줄 
주석으로 사용됨
'''

'he\'s name is \"민수\"'

b = 32.5
c = "지금 온도는 " + str(b) + "도 입니다"
print(c)

d = f"지금 온도는 {b}도 입니다"

print(d)

e = "지금 온도는 {0}도 입니다".format(b)
print(e)

f = f'''
<div>
    지금 온도는 {b}도 입니다
</div>
'''

g = '지금 온도는 %d도 입니다' % b
print(g)

h = '지금 온도는 %f도 입니다' % b
print(h)

i = '_hello'
print(len(i))

print(i.count('l'))
print(i.find('l')) # indexOf
print(i.find('z')) # 없으면 -1 

print(i.index('l'))
# print(i.index('z')) # 없으면 에러 

print(i.rfind('l')) # rear 뒤에서 부터 indexOf

print(i.replace('l' , 'w')) # 모두 바꿔 줌 

j = '그럼 저기서 하나만 바꾸고 싶으면요?'
k = j.split()
print(k)

m = [1, 2, 3]
a, b, c = m