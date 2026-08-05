def div(x, y) :
    result = 0
    if y != 0 :
        result = x / y
    else:
        print('두번째 숫자는 0이 올 수 없습니다.')
    return result

def div2(x, y):
    result = 0
    try :
        result = x / y
    except:
        print('예외 발생')

    return result

def div3(x, y):
    result = 0
    try :
        result = x / y
    except ZeroDivisionError:
        print('0으로 나눌 수 없습니다')
    except TypeError:
        print('숫자만 넣어 주세요')

    return result

def div4(x, y):
    result = 0
    try :
        result = x / y
    except ZeroDivisionError as e: # 예외 메시지 출력
        print('0으로 나눌 수 없습니다' , e )
    except TypeError as e:
        print('숫자만 넣어 주세요' , e )

    return result

def div5(x, y):
    result = 0
    try :
        result = x / y
    except Exception as e : # 모든 예외 처리
        print('예외 발생' , e )

    return result

def div6(x, y):
    result = 0
    try :
        result = x / y
    except Exception as e : # 모든 예외 처리
        print('예외 발생' , e )
    else:
        print('문제 없었다')

    return result

def div7(x, y):
    result = 0
    try :
        result = x / y
        return result
    except Exception as e : # 모든 예외 처리
        print('예외 발생' , e )
    else:
        print('문제 없었다')
    finally:
        print('무조건 실행') # 무조건 실행. 심지어 return을 해도

    return result

a = div(7, 3)
print (a)

# a = div(7, 0)
# a = div2(7, '3')
a = div3(7, 0)
a = div3(7, 'a')
print(a)

a = div4(7, 0)
a = div4(7, 'a')
print(a)

a = div5(7, 0)
a = div5(7, 'a')
print(a)

a = div6(7, 0)
a = div6(7, 2)
print(a)

a = div7(7, 0)
a = div7(7, 2)
print(a)


# raise Exception('메세지')

def loginCheck(id, pw):
    if id == 'admin' and pw == '1234':
        print('로그인 성공')
        return 0

    elif id == '' :
        print('아이디를 입력해주세요')
        return 1

def login():
    id = 'admin'
    pw = '1234'
    result = loginCheck(id, pw)

    if result == 0:
        print('메인 페이지로 이동')
    elif result == 1:
        print('alert(아이디를 입력하세요)')

login()

def loginCheck2(id, pw):
    if id == 'admin' and pw == '1234':
        print('로그인 성공')
        return 0

    elif id == '' :
        print('아이디를 입력해주세요')
        raise Exception('code:1')
    
    elif pw == '' :
        print('비밀번호를 입력해주세요')
        raise Exception('code:2')

def login2():
    id = 'asdf'
    pw = ''
    try:
        result = loginCheck2(id, pw)
        if result == 0:
            print('메인 페이지로 이동')
    except TypeError as e:
        print(e)
        print('alert(비밀번호를 입력해주세요)')
    except Exception as e:
        print(1111, e)
        if e == 'code:1' :
            print('alert(아이디를 입력해주세요)')

login2()

import traceback
try:
    a = 3 / 0
except Exception as e:
    print(e)
    traceback.print_exc()
    a = traceback.format_exc()
    print('-' * 30)
    print(a)