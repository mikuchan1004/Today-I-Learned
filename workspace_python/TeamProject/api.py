from sqlmodel import create_engine, Session, SQLModel  # DB 연결 및 테이블 관리를 위한 SQLModel 모듈
from fastapi import FastAPI, Depends, Request, Form    # FastAPI 기본 기능, 의존성 주입(Depends), 요청 객체(Request), 폼 데이터 처리(Form)
from fastapi.templating import Jinja2Templates         # HTML 템플릿(Jinja2) 연동을 위한 모듈
from fastapi.responses import RedirectResponse         # 작업 완료 후 다른 페이지로 이동(리다이렉트)시키는 모듈
from sqlalchemy import text                           # 원시 SQL(Raw SQL) 문장을 안전하게 실행하기 위한 함수

from DTO.BoardDTO import Board

app = FastAPI()
templates = Jinja2Templates(directory='templates/') 

DATABASE_URL = 'mysql+pymysql://root:human1234$@127.0.0.1:3306/human'

engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session 
        session.commit()

@app.on_event('startup')
def on_startup():
    # 테이블 삭제용 코드 (주의 : 모든 테이블을 날려버리니 신중하게 사용할것)
    # SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

# 게시판 페이지
@app.get('/board')
def board(request:Request, session:Session = Depends(get_session)):
    print('/board  실행')
    # 전체 게시판 조회를 위한 SQL 문 작성 
    sql = text('''
        select * from board
    ''')

    # .mappings().fetchall() : 쿼리 결과를 딕셔너리 형태로 변환하여 전체 목록을 가져옵니다.
    results = session.execute(sql).mappings().fetchall()

    # board.html에 baard_list 변수 이름으로 조회 결과를 전달하여 화면 렌더링
    return templates.TemplateResponse(request, 'board.html', {
        'board_list' : results
    })

# 글 추가 페이지로 이동 
@app.get('/add')
def add_page(request:Request):
    print('/add 실행')
    return templates.TemplateResponse(request, 'add.html')

# 게시글 추가
@app.post('/api/add')
def add_form(board: Board = Form(), session:Session = Depends(get_session)):
    print('/api/add 실행')
    print(board)
    try:
        sql = text('''
            insert into board
            (title, detail, author, date, view, `like`)
            values (:title, :detail, :author, :date, 0, 0)
        ''')
        session.execute(sql, {
            "title" : board.title,
            "detail" : board.detail,
            "author" : board.author,
            "date" : board.date
        })
        session.commit()
    except Exception as e:
        print(e)

    return RedirectResponse(url='/board', status_code=303)

# 상세 내용 보기 
@app.get('/detail/{id}')
def detail_page(id:int , request:Request, session:Session = Depends(get_session) ):
    print('/detail/{id} 실행', id)
    sql = text('''
        select * from board 
        where id = :id
    ''')
    result = session.execute(sql, {'id' : id}).mappings().fetchone()

    return templates.TemplateResponse(request, 'detail.html', {
        "board" : result
    })

# 글 수정 페이지로 이동 
@app.get('/update/{id}')
def update_page(id:int, request:Request, session:Session = Depends(get_session)):
    sql = text ('''
        select * from board
        where id = :id
    ''')
    result = session.execute(sql, {'id' : id}).mappings().first()

    return templates.TemplateResponse(request, 'update.html',{
        'board' : result 
    })

# 글 수정 처리 API (POST 방식)
@app.post('/api/update')
def api_update(board: Board = Form(),session:Session = Depends(get_session)):
    print('/api/update 실행' , board)
    try:
        sql = text('''
        update board 
        set
            title = :title,
            detail = :detail
        where 
            id = :id
        ''')
        session.execute(sql, {
            'id' : board.id,
            'title' : board.title,
            'detail' : board.detail
        })
        session.commit()
    except Exception as e:
        print(e)

    return RedirectResponse(url='/board', status_code=303)

# 글 삭제 처리 API
@app.get ('/api/delete/{id}')
def api_delete(id:int, session:Session = Depends(get_session)):
    print('/api/delete 실행' , id)
    try:
        sql = text('''
            delete from board
            where id = :id    
        ''')
        session.execute(sql, {'id' : id})
        session.commit()
    except Exception as e:
        print(e)

    return RedirectResponse(url='/board', status_code=303)

if __name__ == "__main__" :
    import uvicorn 

    uvicorn.run("api:app", port=8085, reload=True, host="0.0.0.0")