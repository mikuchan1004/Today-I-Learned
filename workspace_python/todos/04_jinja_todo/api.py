from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from todo import Todo  # type:ignore

app = FastAPI()

templates = Jinja2Templates(directory='templates/')

todo_list = []

# 1. 전체 목록 페이지
@app.get('/list')
def list(request: Request):
    print('/list 실행')
    return templates.TemplateResponse(request, 'list.html', {
        'list': todo_list
    })

# 2. 추가 페이지 이동
@app.get('/add')
def add_page(request: Request):
    print('/add 실행')
    return templates.TemplateResponse(request, 'add.html')

# 3. Todo 추가 처리
@app.post('/api/add')
def api_add(todo: Todo = Form()):
    print('/api/add 실행', todo)
    todo_list.append(todo)
    return RedirectResponse(url='/list', status_code=303)

# 4. Todo 상세 조회 페이지
@app.get('/detail/{id}')
def detail_page(request: Request, id: int):
    print('/detail/{id} 실행, id:', id)
    result = None
    for todo in todo_list:
        if todo.id == id:
            result = todo
    return templates.TemplateResponse(request, 'detail.html', {
        'todo': result
    })

# 5. Todo 수정 페이지 이동
@app.get('/update/{id}')
def update_page(request: Request, id: int):
    print('/update/{id} 실행, id:', id)
    result = None
    for todo in todo_list:
        if todo.id == id:
            result = todo
    return templates.TemplateResponse(request, 'update.html', {
        'todo': result
    })

# 6. Todo 수정 처리
@app.post('/api/update')
def api_update(todo: Todo = Form()):
    print('/api/update 실행', todo)
    for t in todo_list:
        if t.id == todo.id:
            t.item = todo.item
    return RedirectResponse(url='/list', status_code=303)

# 7. Todo 삭제 처리 (GET 방식 단 하나만!)
@app.get('/api/delete/{id}')
def api_delete(id: int):
    print('/api/delete 실행, id:', id)
    global todo_list
    todo_list = [t for t in todo_list if t.id != id]
    return RedirectResponse(url='/list', status_code=303)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", port=8000, reload=True, host="0.0.0.0")