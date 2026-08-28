# pip install itsdangerous

from fastapi import FastAPI,  Request,  Response
from starlette.middleware.sessions import SessionMiddleware
from fastapi.templating import Jinja2Templates 
from fastapi.responses import RedirectResponse   

app = FastAPI()

templates = Jinja2Templates(directory='templates/')  

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