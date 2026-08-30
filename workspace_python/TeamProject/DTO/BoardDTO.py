from sqlmodel import SQLModel, Field        # SQLModel 기반 클래스 및 필드 설정 함수
from typing import Optional                  # NULL 값을 허용하는 타잎 지정 모듈
from pydantic import field_validator        # 데이터 검증 및 변환(전처리)용 밸리데이터

class  Board(SQLModel, table=True):
    # 게시물 ID
    id : int | None = Field( 
        default = None, # 기본값으로 None 지정 
        primary_key = True # 기본키 설정
    )
    title : str # 제목 (필수 입력 항목)

    detail : str # 내용 (필수 입력 항목)

    author : str # 작성자 (필수 입력 항목)

    date: str # 작성일 (필수 입력 항목)

    # 조회수
    view : int | None = Field(
        default = 0 # 기본값으로 0 지정 
    )

    # 좋아요 
    like : int | None = Field(
        default = 0 # 기본값으로 0 지정
    )

    @field_validator('view' , 'like' , mode='before')
    @classmethod
    def empty_to_zero(cls, value):
        # None이거나, 문자열인데 공백을 제거했을 때 빈 값인 경우 0으로 변환
        # by Google Gemini 
        if value is None or (isinstance(value, str) and value.strip() == ''):
            return 0
        else:
            return value

