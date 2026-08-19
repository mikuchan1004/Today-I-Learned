from fastapi import APIRouter, Form
from pydantic import BaseModel

crud_router = APIRouter()

todo_list = []

# 할 일 
# crud.py
# todo_list에 crud하는 라우터를 설정하고 
# api.py를 실행해서 테스트하기 

# 이케이케 해도 되고 
# /crud/c
# /crud/r
# /crud/u
# /crud/d

# 이렇게 할 수 있을까요?
# /crud [GET, PUT, DELETE]

@crud_router.post('/crud/c')
async def add_todo(todo:dict) -> dict:
    print('todo:' , todo)
    todo_list.append(todo)
    return {
        "메시지" : "정상적으로 추가되었습니다."
    }

@crud_router.get('/crud/r')
async def get_todo(todo_id : int) -> dict:
   print(todo_list)
   for todo in todo_list :
       # 입력받은 todo의 아이디가 등록된 todo의 아이디와 같다면, "todo" : todo 형태로 돌려줌
       if todo.get('id') == todo_id:
           return {
               "todo" : todo 
           }
   return {
       "메시지" : "그런 아이디는 없는데요?"
   } 

class Todo(BaseModel):
    id:int
    item:str

class Todo2(BaseModel):
    item:str


@crud_router.put('/crud/u')
async def update_todos(todo_id : int, todo_data : Todo2) -> dict:
    for todo in todo_list:
        if todo['id'] == todo_id:
            todo['item'] = todo_data.item
            return {
                "메시지" : "Todo가 변경되었습니다."
            }
    return {
        "메시지" : "ID가 존재하지 않습니다."
    }

@crud_router.delete('/crud/d')
async def delete_single_todo(todo_id : int) -> dict:
    for i in range(len(todo_list)):
        todo = todo_list[i]
        if todo['id'] == todo_id:
            todo_list.pop(i)
        return {
            "메시지" : "Todo가 삭제되었습니다."
        }
    return {
        "메시지" : "입력받은 ID는 존재하지 않습니다."
    }

###############
## ajax 전용 (주석은 Google Gemini가 달아주었습니다)
###############

# ----------------------------------------------------
# 1. 데이터 등록 (Create / POST)
# ----------------------------------------------------
@crud_router.post('/crud/api/c')
def crud_api_c(todo: Todo):
    # 클라이언트가 보낸 JSON 데이터를 Pydantic(Todo) 객체로 받아 메모리 리스트에 추가
    todo_list.append(todo)
    print('/crud/api/c 등록 데이터:', todo)
    return todo  # 등록된 Todo 객체 반환


# ----------------------------------------------------
# 2. 전체 목록 조회 (Read All / GET)
# ----------------------------------------------------
@crud_router.get('/crud/api/r')
def crud_api_r_all():
    print('/crud/api/r 전체 목록 조회')
    print(todo_list)
    return todo_list  # 메모리에 저장된 전체 Todo 리스트 배열 반환


# ----------------------------------------------------
# 3. 단일 항목 상세 조회 (Read One / GET)
# ----------------------------------------------------
@crud_router.get('/crud/api/r/{id}')
def crud_api_r_one(id: int):
    print('/crud/api/r/id 상세 조회 요청 ID:', id)
    
    # todo_list를 순회하며 URL 경로로 전달받은 id와 일치하는 항목 검색
    for todo in todo_list:
        print(f"비교: 저장된 ID({todo.id}) == 요청 ID({id})")
        if todo.id == id:
            print('일치하는 항목 찾음:', todo)
            return todo  # 일치하는 Todo 객체를 찾으면 즉시 반환하고 함수 종료


# ----------------------------------------------------
# 4. 데이터 수정 (Update / PUT)
# ----------------------------------------------------
@crud_router.put('/crud/api/u')
def crud_api_u(todo: Todo):
    print('/crud/api/u 수정 요청 데이터:', todo)
    
    # todo_list 안의 item 객체들과 수신받은 todo.id를 비교
    for item in todo_list:
        if item.id == todo.id:
            item.item = todo.item  # 전달받은 새로운 문자열(todo.item)로 값 수정
            return {"result": "success"}  # 수정 완료 후 즉시 종료하여 불필요한 연산 방지


# ----------------------------------------------------
# 5. 데이터 삭제 (Delete / DELETE)
# ----------------------------------------------------
@crud_router.delete('/crud/api/d/{id}')
def crud_api_d(id: int):
    print('/crud/api/d 삭제 요청 ID:', id)

    # 인덱스(i)를 이용해 원본 리스트 순회 및 해당 요소 삭제
    for i in range(len(todo_list)):
        if todo_list[i].id == id:
            todo_list.pop(i)  # 해당 인덱스의 요소 제거
            return {"result": "success"}  # 삭제 직후 return으로 종료하여 인덱스 초과 에러(IndexError) 방지
