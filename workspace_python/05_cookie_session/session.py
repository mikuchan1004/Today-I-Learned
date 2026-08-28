# pip install itsdangerous

from fastapi import FastAPI,  Request,  Response
from starlette.middleware.sessions import SessionMiddleware
app = FastAPI()




if __name__ == "__main__":
    import uvicorn
    uvicorn.run("session:app" , port=8000, reload=True, host="0.0.0.0")