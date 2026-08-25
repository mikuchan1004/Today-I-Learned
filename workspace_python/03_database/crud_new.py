from sqlmodel import create_engine, Session, SQLModel
from fastapi import FastAPI, Depends, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy import text

# DTO 클래스 임포트
from DTO.EmpDTO import Emp3
from DTO.DeptDTO import Dept3

app = FastAPI()
templates = Jinja2Templates(directory='templates/')

# 데이터베이스 접속 정보
DATABASE_URL = 'mysql+pymysql://root:human1234$@127.0.0.1:3306/human'
engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session: 
        yield session
        session.commit()

@app.on_event('startup')
def on_startup():
    SQLModel.metadata.create_all(engine)

# 1. 통합 목록 페이지 (모달 팝업 포함)
@app.get('/crud')
def list(request: Request, session: Session = Depends(get_session)):
    print('/list 실행')
    sql = text('''
        select * from emp3
    ''')
    results = session.execute(sql).mappings().fetchall()
    return templates.TemplateResponse(request, 'crud.html', {
        'emp_list': results
    })

# 2. 사원 추가 API 
@app.post('/api/add')
def add_form(emp: Emp3 = Form(), session: Session = Depends(get_session)):
    print('/api/add 실행', emp)
    try:
        sql = text('''
            insert into emp3
            (empno, ename, job, mgr, hiredate, sal, comm, deptno)
            values (:empno, :ename, :job, :mgr, :hiredate, :sal, :comm, :deptno)
        ''')
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

    return RedirectResponse(url='/crud', status_code=303)

# 3. 사원 수정 처리 API
@app.post('/api/update')
def api_update(emp: Emp3 = Form(), session: Session = Depends(get_session)):
    print('/api/update 실행', emp)
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

    return RedirectResponse(url='/crud', status_code=303)

# 4. 사원 삭제 처리 API 
@app.get('/api/delete/{empno}')
def api_delete(empno: int, session: Session = Depends(get_session)):
    print('/api/delete 실행', empno)
    try:
        sql = text('''
            delete from emp3
            where empno = :empno
        ''')
        session.execute(sql, {'empno': empno})
        session.commit()
    except Exception as e:
        print(e)

    return RedirectResponse(url='/crud', status_code=303)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("crud_new:app", port=8085, reload=True, host="0.0.0.0")