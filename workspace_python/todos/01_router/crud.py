from fastapi import APIRouter
from pydantic import BaseModel

crud_router = APIRouter()

todo_list = []

# 할 일 
# crud.py
# todo_list에 crud하는 라우터를 설정하고 
# api.py를 실행해서 테스트하기 

# 이케이케 해도 되고 
# /crud/c
# /crud/r
# /crud/u
# /crud/d

# 이렇게 할 수 있을까요?
# /crud [GET, PUT, DELETE]

@crud_router.post('/crud/c')
async def add_todo(todo:dict) -> dict:
    print('todo:' , todo)
    todo_list.append(todo)
    return {
        "메시지" : "정상적으로 추가되었습니다."
    }

@crud_router.get('/crud/r')
async def get_todo(todo_id : int) -> dict:
   print(todo_id, todo_list)
   for todo in todo_list :
       # 입력받은 todo의 아이디가 등록된 todo의 아이디와 같다면, "todo" : todo 형태로 돌려줌
       if todo.get('id') == todo_id:
           return {
               "todo" : todo 
           }
   return {
       "메시지" : "그런 아이디는 없는데요?"
   } 

class Todo(BaseModel):
    item:str


@crud_router.put('/crud/u')
async def update_todos(todo_id : int, todo_data : Todo) -> dict:
    for todo in todo_list:
        if todo['id'] == todo_id:
            todo['item'] = todo_data.item
            return {
                "메시지" : "Todo가 변경되었습니다."
            }
    return {
        "메시지" : "ID가 존재하지 않습니다."
    }

@crud_router.delete('/crud/d')
async def delete_single_todo(todo_id : int) -> dict:
    for i in range(len(todo_list)):
        todo = todo_list[i]
        if todo['id'] == todo_id:
            todo_list.pop(i)
        return {
            "메시지" : "Todo가 삭제되었습니다."
        }
    return {
        "메시지" : "입력받은 ID는 존재하지 않습니다."
    }