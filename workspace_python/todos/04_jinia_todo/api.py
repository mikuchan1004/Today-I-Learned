from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()

templates = Jinja2Templates(directory='templates/')

todo_list = []

# 추가 페이지
@app.get('/add')
async def add_todo(request:Request, todo : dict) -> dict:
    print('/add 실행')
    print('todo:' , todo)
    todo_list.append(todo)
    return templates.TemplateResponse(request, 'add.html')

# 전체 조회
@app.get('/')
async def todo_list_all(request:Request):
    print('/ 실행')
    return templates.TemplateResponse(request, 'list.html')

# 상세 조회
@app.get('/${todo_id}/detail')
async def todo_detail(request:Request, todo_id:int) -> dict:
    print('/detail 실행')
    for todo in todo_list :
        if todo.get('id') == todo_id:
            return {
                "todo" : todo
            }
    return templates.TemplateResponse(request, 'detail.html')

class Todo(BaseModel):
    id : int
    item : str

class Todo2(BaseModel):
    item : str

# 내용 수정
@app.post('/${todo_id}/modify')
async def update_todo(request:Request, todo_id : int, todo_data : Todo2) -> dict:
    print('/modify 실행')
    for todo in todo_list:
        if todo['id'] == todo_id:
            todo['item'] = todo_data.item
            return {
                "메시지" : "Todo가 변경되었습니다."
            }
    return templates.TemplateResponse(request, 'modify.html')

# todo 삭제 
@app.post('/${todd_id}/delete')
async def delete_todo(todo_id : int) -> dict:
    for i in range(len(todo_list)):
        todo = todo_list[i]
        if todo['id'] == todo_id:
            todo_list.pop(i)
    return {
        "메시지" : "Todo가 삭제되었습니다."
    }
 

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app" , port=8000, reload=True, host="0.0.0.0")