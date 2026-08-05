def div(x, y) :
    if y != 0 :
        result = x / y
    else:
        print('두번째 숫자는 0이 올 수 없습니다.')
    return result

def div2(x, y):
    result = x / y
    return result

a = div(7, 3)
print (a)

a = div(7, 0)
print(a)

