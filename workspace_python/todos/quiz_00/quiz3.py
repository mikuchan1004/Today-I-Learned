from fastapi import APIRouter, Request

todo_router = APIRouter()

# 문제 3.
# 웹에서 
# - 숫자 2개와 연산자를 입력 
# - 2, "-" , 3
# 파이썬에서
# - 결과 출력 
# - 화면에서도 출력

@todo_router.post("/todo/param5")
async def todoParam(req:Request):
    data = await req.form()
    num_int1 = data.get('num_int1')
    num_int2 = data.get('num_int2')
    oper = data.get('operator')

    # 두 입력값이 숫자인지 검사
    if num_int1 and num_int1.isdigit() and num_int2.isdigit():
        num_int1 = int(num_int1)
        num_int2 = int(num_int2)
       
        # 입력받은 연산자에 따라 값이 다르게 나오게끔 if문을 써서 분리.
        if oper == '+' :
            total = num_int1 + num_int2
        elif oper == '-' :
            total = num_int1 - num_int2 
        elif oper == '*':
            total = num_int1 * num_int2
        elif oper == '/':
            if num_int2 == 0:
                return {"error" : "0으로 나눌 수 없다구 이 바보야"}
            total = num_int1 / num_int2

        return {
            "첫번째 숫자" : num_int1,
            "연산자" : oper,
            "두번째 숫자" : num_int2,
            "결과는?" : total
        }
    return {"error" : "제발 숫자만 넣어주세요."}