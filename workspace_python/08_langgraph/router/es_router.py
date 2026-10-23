"""
[엘라스틱서치/임베딩 전처리 라우터]
영화 추천 및 검색 시스템 구축을 위한 데이터 전처리 모듈입니다.
1. CSV 파일(영화, 태그, 평점) 로드 및 미리보기
2. 데이터 정합성 검증(결측치, ID 일치 여부, 평점 범위)
3. 텍스트 결합 (영화 제목 + 장르 리스트 + 태그 리스트 -> 검색용 통합 텍스트)
4. 텍스트 청킹 (Sliding Window 방식으로 고정 크기 분할)
5. Gemini/GPT 임베딩 연동 준비
"""

from fastapi import APIRouter
import traceback 
from pathlib import Path
import util
import pandas as pd 
from typing import Any, Literal

# Swagger UI에서 '엘라스틱서치' 태그 그룹으로 묶이도록 라우터 설정
router = APIRouter(tags=["엘라스틱서치"])


# ==============================================================================
# 1. CSV 데이터 미리보기 API
# ==============================================================================
@router.get('/read/head')
def read(fileName: Literal['movies.csv', 'tags.csv', 'ratings.csv'] = 'movies.csv'):
    """
    선택한 CSV 파일의 상위 5개 행(Head)을 JSON 형태로 반환하는 API
    - Literal: 허용할 파일명만 타입 힌트로 제한하여 오타 방지 및 Swagger UI 드롭다운 제공
    """
    frame = util.load_csv(fileName)
    if frame is None:
        return {'ERROR': '파일을 불러오지 못했습니다.'}

    # [데이터 변환 파이프라인]
    # 1. frame.head() : 상위 5개 행 추출 (기본값: 5)
    # 2. astype(object) : int64, float64 등 특수 타입을 파이썬 기본 객체(int, float 등)로 형변환
    #                     (FastAPI의 JSON 직렬화 시 발생할 수 있는 에러 방지)
    # 3. to_dict(orient='records') : [{'col1': val1, 'col2': val2}, ...] 형태의 리스트-딕셔너리로 변환
    #    (참고: orient 기본값은 dict 형태라 인덱스가 최상위 키가 됨)
    preview = frame.head().astype(object).to_dict(orient='records')
    return preview


# ==============================================================================
# 2. 데이터 유효성 및 정합성 검증 API
# ==============================================================================
@router.get('/read/vaild')
def valid():
    """
    데이터셋 간의 외래키(movieId) 정합성과 평점(rating) 범위를 검증하는 API
    - 영화 목록(movies.csv)에 없는 영화 ID가 tags나 ratings에 존재하는지 체크
    """
    df_movies = util.load_csv('movies.csv')
    df_tags = util.load_csv('tags.csv')
    df_ratings = util.load_csv('ratings.csv')

    # dropna() : NaN(결측치) 제거
    notnull = df_movies['movieId'].dropna()

    # set(집합) 자료형을 활용하여 중복 제거 및 고유 ID 추출
    movie_ids = set(notnull)
    tag_ids = set(df_tags['movieId'].dropna())
    ratings_ids = set(df_ratings['movieId'].dropna())

    result = {}
    result['no_id'] = {}
    # 차집합(-) 연산: 영화 메타데이터에 등록되지 않은 movieId 개수 카운트
    result['no_id']['tags'] = len(tag_ids - movie_ids)
    result['no_id']['ratings'] = len(ratings_ids - movie_ids)

    # 평점 데이터의 최소값 및 최대값 확인 (예: 0.5 ~ 5.0)
    result['rating range'] = {}
    result['rating range']['min'] = float(df_ratings['rating'].min())
    result['rating range']['max'] = float(df_ratings['rating'].max())

    return result


