from sqlmodel import SQLModel, Field
from typing import Optional

class Emp3 (SQLModel, table=True):
    # 없으면 클래스명이 테이블명이 된다.
    # __tablename__ = "emp"

    # empno : int = Field(primary_key=True) 
    empno : int | None = Field(
        default = None,  # auto_increment
        primary_key= True
    )
    ename : str 
    job : str
    # mgr : int | None = None
    mgr : Optional[int] = None
    hiredate : str
    sal : float
    # comm : float | None = None
    comm : Optional[float] = None
    deptno : int = Field(
        foreign_key='dept3.deptno'
    )