from fastapi import APIRouter

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