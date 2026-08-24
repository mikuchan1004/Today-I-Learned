import sqlite3

def create_dept():
    connect = sqlite3.connect('sqlite.db')
    cursor = connect.cursor()

    cursor.execute('''
        create table if not exists dept (
        deptno integer primary key,
        dname text not null,
        loc text 
        )
    ''')

    connect.commit()
    connect.close()


def insert_dept():
    connect = sqlite3.connect('sqlite.db')
    cursor = connect.cursor()

# SQL Injection 공격 방지
    cursor.execute('''
        insert into dept (deptno, dname, loc)    
        values (?, ?, ?)
    ''', (10, '1강의실', '천안'))
    
    cursor.execute('''
        insert into dept (deptno, dname, loc)    
        values (?, ?, ?)
    ''', (20, '2강의실', '수원'))
    
    cursor.execute('''
        insert into dept (deptno, dname, loc)    
        values (?, ?, ?)
    ''', (30, '3강의실', '서울'))

    # 가장 최근의 cursor가 영향을 끼친 열의 수 
    print('수정 개수 : ' , cursor.rowcount)

    connect.commit()
    connect.close()

def select_dept():
    connect = sqlite3.connect('sqlite.db')
    cursor = connect.cursor()

    cursor.execute('''
        select deptno, dname, loc
        from dept    
    ''')
        
    rows = cursor.fetchall()
    print('fetchall 결과')
    print(rows)

    connect.close()

def select_dept_20():
    connect = sqlite3.connect('sqlite.db')
    cursor = connect.cursor()

    cursor.execute('''
        select deptno, dname, loc
        from dept 
        where deptno = ?   
    ''', (20,))
    # cursor.execute('''
    #     select deptno, dname, loc
    #     from dept 
    # ''')

    # 결과 하나만 구할 때
    # 결과가 여러개라도 하나만 가져온다 (에러 없음)
    rows = cursor.fetchone()
    print('fetchone 결과')
    print(rows)

    connect.close()

def select_dict():
    connect = sqlite3.connect('sqlite.db')
    connect.row_factory = sqlite3.Row
    cursor = connect.cursor()

    cursor.execute('''
        select deptno, dname, loc
        from dept 
        where deptno = ?   
    ''', (20,))
    # cursor.execute('''
    #     select deptno, dname, loc
    #     from dept 
    # ''')

    # 결과 하나만 구할 때
    # 결과가 여러개라도 하나만 가져온다 (에러 없음)
    rows = cursor.fetchone()
    print('fetchone 결과')
    print(dict(rows))

    connect.close()


# create_dept()
# insert_dept()
# select_dept()
# select_dept_20()
# select_dict()

def select_all_dict():
    connect = sqlite3.connect('sqlite.db')
    connect.row_factory = sqlite3.Row
    cursor = connect.cursor()

    cursor.execute('''
        select deptno, dname, loc
        from dept    
    ''')
        
    rows = cursor.fetchall()
    print('fetchall 결과')
    print(rows)

    result = []
    for row in rows:
        result.append(dict(row))
    print(result)

    result2 = [dict(row) for row in rows]
    print(result2)

    connect.close()

# select_all_dict()

from pydantic import BaseModel
class DeptDTO(BaseModel):
    deptno : int
    dname : str
    loc : str 

def select_all_class():
    connect = sqlite3.connect('sqlite.db')
    connect.row_factory = sqlite3.Row
    cursor = connect.cursor()

    cursor.execute('''
        select deptno, dname, loc
        from dept    
    ''')
        
    rows = cursor.fetchall()

    result = [DeptDTO(**dict(row)) for row in rows]
    print(result)

    connect.close()

# select_all_class()

def update_dept():
    connect = sqlite3.connect('sqlite.db')
    cursor = connect.cursor()

    # cursor.execute('''
    #     update dept
    #     set dname = ?
    #     where deptno = ? 
    # ''', ('좋은 강의실' , '10'))
    cursor.execute('''
        update dept
        set dname = ?
    ''', ('좋은 강의실',))
    
    # 가장 최근의 cursor가 영향을 끼친 열의 수 
    print('수정 개수 : ' , cursor.rowcount)

    connect.commit()
    connect.close()

# update_dept()

def update_with():
    # connect = sqlite3.connect('sqlite.db')
    # 성공하면 commit, 실패하면 rollback하고 close까지 자동으로
    with sqlite3.connect('sqlite.db') as connect:
        cursor = connect.cursor()

    cursor.execute('''
        update dept
        set dname = ?
    ''', ('좋은 강의실',))
    
    # 가장 최근의 cursor가 영향을 끼친 열의 수 
    print('수정 개수 : ' , cursor.rowcount)

    # connect.commit()
    # connect.close()

update_with()
