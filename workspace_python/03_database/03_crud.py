from sqlmodel import create_engine, Session, SQLModel
from fastapi import FastAPI, Depends, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy import text

# SQLModel.metadata에 등록 시킨다
# 그러면 crate_all로 테이블이 없으면 만들어 준다
# Emp3(SQLModel, table=True) 이것 둘 다 적으면 자동으로 만들어준다.
from DTO.EmpDTO import Emp3
from DTO.DeptDTO import Dept3

app = FastAPI()
templates = Jinja2Templates(directory='templates/')

# 데이터베이스 접속 정보
DATABASE_URL = 'mysql+pymysql://root:human1234$@127.0.0.1:3306/human'
engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session : 
        yield session
        session.commit()

@app.on_event('startup')
def on_startup() :
    SQLModel.metadata.create_all(engine)

@app.get('/list')
def list(request: Request,session : Session = Depends(get_session)):
    print('/list 실행')
    sql = text ('''
        select * from emp3
    ''')
    results = session.execute(sql).mappings().fetchall()
    return templates.TemplateResponse(request, 'list.html',{
        'emp_list' : results
    })

#추가 페이지로 이동 
@app.get('/add')
def add_page(request: Request):
    print('/add 실행')
    return  templates.TemplateResponse(request, 'add.html')

# 테이블에 내용을 추가하는 API 
@app.post('/api/add')
def add_form(emp: Emp3 = Form(), session : Session = Depends(get_session)):
    print('/api/add 실행')
    print(emp)
    try:
        # text : sql문을 실헹하기 전에 먼저 컴파일 해둔다 
        sql = text ('''
                insert into emp3
                (empno, ename, job, mgr, hiredate, sal,  comm, deptno)
                values (:empno, :ename, :job, :mgr, :hiredate, :sal, :comm, :deptno)
            ''')
        session.execute(sql, {
            'empno' : emp.empno,
            'ename' : emp.ename,   
            'job' : emp.job,
            'mgr' : emp.mgr,
            'hiredate' : emp.hiredate,
            'sal' : emp.sal,
            'comm' : emp.comm,
            'deptno' : emp.deptno
        })
        session.commit()
    except Exception as e :
        print(e)

    #  추가 완료 후 전체 조회 페이지로 이동
    return RedirectResponse(url = '/list' , status_code=303)

# 사원의 상세 정보 조회
@app.get('/detail/{empno}')
def detail_page(empno:int, request:Request, session : Session = Depends(get_session)):
    print('/detail/{empno} 실행' , empno)
    sql = text ('''
        select * from emp3
        where empno = :empno
    ''')
    result =session.execute(sql, {'empno' : empno}).mappings().fetchone()

    return templates.TemplateResponse(request, 'detail.html',{
        'emp' : result 
    })

#  테이블 수정 페이지 이동 라우트
@app.get('/update/{empno}')
def update_page (empno: int, request: Request, session:Session = Depends(get_session)):
    print('/update/{empno} 실행' , empno)
    sql = text ('''
        select * from emp3
        where empno = :empno
    ''')
    result = session.execute(sql, {'empno' : empno}).mappings().first()

    return templates.TemplateResponse(request, 'update.html', {
        'emp' : result 
    })

#  수정 처리 API 라우트
@app.post('/api/update')
def opi_update(emp: Emp3 = Form(), session : Session = Depends(get_session)):
    print('/api/update 실행' , emp)
    try:
        sql = text ('''
            update emp3
            set 
                empno = :empno,
                ename = :ename,
                job = :job,
                mgr = :mgr, 
                sal = :sal,
                comm = :comm,
                deptno = :deptno
            where 
                empno = :empno
        ''')
        session.execute(sql, {
            'empno' : emp.empno,
            'ename' : emp.ename,
            'job' : emp.job,
            'mgr' : emp.mgr,
            'sal' : emp.sal,
            'comm' : emp.comm,
            'deptno' : emp.deptno
        })
        session.commit()

    except Exception as e:
        print(e)

    #  수정  완료 후 전체 조회 페이지로 이동
    return RedirectResponse(url = '/list' , status_code=303)

# 삭제 처리 API 라우트 
@app.get('/api/delete/{empno}')
def api_delete(empno: int, session : Session = Depends(get_session)):
    print('/api/delete 실행' , empno)
    try:
        sql = text ('''
            delete from emp3
            where empno = :empno
        ''')
        session.execute(sql, {'empno': empno})

        session.commit()
    except Exception as e:
        print(e)

    # 삭제 완료 후 전체 조회 페이지로
    return RedirectResponse(url = '/list' , status_code=303)

# 메인 모듈 실행 시 Uvicorn 개발 서버 시작
if __name__ == "__main__":

    import uvicorn
    # uvicorn 서버 실행 (host: 0.0.0.0, port: 8000, 코드 변경 시 자동 재시작: reload=True)
    # 포트 번호 변경 (사유 : 8000번 포트를 디스코드가 쳐먹...아니 선점해서 사용 불가.)
    uvicorn.run("03_crud:app", port=8085, reload=True, host="0.0.0.0")