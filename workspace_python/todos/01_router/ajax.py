from fastapi import APIRouter, Request
from model import Todo #type:ignore

ajax_router = APIRouter()

todo_list = []

@ajax_router.post("/ajax/todo")
async def add_todo(todo:dict) -> dict:
    print('todo:', todo )
    todo_list.append(todo)
    return {
        "메시지" : "정상적으로 추가되었습니다.",
        "todos" : todo_list
    }

@ajax_router.delete("/ajax/todo/{todo_id}")
async def delete_todo(todo_id : str):
    global todo_list
    # 전달받은 todo_id와 일치하지 않는 항목들만 남겨서 목록 갱신
    todo_list = [todo for todo in todo_list if str(todo.get("id")) != str(todo_id)]

    return {
        "메시지" : f"ID {todo_id}번 항목이 삭제되었습니다.",
        "todos" : todo_list
    }

@ajax_router.get("/ajax/todo")
async def get_todos():
    return {
        "todos" : todo_list
    }

# 구구단을 출력하는데 필요한 코드
@ajax_router.post("/ajax/quiz1")
async def  quiz1(req:Request):
    data = await req.form()
    number = data.get('number')

    #입력값이 유효한 숫자인지 확인 
    if number and number.isdigit():
        num = int(number)

        #구구단 계산 결과를 리스트로 생성 
        gugudan_list = [f"{num} x {i} = {num * i}"for i in range(1,10)]

        return {
            "숫자" : num,
            "구구단" : gugudan_list
        }
    return{"error" : "숫자만 넣는거야 바보야"}

# 두 수의 합을 출력하는데 필요한 코드 
@ajax_router.post("/ajax/quiz2")
async def quiz2(req:Request):
    data = await req.form()
    num1 = data.get('num1')
    num2 = data.get('num2')

    # 두 입력값이 숫자인지 검사
    if num1 and num1.isdigit() and num2.isdigit():
        num1 = int(num1)
        num2 = int(num2)
        total = num1 + num2

        return {
            "첫번째 숫자" : num1,
            "두번째 숫자" : num2,
            "결과는?" : total 
        }
    return {"error" : "숫자만 넣으라니까?"}

#웹버전 계산기 코드 
@ajax_router.post('/ajax/quiz3')
async def quiz3(req:Request):
    data = await req.form()
    num_int1  = data.get('num_int1')
    num_int2 = data.get('num_int2')
    oper = data.get('operator')

    #두 입력값이 숫자인지 검사
    if num_int1 and num_int1.isdigit() and num_int2.isdigit():
        num_int1 = int(num_int1)
        num_int2 = int(num_int2)

        #입력받은 연산자에 따라 값이 다르게 나오게끔  if문을 써서 분리 
        if oper == '+' :
            total = num_int1 + num_int2
        elif oper == '-':
            total = num_int1 - num_int2
        elif oper == '*' :
            total = num_int1 * num_int2
        elif oper == '/':
            if num_int2 == 0:
                return {'error' : '0으로 나눌 수 없다구 이 바보야'}
            total = num_int1  / num_int2

            return {
                "첫번째 숫자" : num_int1,
                "연산자" : oper,
                "두번째 숫자" : num_int2,
                "결과는?" :   total
            } 
        return {'error' : '숫자만 넣는거라니까? 바보야?'}

@ajax_router.post('/todo43')
async def add_todo43(todo:Todo) -> dict:
    todo_list.append(todo)
    print(f'todo: {todo}')
    return {
        "code" : "200 OK"
    }