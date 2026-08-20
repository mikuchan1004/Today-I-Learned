from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

# 코드에 적힌 주석들은 Google Gemini가 달아주었습니다.

# FastAPI 앱 객체 생성
app = FastAPI()

# Jinja2 템플릿 설정 (templates 폴더 안의 HTML 파일들을 읽어옵니다)
templates = Jinja2Templates(directory='templates/')

# 메모리 기반 데이터 저장소 (임시 DB 역할)
# 서버가 재시작되면 초기화되므로 실무에선 DB를 연동해야 합니다.
todo_list = []


# ==========================================
# 1. [전체 조회 페이지]
# ==========================================
@app.get('/')
def todo_list_page(request: Request):
    """
    [GET /]
    - 전체 Todo 목록을 보여주는 메인 페이지입니다.
    - Jinja2 템플릿 사용 시 FastAPI는 반드시 'request: Request' 객체를 인자로 받아야 합니다.
    - list.html에 'todos'라는 이름으로 todo_list 데이터를 전달합니다.
    """
    return templates.TemplateResponse(
        request=request, 
        name='list.html', 
        context={'todos': todo_list}
    )


# ==========================================
# 2. [추가 페이지 이동]
# ==========================================
@app.get('/add')
def todo_add_page(request: Request):
    """
    [GET /add]
    - 사용자가 새로운 Todo를 작성할 수 있는 폼 페이지(add.html)를 보여줍니다.
    """
    return templates.TemplateResponse(
        request=request, 
        name='add.html'
    )


# ==========================================
# 3. [추가 처리 (Form 제출)]
# ==========================================
@app.post('/add')
def todo_add(id: int = Form(...), item: str = Form(...)):
    """
    [POST /add]
    - add.html의 <form>에서 전송된 데이터를 받아 todo_list에 추가합니다.
    - HTML Form 데이터는 JSON이 아니므로 'Form(...)' 매개변수를 사용해야 합니다.
    - 추가 작업이 끝나면 전체 목록 페이지('/')로 사용자를 리다이렉트(페이지 이동)시킵니다.
    - status_code=303 (See Other): POST 요청 후 GET 요청으로 안전하게 페이지를 전환하기 위해 필수입니다.
    """
    # 폼으로 받아온 id와 item을 딕셔너리 형태로 리스트에 추가
    todo_list.append({'id': id, 'item': item})
    
    # 작업 완료 후 메인 페이지('/')로 리다이렉트
    return RedirectResponse(url='/', status_code=303)


# ==========================================
# 4. [상세 페이지]
# ==========================================
@app.get('/todo/{todo_id}')
def todo_detail(request: Request, todo_id: int):
    """
    [GET /todo/{todo_id}]
    - URL 경로로 전달받은 todo_id에 해당하는 단 하나의 Todo 항목만 조회합니다.
    - next(): todo_list에서 조건에 맞는 첫 번째 아이템을 찾고, 없으면 None을 반환합니다.
    """
    # todo_list에서 'id'가 URL의 'todo_id'와 일치하는 항목 검색
    target = next((t for t in todo_list if t['id'] == todo_id), None)
    
    # 해당 ID의 Todo가 없으면 메인 목록으로 돌아갑니다.
    if not target:
        return RedirectResponse(url='/', status_code=303)
        
    return templates.TemplateResponse(
        request=request, 
        name='detail.html', 
        context={'todo': target}
    )


# ==========================================
# 5. [수정 페이지 이동]
# ==========================================
@app.get('/todo/{todo_id}/edit')
def todo_edit_page(request: Request, todo_id: int):
    """
    [GET /todo/{todo_id}/edit]
    - 수정할 Todo의 기존 내용을 불러와 수정 입력 폼(edit.html)에 채워서 보여줍니다.
    """
    target = next((t for t in todo_list if t['id'] == todo_id), None)
    
    if not target:
        return RedirectResponse(url='/', status_code=303)
        
    return templates.TemplateResponse(
        request=request, 
        name='edit.html', 
        context={'todo': target}
    )


# ==========================================
# 6. [수정 처리 (Form 제출)]
# ==========================================
@app.post('/todo/{todo_id}/edit')
def todo_edit(todo_id: int, item: str = Form(...)):
    """
    [POST /todo/{todo_id}/edit]
    - 수정 폼에서 입력받은 새로운 item 내용으로 기존 데이터를 업데이트합니다.
    - 수정 완료 후 해당 항목의 [상세 페이지]로 다시 이동시킵니다.
    """
    for todo in todo_list:
        if todo['id'] == todo_id:
            todo['item'] = item  # 내용 수정
            break
            
    # 수정된 상세 페이지로 리다이렉트
    return RedirectResponse(url=f'/todo/{todo_id}', status_code=303)


# ==========================================
# 7. [삭제 처리]
# ==========================================
@app.post('/todo/{todo_id}/delete')
def todo_delete(todo_id: int):
    """
    [POST /todo/{todo_id}/delete]
    - 지정한 todo_id를 제외한 나머지 항목들로 todo_list를 다시 구성하여 삭제를 구현합니다.
    - 삭제가 끝나면 메인 목록 페이지('/')로 이동합니다.
    """
    global todo_list
    # 선택한 todo_id가 아닌 것들만 남김 (리스트 컴프리헨션)
    todo_list = [t for t in todo_list if t['id'] != todo_id]
    
    # 삭제 후 메인 페이지로 이동
    return RedirectResponse(url='/', status_code=303)


# 서버 실행부
if __name__ == "__main__":
    import uvicorn
    # 0.0.0.0:8000 포트에서 자동 새로고침(reload=True) 모드로 서버 시작
    uvicorn.run("api:app", port=8000, reload=True, host="0.0.0.0")