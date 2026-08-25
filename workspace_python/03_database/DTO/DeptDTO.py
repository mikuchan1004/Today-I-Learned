# 이 파일에 적힌 주석들은 전부 다 Google Gemini가 달아주었습니다
from sqlmodel import SQLModel, Field  # SQLModel(ORM)과 Field(테이블 컬럼 속성 정의) 임포트
from typing import Optional            # NULL 허용 타입을 위한 Optional 모듈 임포트

# table=True: DB에 이 클래스 구조와 동일한 'dept3' 테이블을 매핑하여 생성
class Dept3(SQLModel, table=True):
    deptno: int = Field(primary_key=True)  # 부서 번호 (기본키 / PK)
    dname: str                             # 부서명 (필수 문자열)
    loc: str                               # 부서 위치 (필수 문자열)