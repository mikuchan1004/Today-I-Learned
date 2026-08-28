# pip install itsdangerous

from fastapi import FastAPI,  Request,  Response
from starlette.middleware.sessions import SessionMiddleware
from fastapi.templating import Jinja2Templates 
from fastapi.responses import RedirectResponse   
from fastapi.staticfiles import StaticFiles

app = FastAPI()

templates = Jinja2Templates(directory='templates/')  

app.mount(
    "/static", # URL 경로 
    StaticFiles(directory="static"), # 실제 폴더 명
    name="static" # Jinja에서 사용할 이름 
)

app.add_middleware(
    SessionMiddleware,
      secret_key='human1234$'
 )

@app.get('/login')
def login(request:Request):
    # 세션 저장
    request.session['isLogin'] = True
    request.session['id'] = "admin"
    return "로그인 성공!"

@app.get('/mypage')
def mypage(request:Request):
    isLogin = request.session.get('isLogin')
    id = request.session.get('id')
    if isLogin is None  :
        return "로그인 하세요"  
    else :
        return f" id: [{id}] 비밀스러운 공간에 오신 걸 환영합니다."

@app.get('/logout')
def logout(request:Request):
    # invalidate
    request.session.clear()
    return "로그아웃"

@app.get('/')
def home(request:Request):
    return templates.TemplateResponse(request, 'main.html')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("session:app" , port=8000, reload=True, host="0.0.0.0")