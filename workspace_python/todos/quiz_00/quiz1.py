from fastapi import APIRouter, Request

todo_router = APIRouter()

# 문제 1.
# 브라우저에서 
# input에 몇 단 입력
# 파이썬에서 
# 해당 구구단의 단 출력 

@todo_router.post("/todo/param3")
async def todoParam(req:Request):
    data = await req.form()
    number = data.get('number')

    # 1. 입력값이 유효한 숫자인지 확인 
    if number and number.isdigit():
        num = int(number)

        # 2. 구구단 계산 결과를 리스트로 생성
        gugudan_list = [f"{num} x {i} = {num * i}" for i in range(1,10)]
    
        return {
            "숫자" : num,
            "구구단" : gugudan_list
        }
    return {"error" : "숫자만 넣는거라구."}