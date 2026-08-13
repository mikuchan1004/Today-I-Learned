from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def welcome() -> dict:
    return {
        "message" : "Hello World"
    }

# 주소와 방식이 같은 게 있다면 먼저 선언한 것만 실행된다. 조심하자. 
@app.get("/html")
def html()  : 
    return "<h1>hello</h1>"

# @app.get("/html")
# def htm2l()  : 
#     return "<h1>hello2</h1>"

@app.post('/html')
def html2() :
    return "<h1>hello2</h1>"

@app.get("/no")
def no()  : 
    print('들어왔음')
# retrun이 없으면 null을 돌려준다  (fastAPI 한정)