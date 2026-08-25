# 이 파일에  적힌 주석들은 전부 다 Google Gemini가 달아주었습니다.
from sqlmodel import SQLModel, Field        # SQLModel 기반 클래스 및 필드 설정 함수
from typing import Optional                  # NULL 값을 허용하는 타잎 지정 모듈
from pydantic import field_validator        # 데이터 검증 및 변환(전처리)용 밸리데이터

class Emp3(SQLModel):
    # 별도로 __tablename__을 명시하지 않으면 클래스 이름인 'emp3'가 테이블명이 됩니다.
    # __tablename__ = "emp"

    # 사원번호: 기본키(PK) 설정 및 Auto Increment / 선택 입력을 위해 기본값 None 지정
    empno: int | None = Field(
        default=None,  # 기본값 None 설정 (DB 자동 증가 키 등록 시 사용)
        primary_key=True  # 기본키(Primary Key) 설정
    )
    ename: str   # 사원명 (필수 입력 항목)
    job: str     # 직책명 (필수 입력 항목)
    
    # 상사 사원번호: 상사가 없는 경우(NULL)가 있으므로 Optional[int] 처리
    mgr: Optional[int] = None
    
    hiredate: str   # 고용일 / 입사일 (문자열 형태)
    sal: float      # 급여 (실수형 숫자)
    
    # 보너스/커미션: 보너스가 없는 경우(NULL)가 있으므로 Optional[float] 처리
    comm: Optional[float] = None
    
    # 부서번호: dept3 테이블의 deptno 컬럼을 참조하는 외래키(FK) 설정
    deptno: int = Field(
        foreign_key='dept3.deptno'
    )
    # =========================================================================
    # [폼 데이터 파싱 처리기]
    # HTML <form>에서 숫자 필드를 비워두고 전송하면 빈 문자열("")이 전송되는데,
    # Pydantic이 이를 int/float로 형변환하려다 에러(ValidationError)를 일으키는 것을 방지
    # =========================================================================
    @field_validator('comm', 'mgr', mode='before')
    @classmethod 
    def empty_to_none(cls, value):
        # mode='before': 데이터 타입 검사 전(전처리 단계)에 가장 먼저 실행됨
        if value == '':
            return None  # 빈 문자열("")이 들어오면 None(NULL)으로 바꾸어 타입 에러 예방
        else:
            return value # 값이 채워져 있으면 그대로 넘겨줌
    
    # 아래는 모델 전체 필드를 전처리하는 옛 방식 예시 (참고용 주석)
    # @model_validator(mode='before')
    # @classmethod
    # def empty_to_none(cls, value):
    #     print(value,  value if value != "" else None)
    #     return value if value != "" else None