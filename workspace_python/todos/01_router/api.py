from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from todo import todo_router #type:ignore

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