from sqlmodel import create_engine, Session, SQLModel
from fastapi import FastAPI, Depends, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy import text
from typing import Optional # 빈 칸 허용을 위해 추가

from DTO.EmpDTO import Emp3
from DTO.DeptDTO import Dept3

app = FastAPI()
templates = Jinja2Templates(directory='templates/')

DATABASE_URL = 'mysql+pymysql://root:human1234$@127.0.0.1:3306/human'
engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session
        session.commit()

@app.on_event('startup')
def on_startup() :
    SQLModel.metadata.create_all(engine)

# EMP 테이블 전체 조회 페이지 
@app.get('/list')
def emp_list(request: Request, session: Session = Depends(get_session)):
    print('/list 실행')
    # DB에 직접 SELECT 쿼리를 날려서 목록을 가져옴 
    sql = text('select * from emp3')
    results = session.execute(sql).mappings().fetchall()
    return templates.TemplateResponse(request, 'list.html',{
        'emp_list' : results
    }) 

# EMP 테이블 추가 화면 이동 
@app.get('/add')
def add_emp(request:Request):
    print('/add 실행')
    return templates.TemplateResponse(request, 'add.html')

# EMP 테이블에 값을 추가하는 API
@app.post('/api/add')
def emp_add_form (
    request: Request,
    empno : int = Form(),
    ename : str = Form(),
    job : str = Form(),
    mgr : Optional[int] = Form(None),
    hiredate : str = Form(),
    sal : float = Form(),
    comm : Optional[float] = Form(None),
    deptno : int = Form(),
    session: Session = Depends(get_session)
):
    emp_list = []
    try :
        sql = text('''
            insert into emp3 
            (empno, ename, job, mgr, hiredate, sal, comm, deptno)
            values (:empno, :ename, :job, :mgr, :hiredate, :sal, :comm, :deptno )
        ''')

        session.execute(sql, {
            "empno" : empno,
            "ename" : ename,
            "job" : job,
            "mgr" : mgr,
            "hiredate" : hiredate,
            "sal" : sal,
            "comm" : comm,
            "deptno" : deptno
        })

        session.commit()
    
    except Exception as e :
        print(e)

#추가 완료 후 전체 페이지로 리다이렉트
    return RedirectResponse(url='/list' , status_code=303)

# 상세 정보 조회 라우트
@app.get('/detail/{empno}')
def detail_page(empno:int, request: Request ,  session: Session = Depends(get_session)):
    print('/datail/{empno} 실행,  empno:' , empno)
    sql = text('''
        select * from emp3
        where empno = :empno
         ''')
    result = session.execute(sql, {"empno" : empno}).mappings().first()
    return templates.TemplateResponse(request, 'detail.html',{
            'request' : request,
            'emp' : result
        }) 

# 수정 화면 이동 라우트
@app.get('/update/{empno}')
def update_page(empno:int, request: Request, session: Session = Depends(get_session)):
    print('/update/{empno} 실행 , empno:', empno )
    sql = text ('''
        select * from emp3
        where empno = :empno
    ''')
    result = session.execute(sql, {"empno" : empno }).mappings().first()
    return templates.TemplateResponse(request,'update.html', {
        'request' : request,
        'emp' : result
    })

# 테이블 수정처리 API 라우트 
@app.post('/api/update')
def emp_update_form(
    request: Request,  emp: Emp3 = Form(), session: Session = Depends(get_session)
):
    try:
        sql = text('''
            update emp3
            set 
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
        session.execute(sql, {
            'empno' : Emp3.empno,
            'ename' : Emp3.ename,
            'job' : Emp3.job,
            'mgr' : Emp3.mgr,
            'hiredate' : Emp3.hiredate,
            'sal' : Emp3.sal,
            'comm' : Emp3.comm,
            'deptno' : Emp3.deptno
        })
        
        session.commit()

    except Exception as e :
        print(e)

    # 수정 완료 후 전체 조회 페이지로 리다이렉트
    return RedirectResponse(url='/list' , status_code=303)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("03_crud:app" , port=8085, reload=True, host="0.0.0.0")