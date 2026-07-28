a = 10
b = 5
print(3 < a < 20)

if True : 
    print(1)
# print(2)
    print(3)

    if True : 
        print(4)

if True :
    pass
else :
    pass

if 1 : 
    print('참')

    '''
    파이썬에서 False란?
    False, None, 0, 0.0, 빈 컨테이너(비어있는 문자열, 리스트, 튜플, 딕셔너리)
    '''

a = []
if a :
    print('참')
else : 
    print('거짓')

# 문제 14.7 (174페이지)
score = input('점수 4개 입력, 띄어쓰기로 구분 : ')
print(score, score.split(' ')) 
scores = score.split(' ') # 입력된 점수들을 List로 반환
sum = int(scores[0]) + int(scores[1]) + int(scores[2]) + int(scores[3]) # 모든 점수를 합침
avg = sum / len(scores) # 합친 점수의 평균을 구함

if (0 <= int(scores[0]) <= 100) \
    and (0 <= int(scores[1]) <= 100) \
    and (0 <= int(scores[2]) <= 100) \
    and (0 <= int(scores[3]) <= 100) :

    if avg >= 80 :
        print('합격')
    else :
        print('불합격')
else : 
    print('잘못된 입력')

button = int(input('메뉴를 고르시오'))

if button == 1:
    print('콜라')
elif button == 2:
    print('사이다')
elif button == 3:
    print('환타')
else : 
    print('제공하지 않는 메뉴')

# break 필요 없음
# 또는은 | (파이프)

a = 7
match a :
    case 6 | 7 | 8 :
        print('여름')
    case '여름2' :
        print('여름2')
    case _ :
        print('그 외')