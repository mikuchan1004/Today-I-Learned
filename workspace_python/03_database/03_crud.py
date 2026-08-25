# 이 파일에 적혀있는 주석은 전부 다 Google Gemini가 달아주었습니다.
# [1] 데이터베이스 ORM 및 웹 프레임워크 필수 모듈 임포트
from sqlmodel import create_engine, Session, SQLModel  # DB 연결 및 테이블 관리를 위한 SQLModel 모듈
from fastapi import FastAPI, Depends, Request, Form    # FastAPI 기본 기능, 의존성 주입(Depends), 요청 객체(Request), 폼 데이터 처리(Form)
from fastapi.templating import Jinja2Templates         # HTML 템플릿(Jinja2) 연동을 위한 모듈
from fastapi.responses import RedirectResponse         # 작업 완료 후 다른 페이지로 이동(리다이렉트)시키는 모듈
from sqlalchemy import text                           # 원시 SQL(Raw SQL) 문장을 안전하게 실행하기 위한 함수

# [2] 사용자 정의 데이터 모델(DTO) 임포트
# SQLModel을 상속받아 만든 사원(Emp3) 및 부서(Dept3) 데이터 구조 정의 객체
from DTO.EmpDTO import Emp3
from DTO.DeptDTO import Dept3

# [3] FastAPI 애플리케이션 및 템플릿 설정
app = FastAPI()  # FastAPI 웹 서버 인스턴스 생성
templates = Jinja2Templates(directory='templates/')  # HTML 파일들이 위치한 폴더 경로 지정

# [4] 데이터베이스 접속 설정 (MySQL)
# 접속 정보 형식: mysql+driver://계정:비밀번호@IP주소:포트번호/DB이름
DATABASE_URL = 'mysql+pymysql://root:human1234$@127.0.0.1:3306/human'

# create_engine: DB 연결 엔진 생성 (echo=True로 설정 시 터미널에 실행되는 SQL 쿼리 로그가 표시됨)
engine = create_engine(DATABASE_URL, echo=True)

# [5] DB 세션 생성 및 자동 관리 함수 (의존성 주입용)
def get_session():
    with Session(engine) as session: 
        yield session       # 라우터 함수에 DB 세션을 전달
        session.commit()    # 요청 처리가 무사히 끝나면 변경사항을 DB에 최종 반영(커밋)

# [6] 서버 시작 시 자동 실행되는 이벤트
@app.on_event('startup')
def on_startup():
    # SQLModel에 등록된 클래스 구조를 기반으로 DB에 테이블이 없으면 자동 생성
    SQLModel.metadata.create_all(engine)

# ==========================================
# [라우터 영역] 페이지 이동 및 API 기능 정의
# ==========================================

# 1. 사원 전체 목록 조회 페이지
@app.get('/list')
def list(request: Request, session: Session = Depends(get_session)):
    print('/list 실행')
    # 전체 사원 조회를 위한 SQL 문 작성
    sql = text('''
        select * from emp3
    ''')
    # .mappings().fetchall(): 쿼리 결과를 딕셔너리 형태로 변환하여 전체 목록을 가져옴
    results = session.execute(sql).mappings().fetchall()
    
    # list.html 파일에 emp_list 변수 이름으로 조회 결과를 전달하여 화면 렌더링
    return templates.TemplateResponse(request, 'list.html', {
        'emp_list': results
    })

# 2. 사원 등록 폼 페이지로 이동
@app.get('/add')
def add_page(request: Request):
    print('/add 실행')
    # 단순 추가 입력 양식 화면(add.html)을 보여줌
    return templates.TemplateResponse(request, 'add.html')

# 3. 사원 등록 처리 API (POST 방식)
@app.post('/api/add')
def add_form(emp: Emp3 = Form(), session: Session = Depends(get_session)):
    """
    emp: Emp3 = Form() -> HTML <form> 태그에서 전송된 값을 Emp3 DTO 객체 형태로 자동으로 매핑받음
    """
    print('/api/add 실행')
    print(emp)
    try:
        # SQL 파라미터 바인딩 방식(:variable)을 사용하여 SQL 인젝션 공격 방지 및 데이터 전달
        sql = text('''
            insert into emp3
            (empno, ename, job, mgr, hiredate, sal, comm, deptno)
            values (:empno, :ename, :job, :mgr, :hiredate, :sal, :comm, :deptno)
        ''')
        
        # 쿼리 실행 및 DTO의 필드 값 할당
        session.execute(sql, {
            'empno': emp.empno,
            'ename': emp.ename,   
            'job': emp.job,
            'mgr': emp.mgr,
            'hiredate': emp.hiredate,
            'sal': emp.sal,
            'comm': emp.comm,
            'deptno': emp.deptno
        })
        session.commit()  # DB에 입력 사항 저장
    except Exception as e:
        print(e)  # 에러 발생 시 콘솔에 출력

    # 추가 완료 후 HTTP 303(See Other) 상태 코드로 전체 목록 페이지('/list')로 이동
    return RedirectResponse(url='/list', status_code=303)