# ==============================================================================
# 3. 검색 및 임베딩을 위한 통합 텍스트 콘텐츠 생성 함수
# ==============================================================================
def makeContent():
    """
    영화의 메타데이터(제목, 장르, 사용자 태그)를 하나의 문자열(content_text)로 결합하는 핵심 전처리 함수
    반환값: ['movieId', 'title', 'list_genre', 'list_tag', 'content_text'] 컬럼을 갖는 DataFrame
    """
    df_movies = util.load_csv('movies.csv')
    df_tags = util.load_csv('tags.csv')

    # [Pandas 기본 개념]
    # DataFrame : 2차원 테이블 구조 (행과 열)
    # Series    : 1차원 배열 (DataFrame의 단일 컬럼)
    result = pd.DataFrame()
    result['movieId'] = df_movies['movieId']
    # 제목 컬럼: 문자열 변환 후 앞뒤 공백 제거
    result['title'] = df_movies['title'].astype(str).str.strip()

    # --- [장르 전처리] ---
    # 원본 데이터는 "Action|Adventure|Sci-Fi" 형식의 파이프(|) 구분자 문자열
    def parse_genre(genres):
        """파이프(|)로 연결된 장르 문자열을 리스트 형태로 분리"""
        genre_list = []
        # 빈 문자열이거나 장르가 명시되지 않은 경우 빈 리스트 반환
        if str(genres).strip() == '' or str(genres) == '(no genres listed)':
            return genre_list

        list_genre = str(genres).split('|')
        for genre in list_genre:
            # strip(): 앞뒤 공백 제거
            genre_list.append(genre.strip())

        return genre_list

    # map() : 단일 Series(컬럼)의 각 요소에 함수를 1:1 매핑 적용
    result['list_genre'] = df_movies['genres'].map(parse_genre)

    # --- [태그 전처리] ---
    # copy() : 원본 DataFrame의 메모리를 보존하고 독립적인 사본 생성
    tags = df_tags[['movieId', 'tag']].copy()

    # 태그 공백 제거 및 소문자 정규화 (결과를 다시 컬럼에 할당해야 반영됨)
    tags['tag'] = tags['tag'].astype(str).str.strip().str.lower()

    # 동일 영화에 동일 태그가 중복 달린 경우 1개만 남기고 제거
    tags = tags.drop_duplicates(['movieId', 'tag'])

    # [태그 그룹화 방법 2가지 비교]
    # 방법 A (반복문):
    #   movie_tags = {}
    #   for info in tags.to_dict(orient='records'):
    #       id, tag = info['movieId'], info['tag']
    #       if id not in movie_tags: movie_tags[id] = []
    #       movie_tags[id].append(tag)
    #
    # 방법 B (Pandas 최적화 - 아래 코드):
    #   1. tags.groupby('movieId') : movieId 기준으로 그룹핑
    #   2. ['tag'].agg(list)       : 각 그룹의 tag들을 파이썬 list로 집계
    #   3. to_dict()               : {movieId: [tag1, tag2, ...]} 딕셔너리로 변환
    movie_tags = tags.groupby('movieId')['tag'].agg(list).to_dict()

    # 영화 ID를 key로 조회하여 태그 리스트를 매핑 (태그가 없으면 빈 리스트 [] 반환)
    result['list_tag'] = df_movies['movieId'].map(lambda id: movie_tags.get(id, []))

    # --- [검색용 통합 텍스트 컬럼 생성] ---
    # 파이썬 리스트는 '+' 연산자로 병합 가능: ['Title'] + ['Action'] + ['fun'] -> ['Title', 'Action', 'fun']
    # apply(..., axis=1) : DataFrame의 행(row) 단위로 반복 연산 수행
    #   - axis=0 : 열(컬럼) 방향 (위 -> 아래)
    #   - axis=1 : 행(레코드) 방향 (왼쪽 -> 오른쪽)
    result['content_text'] = result.apply(
        lambda info: " ".join([info['title']] + info['list_genre'] + info['list_tag']).strip(),
        axis=1
    )

    # reset_index(drop=True) : 가공 과정에서 어긋날 수 있는 인덱스를 0부터 다시 순차 번호로 초기화
    return result.reset_index(drop=True)


@router.get('/make/content')
def content():
    """가공된 영화 통합 데이터(makeContent) 상위 10건을 확인하는 API"""
    dataFrame = makeContent()
    return dataFrame.head(10).to_dict(orient='records')


# ==============================================================================
# 4. 텍스트 청킹(Chunking) - 슬라이딩 윈도우 분할
# ==============================================================================
def makeChunk():
    """
    통합 텍스트(content_text)를 LLM 임베딩 및 벡터 검색에 적합하도록 일정 크기로 자르는(Chunking) 함수
    - Sliding Window 기법을 사용하여 문맥 유실을 방지하기 위해 overlap(겹침) 구간을 둠
    """
    size_chunk = 50   # 한 청크당 최대 글자 수 (Window 크기)
    overlap: int = 15 # 앞선 청크와 겹쳐서 가져갈 글자 수 (문맥 보존용)
    
    # 타입 힌트: 딕셔너리들을 담은 리스트
    chunks: list[dict[str, Any]] = []

    dataFrame = makeContent()
    content = dataFrame.to_dict(orient="records")

    # 다음 청크 시작 위치로 이동할 간격 (Step = ChunkSize - Overlap)
    # 예: size=50, overlap=15 -> 35글자씩 전진
    step = size_chunk - overlap

    for info in content:
        text = info.get('content_text', '').strip()
        if not text:
            continue

        # range(시작, 끝, 간격) : step만큼 건너뛰며 청크 시작 인덱스 생성
        for idx, idx_start in enumerate(range(0, len(text), step)):
            # [주의: 슬라이싱 범위 수정]
            # text[idx_start : idx_start + size_chunk]로 잘라야 지정한 길이(50자)만큼 슬라이싱됨
            chunk = text[idx_start : idx_start + size_chunk]
            if chunk:
                chunks.append({
                    'movieId': int(info['movieId']),
                    'title': str(info['title']),
                    'genres': list(info['list_genre']),
                    'tags': list(info['list_tag']),
                    'content': chunk,
                    'chunk_index': idx  # 해당 영화 내에서 몇 번째 청크인지 식별
                })

    # [주의: return 위치 수정]
    # for info in content 루프가 완전히 끝난 뒤 모든 영화의 청크를 반환해야 함
    return chunks


@router.get('/make/chunk')
def chunk():
    """생성된 청크 목록 중 앞쪽 10개만 미리보기로 반환하는 API"""
    return makeChunk()[0:10]


# ==============================================================================
# 5. 임베딩 모델 연동 스텁 (향후 구현 영역)
# ==============================================================================
def embedding_with_gemini(data):
    """Google Gemini 임베딩 모델(예: text-embedding-004)을 호출하여 벡터를 생성할 함수"""
    pass

def embedding_with_gpt(data):
    """OpenAI GPT 임베딩 모델(예: text-embedding-3-small)을 호출하여 벡터를 생성할 함수"""
    pass