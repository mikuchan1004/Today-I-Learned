# pip install sqlmodel

from sqlmodel import create_engine, Session, SQLModel
from fastapi import FastAPI, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy import text

# SQLModel.metadata에 등록 시킨다
# 그러면 crate_all로 테이블이 없으면 만들어 준다
# Emp3(SQLModel, table=True) 이것 둘 다 적으면 자동으로 만들어준다.
from DTO.EmpDTO import Emp3
from DTO.DeptDTO import Dept3

app = FastAPI()
templates = Jinja2Templates(directory='templates/')


# DB+driver://id:pw:@ip:port/database
DATABASE_URL = 'mysql+pymysql://root:human1234$@127.0.0.1:3306/human'
engine = create_engine(DATABASE_URL, echo=True)
# engine = create_engine(
#     DATABASE_URL, 
#     echo=True,
#     execution_options = {
#         'isolation_level' : 'AUTOCOMMIT' # rollback 안됨.
#     }
# )

def get_session():
    with Session(engine) as session : 
        yield session
        session.commit()

@app.on_event('startup')
def on_startup() :
    SQLModel.metadata.create_all(engine)

@app.get('/emp/deptno')
def emp_list_deptno(
    request: Request,
    deptno: int,
    session: Session = Depends(get_session)
):
    emp_list = []
    try:
        # text : sql문을 실행하기 전에 미리 컴파일 해둔다
        sql = text('''
            select * 
            from emp3
            where deptno = :deptno
        ''')

        result = session.execute(sql, {'deptno':deptno})
        # emp_list = result.fetchall() 
        emp_list = result.mappings().fetchall() 
        print(emp_list)
        
    except Exception as e:
        print(e)

    return templates.TemplateResponse(request, 'list.html',{
                'emp_list' : emp_list
            })

@app.get('/emp/update/sal')
def update_sal(
    per:int,
    session : Session = Depends(get_session)
):
  upsal = 1 + (per / 100) 
  print('upsal' , upsal)

  try : 
    sql = text ('''
            update emp3
            set sal = sal * :upsal
            where deptno = 30
        ''')
    result = session.execute(sql, {'upsal':upsal})
    
    print('실행 결과로 영향을 받은 row 수 :' , result.rowcount)
  except Exception as e : 
        print('ERR' , e)
        session.rollback()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("02_sqlmodel:app" , port=8000, reload=True, host="0.0.0.0")