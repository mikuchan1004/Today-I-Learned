from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
app = FastAPI()

templates = Jinja2Templates(directory='templates/')

@app.get('/hello')
def hello(request : Request):
    print('/hello 실행')
    return templates.TemplateResponse(request, 'home.html',{
        'ip' : request.client.host,
        'msg' : '안뇽?'
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app" , port=8000, reload=True, host="0.0.0.0")