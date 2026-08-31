# ==============================================================================
# 1. 필요한 외부 도구(라이브러리) 가져오기
# ==============================================================================
from sqlmodel import create_engine, Session, SQLModel  # DB 연결 및 데이터 구조를 다루는 도구
from fastapi import FastAPI, Depends, Request, Form    # 웹 서버 제작, 데이터 받기, 자동 의존성 주입 도구
from fastapi.templating import Jinja2Templates         # HTML 화면 파일(템플릿)을 연결해 주는 도구
from fastapi.responses import RedirectResponse         # 작업 완료 후 다른 페이지로 사용자를 이동시키는 도구
from sqlalchemy import text                           # 파이썬 안에서 직접 SQL(DB 명령어)을 쓸 수 있게 해주는 도구

from DTO.BoardDTO import Board                        # 게시판 데이터 모양(규격)을 정의해 둔 객체 클래스

# ==============================================================================
# 2. 웹 서버 및 데이터베이스 기본 설정
# ==============================================================================
app = FastAPI()                                        # FastAPI 웹 서버 객체 생성 (프로그램의 메인 엔진)
templates = Jinja2Templates(directory='templates/')   # HTML 파일들이 저장된 폴더 경로 지정

# DB 접속 주소 (아이디:root / 비밀번호:human1234$ / IP:127.0.0.1 / DB이름:human)
DATABASE_URL = 'mysql+pymysql://root:human1234$@127.0.0.1:3306/human'

# DB 연결 엔진 생성 (echo=True로 설정하면 터미널에 실행되는 SQL 문장이 실시간으로 출력됨)
engine = create_engine(DATABASE_URL, echo=True)

# DB 연결 작업실(세션)을 만들어서 빌려주는 헬퍼 함수
def get_session():
    with Session(engine) as session:                  # DB 작업용 통로(세션)를 한 번 엽니다.
        yield session                                 # 요청 처리 동안 세션을 사용하도록 넘겨줍니다.
        session.commit()                              # 모든 작업이 무사히 끝나면 변경사항을 DB에 최종 저장합니다.

# 서버가 '시작'될 때 자동으로 1번만 실행되는 함수
@app.on_event('startup')
def on_startup():
    # SQLModel.metadata.drop_all(engine)              # [주의] 기존 DB 테이블을 싹 지우는 코드 (필요할 때만 주석 해제)
    SQLModel.metadata.create_all(engine)              # DB에 'board' 테이블이 없으면 모델 구조대로 새로 생성합니다.

# ==============================================================================
# 3. 웹 라우터 (각 URL 페이지 처리)
# ==============================================================================

# [R] 게시판 목록 페이지 (GET /board)
@app.get('/board')
def board(request: Request, session: Session = Depends(get_session)):
    print('/board 실행')
    
    # DB에서 모든 게시물 데이터를 가져오는 SQL 문장
    sql = text('''
        select * from board
    ''')

    # 실행 결과를 파이썬 딕셔너리 형태로 싹 다 끌어옵니다.
    results = session.execute(sql).mappings().fetchall()

    # board.html 파일에 'board_list'라는 이름으로 조회한 글 목록 데이터를 전달하며 화면을 그려줍니다.
    return templates.TemplateResponse(request, 'board.html', {
        'board_list' : results
    })

# [C] 글 추가 입력 작성 페이지로 이동 (GET /add)
@app.get('/add')
def add_page(request: Request):
    print('/add 실행')
    # 단순히 글 작성 양식인 add.html 화면만 보여줍니다.
    return templates.TemplateResponse(request, 'add.html')

# [C] 실제 글 등록 처리 API (POST /api/add)
@app.post('/api/add')
def add_form(board: Board = Form(), session: Session = Depends(get_session)):
    print('/api/add 실행')
    print(board)
    try:
        # 사용자가 입력한 값들을 DB의 board 테이블에 새로 집어넣는 SQL 문
        # (조회수 view와 좋아요 like는 기본값인 0으로 세팅)
        sql = text('''
            insert into board
            (title, detail, author, date, view, `like`)
            values (:title, :detail, :author, :date, 0, 0)
        ''')
        
        # HTML 폼에서 넘어온 board 객체의 데이터들을 SQL 인자에 바인딩해서 실행
        session.execute(sql, {
            "title" : board.title,
            "detail" : board.detail,
            "author" : board.author,
            "date" : board.date
        })
        session.commit()                              # DB 저장 확정
    except Exception as e:
        print(e)                                      # 에러 발생 시 콘솔에 출력

    # 글 저장이 끝나면 다시 게시판 목록 페이지('/board')로 화면을 튕겨(리다이렉트) 줍니다.
    return RedirectResponse(url='/board', status_code=303)

# [R] 게시글 상세 읽기 페이지 (GET /detail/{id})
@app.get('/detail/{id}')
def detail_page(id: int, request: Request, session: Session = Depends(get_session)):
    print('/detail/{id} 실행', id)
    
    # URL로 전달된 글 번호(id)에 해당하는 특정 게시물 1개만 조회
    sql = text('''
        select * from board 
        where id = :id
    ''')
    
    # 1개의 데이터만 딕셔너리로 가져옵니다.
    result = session.execute(sql, {'id' : id}).mappings().fetchone()

    # detail.html 파일에 조회한 글 정보('board')를 담아서 전달합니다.
    return templates.TemplateResponse(request, 'detail.html', {
        "board" : result
    })

# [U] 글 수정 작성 페이지로 이동 (GET /update/{id})
@app.get('/update/{id}')
def update_page(id: int, request: Request, session: Session = Depends(get_session)):
    # 수정하기 전, 기존에 입력되어 있던 글 내용을 가져오기 위해 1개 데이터 조회
    sql = text('''
        select * from board
        where id = :id
    ''')
    result = session.execute(sql, {'id' : id}).mappings().first()

    # 기존 글 정보를 담아서 update.html(수정 폼)으로 보내줍니다.
    return templates.TemplateResponse(request, 'update.html', {
        'board' : result 
    })

# [U] 실제 글 수정 처리 API (POST /api/update)
@app.post('/api/update')
def api_update(board: Board = Form(), session: Session = Depends(get_session)):
    print('/api/update 실행', board)
    try:
        # 해당 id 번호를 가진 게시글의 제목(title)과 내용(detail)을 전달받은 새 데이터로 덮어씁니다.
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
        session.commit()                              # 수정 반영 확정
    except Exception as e:
        print(e)

    # 수정 완료 후 게시판 목록으로 이동
    return RedirectResponse(url='/board', status_code=303)

# [D] 실제 글 삭제 처리 API (GET /api/delete/{id})
@app.get('/api/delete/{id}')
def api_delete(id: int, session: Session = Depends(get_session)):
    print('/api/delete 실행', id)
    try:
        # 해당 id 번호를 가진 게시글을 DB에서 삭제하는 SQL 문
        sql = text('''
            delete from board
            where id = :id    
        ''')
        
        session.execute(sql, {'id' : id})
        session.commit()                              # 삭제 확정
    except Exception as e:
        print(e)

    # 삭제 후 게시판 목록으로 이동
    return RedirectResponse(url='/board', status_code=303)

# ==============================================================================
# 4. 서버 직접 실행부 (python api.py로 실행할 때 작동)
# ==============================================================================
if __name__ == "__main__":
    import uvicorn 
    # 포트 8085로 서버를 열고, 코드가 수정되면 자동으로 서버를 재시작(reload=True)합니다.
    uvicorn.run("api:app", port=8085, reload=True, host="0.0.0.0")