# 4. 사원 상세 정보 페이지 조회
@app.get('/detail/{empno}')
def detail_page(empno: int, request: Request, session: Session = Depends(get_session)):
    """
    empno: int -> URL 경로 파라미터로 넘어온 사원번호를 정수형으로 전달받음
    """
    print('/detail/{empno} 실행', empno)
    sql = text('''
        select * from emp3
        where empno = :empno
    ''')
    # .mappings().fetchone(): 조건에 맞는 데이터 1건을 딕셔너리 형태로 가져옴
    result = session.execute(sql, {'empno': empno}).mappings().fetchone()

    # detail.html에 emp 변수로 사원 정보 1건을 전달
    return templates.TemplateResponse(request, 'detail.html', {
        'emp': result 
    })

# 5. 사원 정보 수정 페이지로 이동
@app.get('/update/{empno}')
def update_page(empno: int, request: Request, session: Session = Depends(get_session)):
    print('/update/{empno} 실행', empno)
    sql = text('''
        select * from emp3
        where empno = :empno
    ''')
    # 기존 사원 데이터를 불러와서 수정 입력 창에 미리 뿌려주기 위해 조회
    result = session.execute(sql, {'empno': empno}).mappings().first()

    # update.html에 기존 정보 전달
    return templates.TemplateResponse(request, 'update.html', {
        'emp': result 
    })

# 6. 사원 정보 수정 처리 API (POST 방식)
@app.post('/api/update')
def api_update(emp: Emp3 = Form(), session: Session = Depends(get_session)):
    print('/api/update 실행', emp)
    try:
        sql = text('''
            update emp3
            set 
                empno = :empno,
                ename = :ename,
                job = :job,
                mgr = :mgr, 
                hiredate = :hiredate,
                sal = :sal,
                comm = :comm,
                deptno = :deptno
            where 
                empno = :empno
        ''')
        
        # 수정 폼에서 입력받은 새로운 값들로 DB 업데이트 실행
        session.execute(sql, {
            'empno': emp.empno,
            'ename': emp.ename,
            'job': emp.job,
            'mgr': emp.mgr,
            'hiredate': emp.hiredate,
            'sal': emp.sal,
            'comm': emp.comm,
            'deptno': emp.deptno
        })
        session.commit()

    except Exception as e:
        print(e)

    # 수정 완료 후 전체 목록 페이지('/list')로 이동
    return RedirectResponse(url='/list', status_code=303)

# 7. 사원 정보 삭제 처리 API (GET 방식)
@app.get('/api/delete/{empno}')
def api_delete(empno: int, session: Session = Depends(get_session)):
    print('/api/delete 실행', empno)
    try:
        sql = text('''
            delete from emp3
            where empno = :empno
        ''')
        # 해당 사원번호를 가진 레코드 삭제 실행
        session.execute(sql, {'empno': empno})
        session.commit()
    except Exception as e:
        print(e)

    # 삭제 완료 후 전체 목록 페이지('/list')로 이동
    return RedirectResponse(url='/list', status_code=303)

# ==========================================
# [메인 실행 영역] Uvicorn 백엔드 서버 구동
# ==========================================
if __name__ == "__main__":
    import uvicorn
    
    # Uvicorn 서버 실행
    # "파일이름:FastAPI객체명" -> "03_crud:app"
    # host="0.0.0.0": 외부 접속 허용
    # port=8085: 웹 서버가 사용할 포트 번호 (8000번 대신 지정)
    # reload=True: 코드 변경 시 서버 자동 재시작 (개발용 옵션)
    uvicorn.run("03_crud:app", port=8085, reload=True, host="0.0.0.0")