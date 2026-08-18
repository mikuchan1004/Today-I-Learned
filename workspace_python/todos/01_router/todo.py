from fastapi import APIRouter, Form, Request
from model import Todo #type:ignore

todo_router = APIRouter()

todo_list = []

@todo_router.post("/todo")
async def add_todo(todo:dict) -> dict:
    print('todo:', todo)
    todo_list.append(todo)
    return{
        "message" : "정상적으로 추가되었습니다."
    }

@todo_router.get("/todo")
async def retrieve_todos() -> dict:
    return {
        "todos": todo_list
    }


@todo_router.get("/todo/param")
async def todoParamGet(id : int, item:str = "") -> dict:
    print(id, item)
    return {
        "id": id,
        "item" : item
    }

@todo_router.post("/todo/param")
async def todoParamPost(id : int = Form(), item:str = Form()) -> dict:
    print(id, item)
    return {
        "id": id,
        "item" : item
    }

@todo_router.get("/todo/param2")
@todo_router.post("/todo/param2")
@todo_router.put("/todo/param2")
@todo_router.delete("/todo/param2")
async def todoParam(req:Request) -> dict:
    if req.method == "GET":
        data = req.query_params
    else :
        data = await req.form()

    id = data.get('id')
    item = data.get('item')
    print(id, item, req.method)

    return {
        "id": id,
        "item" : item
    }

@todo_router.post('/todo43')
async def add_todo43(todo:Todo) -> dict:
    todo_list.append(todo)
    print(f'todo : {todo}')
    return {
        "code" : "200 OK"
    }

@todo_router.get("/todo/{todo_id}")
async def get_single_todo(todo_id: int) -> dict:
    print('todo_id:' , todo_id)
    for todo in todo_list:
        if todo.id == todo_id:
            return {
                "todo" : todo 
            }
    return {
        "message" : "ID가 존재하지 않습니다"
    }

# Valid, Validate 유효성 검증
from fastapi import Path
@todo_router.get("/todo2/{todo_id}")
async def get_single_todo2(todo_id: int = Path(gt=10, le=100)) -> dict:
    print('todo_id:' , todo_id)
    
    for todo in todo_list:
        if todo.id == todo_id:
            return {
                "todo" : todo 
            }
    return {
        "message" : "ID가 존재하지 않습니다"
    }

from typing import Annotated

ValidTodoID = Annotated[int, Path(ge=10)]

@todo_router.get("/todo3/{todo_id}")
# async def get_single_todo3(todo_id: Annotated[int, Path(ge=10)]) -> dict:
async def get_single_todo3(todo_id: ValidTodoID) -> dict:
    print('todo_id:' , todo_id)
    
    for todo in todo_list:
        if todo.id == todo_id:
            return {
                "todo" : todo 
            }
    return {
        "message" : "ID가 존재하지 않습니다"
    }

# get 방식일 때, 즉 ? 뒤에 오는 query string
from fastapi import Query
@todo_router.get("/todo4")
def todo4(id: int = Query(gt=0, lt=10000)):
    print(id)


print(2, __name__)

if __name__ == "__main__":
    print('todo.py 파일 직접 실행')