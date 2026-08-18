from fastapi import FastAPI, Request
# 크로스 도메인 문제 해결을 위해 필요한걸 호출
from fastapi.middleware.cors import CORSMiddleware
# 불러온 라우터들에게 별칭 부여
from todo import todo_router as main_router #type:ignore
from quiz_00.quiz1 import todo_router as quiz1_router
from quiz_00.quiz2 import todo_router as quiz2_router
from quiz_00.quiz3 import todo_router as quiz3_router
from ajax import ajax_router #type:ignore

# 크로스 도메인 CORS 해결 코드
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_methods = ["*"],
    allow_headers = ["*"]
)

@app.get("/")
async def welcome() -> dict:
    return {
        "message" : "Hello World"
    }

app.include_router(main_router)
app.include_router(quiz1_router)
app.include_router(quiz2_router)
app.include_router(quiz3_router)
app.include_router(ajax_router)

@app.get('/ip')
def test(req: Request):
    ip = req.client.host
    print(ip)

    return ip

print(1, __name__)

if __name__ == "__main__":
    print('api.py 파일 직접 실행')

    import uvicorn
    uvicorn.run("api:app" , port=8000, reload=True, host="0.0.0.0")