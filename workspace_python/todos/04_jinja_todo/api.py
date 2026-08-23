from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from todo import Todo  # type:ignore (Pydantic 모델 Todo 클래스 임포트)

# FastAPI 애플리케이션 객체 생성
app = FastAPI()

# Jinja2 템플릿 연동 설정 (templates 디렉토리 지정)
templates = Jinja2Templates(directory='templates/')

# 인메모리 Todo 저장소 (임시 데이터베이스 역할)
todo_list = []

# 1. 전체 Todo 목록 조회 페이지 라우트
@app.get('/list')
def list(request: Request):
    print('/list 실행')
    # list.html 템플릿에 todo_list 데이터를 넘겨주며 렌더링
    return templates.TemplateResponse(request, 'list.html', {
        'list': todo_list
    })

# 2. Todo 추가 화면 이동 라우트
@app.get('/add')
def add_page(request: Request):
    print('/add 실행')
    # 추가 폼이 작성된 add.html 템플릿 렌더링
    return templates.TemplateResponse(request, 'add.html')

# 3. Todo 생성 API 라우트
@app.post('/api/add')
def api_add(todo: Todo = Form()):
    print('/api/add 실행', todo)
    # Form 데이터로 전달받은 Todo 객체를 메모리 리스트에 추가
    todo_list.append(todo)
    # 추가 작업 완료 후 목록 페이지(/list)로 리다이렉트 (HTTP 303 See Other)
    return RedirectResponse(url='/list', status_code=303)

# 4. Todo 상세 정보 조회 페이지 라우트
@app.get('/detail/{id}')
def detail_page(request: Request, id: int):
    print('/detail/{id} 실행, id:', id)
    result = None
    # todo_list를 순회하며 URL 경로로 들어온 id와 일치하는 Todo 탐색
    for todo in todo_list:
        if todo.id == id:
            result = todo
    # 조회된 Todo 객체를 detail.html 템플릿에 전달하여 렌더링
    return templates.TemplateResponse(request, 'detail.html', {
        'todo': result
    })

# 5. Todo 수정 화면 이동 라우트
@app.get('/update/{id}')
def update_page(request: Request, id: int):
    print('/update/{id} 실행, id:', id)
    result = None
    # todo_list를 순회하며 수정할 대상 id와 일치하는 Todo 탐색
    for todo in todo_list:
        if todo.id == id:
            result = todo
    # 기존 Todo 데이터를 update.html 템플릿에 전달하여 폼에 기본값 세팅
    return templates.TemplateResponse(request, 'update.html', {
        'todo': result
    })

# 6. Todo 수정 처리 API 라우트
@app.post('/api/update')
def api_update(todo: Todo = Form()):
    print('/api/update 실행', todo)
    # 리스트에서 전달받은 todo.id와 동일한 항목을 찾아 내용(item) 갱신
    for t in todo_list:
        if t.id == todo.id:
            t.item = todo.item
    # 수정 완료 후 목록 페이지(/list)로 리다이렉트
    return RedirectResponse(url='/list', status_code=303)

# 7. Todo 삭제 처리 API 라우트 (GET 방식 /a 태그 매핑)
@app.get('/api/delete/{id}')
def api_delete(id: int):
    print('/api/delete 실행, id:', id)
    global todo_list
    # 리스트 컴프리헨션: 삭제할 id와 일치하지 않는 요소들만 새로 남겨서 리스트 갱신
    todo_list = [t for t in todo_list if t.id != id]
    # 삭제 완료 후 목록 페이지(/list)로 리다이렉트
    return RedirectResponse(url='/list', status_code=303)


# 메인 모듈 실행 시 Uvicorn 개발 서버 시작
if __name__ == "__main__":
    import uvicorn
    # uvicorn 서버 실행 (host: 0.0.0.0, port: 8000, 코드 변경 시 자동 재시작: reload=True)
    # 포트 번호 변경 (사유 : 8000번 포트를 디스코드가 선점해서 사용 불가.)
    uvicorn.run("api:app", port=8085, reload=True, host="0.0.0.0")