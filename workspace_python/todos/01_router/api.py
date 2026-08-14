from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from todo import todo_router #type:ignore
# quiz_00 폴더의 quiz1 파일에 있는 todo_router를 가져다가 쓰겠다는 의미
from quiz_00.quiz1 import todo_router
# quiz_00 폴더의 quiz2 파일에 있는 todo_router를 가져다가 쓰겠다는 의미
from quiz_00.quiz2 import todo_router
# quiz_00 폴더의 quiz3 파일에 있는 todo_router를 가져다가 쓰겠다는 의미
from quiz_00.quiz3 import todo_router

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

app.include_router(todo_router)

print(1, __name__)

if __name__ == "__main__":
    print('api.py 파일 직접 실행')

    import uvicorn
    uvicorn.run("api:app" , port=8000, reload=True)