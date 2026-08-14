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

print(2, __name__)

if __name__ == "__main__":
    print('todo.py 파일 직접 실행')