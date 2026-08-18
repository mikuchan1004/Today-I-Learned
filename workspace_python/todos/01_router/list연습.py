from fastapi import APIRouter

todo_router = APIRouter()

todo_list = []

d1 = {
    'id':1684,
    'item':'item1'
}

# d1을 list에 추가
todo_list.append(d1)
print(todo_list)

d2 = {
    'id':29681,
    'item':'item2'
}

todo_list.append(d2)
print(todo_list)

# id가 29681인 것의 딕셔너리 출력 
print(todo_list[1])