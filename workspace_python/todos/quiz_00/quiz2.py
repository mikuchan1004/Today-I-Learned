from fastapi import APIRouter, Request

todo_router = APIRouter()

# 문제 2.
# 클라이언트에서 
# -숫자 두 개를 입력받음 
# 파이썬에서 
# - 두 개의 합을 출력.

@todo_router.post("/todo/param4")
async def todoParam(req:Request):
    data = await req.form()
    num1 = data.get('num1')
    num2 = data.get('num2')

    # 두 입력값이 숫자인지 검사
    if num1 and num1.isdigit() and num2.isdigit():
        num1 = int(num1)
        num2 = int(num2)
        total = num1 + num2

        return {
            "number1" : num1,
            "number2" : num2,
            "result" : total
        }