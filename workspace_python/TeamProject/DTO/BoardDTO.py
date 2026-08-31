# ==============================================================================
# 데이터베이스 테이블 구조 겸 데이터 전달(DTO)용 모델 정의
# ==============================================================================
from sqlmodel import SQLModel, Field        # DB 테이블을 만들고 필드(컬럼) 세부 설정을 돕는 도구
from typing import Optional                  # 값이 비어있을 수도(None) 있음을 명시할 때 쓰는 도구
from pydantic import field_validator        # 데이터가 들어올 때 올바른지 검사하고 가공하는 검증 도구

# 'table=True'를 붙여서 이 클래스가 데이터베이스의 'board' 테이블 구조이자,
# 파이썬 안에서 데이터를 주고받는 DTO(Data Transfer Object) 역할을 동시에 수행하게 합니다.
class Board(SQLModel, table=True):
    
    # 1. 게시물 고유 번호 (Primary Key / 식별자)
    # int | None: 정수 숫자가 들어가거나 처음에는 비어있을 수 있음
    # primary_key=True: DB에서 각 게시글을 구분하는 제일 중요한 '주민등록번호' 역할 (DB가 1, 2, 3... 자동으로 부여)
    id : int | None = Field( 
        default = None,                      # 기본값은 비워둠 (DB가 번호를 알아서 채워주도록 함)
        primary_key = True                   # 기본키(Primary Key) 설정
    )

    # 2. 필수 입력 항목들 (제목, 내용, 작성자, 작성일)
    # str: 반드시 글자(문자열) 형태로 데이터가 들어와야 하는 칸들
    title : str                              # 글 제목 (필수 입력 항목)
    detail : str                             # 내용 (필수 입력 항목)
    author : str                             # 작성자 (필수 입력 항목)
    date: str                                # 작성일 (필수 입력 항목, 예: '2026-08-30')

    # 3. 기본값이 존재하는 수치 항목들 (조회수, 좋아요 수)
    # default = 0: 데이터가 들어오지 않아도 자동으로 숫자 0으로 세팅됨
    view : int | None = Field(
        default = 0                          # 조회수 기본값 0 지정
    )

    like : int | None = Field(
        default = 0                          # 좋아요 기본값 0 지정
    )

    # ==============================================================================
    # 4. 데이터 전처리 / 자동 검증기 (Validator)
    # ==============================================================================
    # 'view'와 'like' 칸에 데이터가 세팅되기 전(mode='before')에 이 함수가 자동으로 먼저 실행됩니다.
    @field_validator('view', 'like', mode='before')
    @classmethod
    def empty_to_zero(cls, value):
        # 폼에서 넘어온 값이 비어있거나(None), 공백만 들어간 빈 문자열('')인 경우 
        # 에러가 나지 않도록 숫자 0으로 깔끔하게 변환해서 반환해 줍니다.
        if value is None or (isinstance(value, str) and value.strip() == ''):
            return 0
        else:
            return value