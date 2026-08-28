from fastapi import FastAPI, Cookie, Request,  Response
from fastapi.templating import Jinja2Templates 
from typing import Annotated

app = FastAPI()
templates = Jinja2Templates(directory='templates/') 

@app.get('/main')
def main(
     request: Request,
     response : Response,

     no: str | None = Cookie(None),
     yes : Annotated [str|None, Cookie()] = None 
     ):
     print('no' , no)
     print('yes' , yes)

     response = templates.TemplateResponse(request, 'main.html')

     response.set_cookie(
         key = 'key',
         value = 'value'
     )

     response.set_cookie(
         key = 'key2',
         value = 'value2',
         max_age = 10 # 10초 후 쿠키가 사라짐 
     )

     response.set_cookie(
         key = 'key3',
         value = 'value3',
         max_age = 1000,
         httponly = True # javascript로 수정 불가
     ) 

     return response

@app.get('/delete/cookie')
def delete_cookie(response:Response):
     response.delete_cookie('key3')
     return '{"message" : "쿠키 key3 삭제 완료"}'

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("cookie:app" , port=8000, reload=True, host="0.0.0.0")