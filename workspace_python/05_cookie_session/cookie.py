from fastapi import FastAPI, Cookie, Request, Response
from fastapi.templating import Jinja2Templates 
from typing import Annotated

app = FastAPI()
# HTML 템플릿 파일들이 저장되어 있는 폴더 지정
templates = Jinja2Templates(directory='templates/') 

# 브라우저가 /main 주소로 접속했을 때 실행되는 함수
@app.get('/main')
def main(
     request: Request,
     response : Response,

     # [쿠키 읽기 1] 브라우저가 보낸 쿠키 중 'no'라는 이름을 찾아 알아서 변수에 저장합니다.
     # 쿠키가 없으면 기본값으로 None이 들어갑니다.
     no: str | None = Cookie(None),
     
     # [쿠키 읽기 2] 위와 동일한 기능인데, Annotated라는 최신 파이썬 문법 형태로 쓴 것입니다.
     yes : Annotated[str | None, Cookie()] = None 
     ):
     
     # 서버 터미널 창에 받은 쿠키 값을 출력해서 확인합니다.
     print('no :' , no)
     print('yes :' , yes)

     # 브라우저에 보여줄 HTML 화면(main.html) 응답 객체를 만듭니다.
     response = templates.TemplateResponse(request, 'main.html')

     # [쿠키 쓰기 1] 기본 세션 쿠키 설정 (브라우저 종료 전까지 유지)
     response.set_cookie(
         key = 'key',
         value = 'value'
     )

     # [쿠키 쓰기 2] 10초 후 자동 삭제되는 타이머 쿠키 설정
     response.set_cookie(
         key = 'key2',
         value = 'value2',
         max_age = 10 # 10초 수명
     )

     # [쿠키 쓰기 3] 보안 강화 쿠키 설정 (httponly=True)
     response.set_cookie(
         key = 'key3',
         value = 'value3',
         max_age = 1000,
         httponly = True # 자바스크립트(document.cookie)로 접근 불가능하게 막아 해킹 방지
     )

     # 준비된 응답(HTML + 쿠키 3개)을 브라우저로 보냅니다.
     return response


# 브라우저가 /delete/cookie 주소로 접속했을 때 쿠키 삭제 처리
@app.get('/delete/cookie')
def delete_cookie(response: Response):
     # 브라우저에게 'key3' 쿠키를 즉시 삭제하라고 명령합니다.
     response.delete_cookie('key3')
     return '{"message" : "쿠키 key3 삭제 완료"}'


if __name__ == "__main__":
    import uvicorn
    # 서버 실행 명령어 (포트 8000번)
    uvicorn.run("cookie:app" , port=8000, reload=True, host="0.0.0.0")