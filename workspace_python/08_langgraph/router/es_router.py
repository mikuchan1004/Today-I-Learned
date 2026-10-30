"""
[엘라스틱서치/임베딩 전처리 라우터]
영화 추천 및 검색 시스템 구축을 위한 데이터 전처리 모듈입니다.
1. CSV 파일(영화, 태그, 평점) 로드 및 미리보기
2. 데이터 정합성 검증(결측치, ID 일치 여부, 평점 범위)
3. 텍스트 결합 (영화 제목 + 장르 리스트 + 태그 리스트 -> 검색용 통합 텍스트)
4. 텍스트 청킹 (Sliding Window 방식으로 고정 크기 분할)
5. Gemini/GPT 임베딩 연동 준비
6. 콘텐츠 기반 필터링(CBF), 협업 필터링(CF), 하이브리드 추천(RRF) 구현
"""

from fastapi import APIRouter, Query
import traceback 
from pathlib import Path
import util
import pandas as pd 
from typing import Any, Literal
import os
from elasticsearch import helpers
from collections import Counter
import math
from surprise import Dataset, Reader, KNNWithMeans

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

    for idx_content, info in enumerate(content):
        text = info.get('content_text', '').strip()
        if not text:
            continue

        # range(시작, 끝, 간격) : step만큼 건너뛰며 청크 시작 인덱스 생성
        for idx, idx_start in enumerate(range(0, len(text), step)):
            # [주의: 슬라이싱 범위]
            # text[idx_start : idx_start + size_chunk]로 잘라야 지정한 길이(50자)만큼 슬라이싱됨
            chunk = text[idx_start : idx_start + size_chunk]
            if chunk:
                chunks.append({
                    'index' : idx_content,
                    'movieId': int(info['movieId']),
                    'title': str(info['title']),
                    'genres': list(info['list_genre']),
                    'tags': list(info['list_tag']),
                    'content': chunk,
                    'chunk_index': idx  # 해당 영화 내에서 몇 번째 청크인지 식별
                })

    # for info in content 루프가 완전히 끝난 뒤 모든 영화의 청크를 반환
    return chunks


@router.get('/make/chunk')
def chunk():
    """생성된 청크 목록 중 앞쪽 10개만 미리보기로 반환하는 API"""
    return makeChunk()[0:10]


# ==============================================================================
# 5. 임베딩(Embedding) 생성 및 테스트 API
# ==============================================================================
@router.get('/make/embedding/gemini')
def embedding_gemini():
    """Gemini API를 활용하여 상위 10개 청크의 벡터 임베딩 생성 테스트"""
    target = makeChunk()[0:10]
    actions = util.embedding_with_gemini(target)
    return actions

@router.get('/make/embedding/openai')
def embedding_openai():
    """OpenAI API를 활용하여 상위 10개 청크의 벡터 임베딩 생성 테스트"""
    target = makeChunk()[0:10]
    actions = util.embedding_with_openai(target)
    return actions


# ==============================================================================
# 6. 엘라스틱서치 연결 상태 및 대량 데이터 색인(Bulk Insert)
# ==============================================================================
@router.get('/es/health')
def health():
    """엘라스틱서치 클러스터와의 핑(Ping) 연결 상태 점검"""
    return {'msg' : util.es.ping()}

@router.post('/es/bulk')
def bulk():
    """
    모든 영화 청크를 벡터로 임베딩한 후 엘라스틱서치 인덱스에 벌크(Bulk) 색인
    - 기존 인덱스가 존재하면 삭제 후 최신 스키마(매핑)로 재생성합니다.
    """
    target = makeChunk()
    # 임베딩 생성 (벡터 필드 포함 액션 리스트 반환)
    actions = util.embedding_with_openai(target)

    # 1. 엘라스틱서치에 기존 인덱스가 있다면 깔끔하게 삭제
    if util.es.indices.exists(index=os.getenv('ES_INDEX')):
        util.es.indices.delete(index=os.getenv('ES_INDEX'))

    # 2. 인덱스가 없으면 필드 매핑(스키마) 정의 후 새로 생성
    if not util.es.indices.exists(index=os.getenv('ES_INDEX')):
        mappings = {
            'properties': {
                'index': {'type': 'integer'},
                'movieId': {'type': 'integer'},
                'title': {'type': 'text'},
                'genres': {'type': 'keyword'},      # 정확한 필터링/집계를 위해 keyword 사용
                'tags': {'type': 'text'},
                'content': {'type': 'text'},
                'chunk_index': {'type': 'integer'},
                'embedding': {
                    'type': 'dense_vector',         # 벡터 검색용 dense_vector 타입
                    'dims': 768                     # 임베딩 모델의 벡터 차원 수
                },
            }
        }
        util.es.indices.create(
            index=os.getenv('ES_INDEX'),
            mappings=mappings
        )

    # 3. helpers.bulk()를 통해 대량 문서를 한 번의 네트워크 요청으로 고속 삽입
    success, errors = helpers.bulk(
        util.es,
        actions,
        stats_only=False
    )
    return {
        'msg': {
            'succ': success,
            'errors': errors
        }
    }


# ==============================================================================
# 7. 엘라스틱서치 검색(Search) API
# ==============================================================================
def search_movies(keyword: str, size: int = 10):
    """
    다중 필드(multi_match) 키워드 텍스트 검색 헬퍼 함수
    - title, genres, tags, content 필드를 대상으로 검색어 매칭
    """
    response = util.es.search(
        index=os.getenv('ES_INDEX'),
        query={
            'multi_match': {
                'query': keyword,
                'fields': ['title', 'genres', 'tags', 'content'],
            }
        },
        size=size
    )
    return response

def search_vector(keyword: str, size:int = 10):
    """
    입력된 검색어를 벡터로 변환한 후 엘라스틱서치 KNN 벡터 검색을 수행하는 함수
    - 기존 embedding_with_gemini 함수를 그대로 재활용하여 쿼리 벡터 생성
    """
    # 1. 단일 검색어 텍스트를 임베딩 입력 형식(딕셔너리 리스트)으로 구성
    querys = [{
        'content' : keyword,
        'movieId' :  0,
        'chunk_index' : 0,
    }]
    # 2. Gemini 임베딩 모델을 통해 벡터 추출
    vectors =  util.embedding_with_gemini(querys)
    vector = vectors[0]['_source']['embedding']

    # 3. 엘라스틱서치 dense_vector 필드를 대상으로 KNN(k-최근접 이웃) 유사도 검색 수행
    response = util.es.search(
        index = os.getenv('ES_INDEX'),
        knn = {
            'field' : 'embedding',
            'query_vector' : vector,
            'num_candidates' : max(size*10, 50), # 탐색할 후보 벡터 수
            'k' : size                          # 반환할 이웃 수
        },
        size = size 
    )
    
    return response

@router.get('/es/select/multi_match')
def multi_match(keyword: str, size: int = 10):
    """키워드를 입력받아 다중 필드에서 검색된 영화 목록을 반환하는 API"""
    response = search_movies(keyword, size)
    return {
        'msg': util.formatter(response)
    }

def term_movieId(ids: list):
    """
    여러 movieId를 기반으로 문서를 조회하는 terms 쿼리 헬퍼 함수
    - [주의]: URL Query 파라미터로 넘어온 값은 문자열 형태일 수 있으므로 정수형(int) 변환 필요
    - [주의]: 엘라스틱서치 쿼리 키는 반드시 따옴표로 감싼 'terms' 문자열이어야 함 (함수 terms와 혼동 방지)
    """
    # 엘라스틱서치 movieId 필드가 integer 타입이므로 안전하게 int로 변환
    int_ids = [int(i) for i in ids]

    response = util.es.search(
        index=os.getenv('ES_INDEX'),
        query={
            'terms': {
                'movieId': int_ids
            }
        },
        # 영화당 청크가 여러 개 존재할 수 있으므로 요청한 ID 개수에 비례하여 사이즈 확보
        size=len(int_ids) * 5
    )
    return response

@router.get('/es/select/terms')
def terms(ids: list = Query(...)):
    """
    복수의 movieId를 쿼리 파라미터로 받아 해당하는 청크 문서를 조회하는 API
    - 예시: /es/select/terms?ids=1&ids=2
    """
    response = term_movieId(ids)
    return {
        'msg': util.formatter(response)
    }

#-----------------------------------
# 추천 시스템 (Recommendation System)
#-----------------------------------

@router.get('/recommend/test/counter')
def test_counter():
    """
    collections.Counter의 동작 원리(문자열, 1차원 리스트, 2차원 리스트 누적)를 테스트하는 학습용 API
    """
    # 1. 단일 문자열 내 각 알파벳의 등장 빈도 계산
    str = 'hello world'
    print( Counter(str))

    # 2. 1차원 리스트 내 요소들의 등장 빈도 계산
    list_counter = ['hi' , 'hey' , 'hi' , 'hello'  , 'hi' , 'nihao' , 'hey'] 
    print(Counter(list_counter))

    # 3. Counter 객체 생성 후 update()로 리스트 요소를 누적하는 방식
    food_counter = Counter()
    list_food = ['떡만두국' , '제육덮밥' , '참치김밥' , '돈까스' , '참치김밥', '돈까스']
    for food in list_food :
        food_counter.update(food)
    print(1, food_counter)

    # 4. 리스트를 통째로 감싸서 넘기면 리스트 자체가 단일 요소로 처리됨 (주의점 확인용)
    food_counter2 = Counter()
    for food in [list_food] :
        food_counter2.update(food)
    print(2, food_counter2)

    # 5. 2차원 리스트(유저별 선호 음식 등)를 반복문으로 순회하며 update() 누적
    favorite_foods = [ 
        ['밥' , '치킨'] ,
        ['산낙지', '육회' , '광어회'],
        ['밥' , '라면' , '짜장면'],
        ['햄버거' , '라면' , '밥']
    ]
    food_counter3 = Counter()
    for foods in favorite_foods  : 
        food_counter3.update(foods)
    print(3, food_counter3)

# CBF 콘텐츠 기반 필터링 (Content-Based Filtering)
# 핵심 개념: "내가 과거에 좋아했던 영화들의 장르와 태그를 분석해서, 그와 가장 비슷한 영화를 찾자!"
def content_based_filtering(list_movieId: list, candidate_size: int = 10):
    """
    사용자가 선택한 영화 ID 리스트를 바탕으로, 해당 영화들의 주요 장르와 태그를 추출하여
    유사한 영화를 벡터 검색(KNN)으로 찾아내는 CBF 함수
    """
    # 1. 입력받은 영화들의 상세 청크 데이터를 엘라스틱서치 terms 쿼리로 조회
    selected = term_movieId(list_movieId)

    # return selected

    # 2. 조회된 영화들에서 사용된 장르와 태그의 출현 빈도를 각각 집계
    genre_counter = Counter()
    tag_counter = Counter()
    for hit in  selected['hits']['hits']:
        source = hit['_source']
        genre_counter.update(source.get('genres' , []))
        tag_counter.update(source.get('tags' , []))

    print('genre_counter : ' , genre_counter )
    print('tag_counter : ' , tag_counter )
   
    # terms_genre = [ ]
    # for term, count in genre_counter.most_common(max):
    #     terms_genre.append(term)

    max = 5
    # 3. 장르와 태그를 각각 집계한 뒤 빈도가 가장 높은 상위 5개 특성 추출
    #    - most_common(max): [(단어, 빈도), ...] 형태에서 단어(term)만 리스트 컴프리헨션으로 추출
    #    - 사용하지 않는 빈도수 변수는 언더스코어(_)로 무시
    terms_genre  = [term for term, _ in genre_counter.most_common(max)]

    terms_tag  = [term for term, _ in tag_counter.most_common(max)]

    # 4. 리스트 결합 방식 비교:
    #    - terms_genre + terms_tag 는 매번 새로운 리스트 메모리를 생성함
    terms = terms_genre + terms_tag

    #    - extend()를 사용하면 기존 리스트에 원소들을 바로 추가하여 메모리를 절약할 수 있음
    terms = []
    terms.extend(terms_genre)
    terms.extend(terms_tag)
    # return terms

    # 5. 검색어 문자열 생성 및 순서 보장 중복 제거:
    #    - 단순히 " ".join(terms)를 하면 중복 단어가 들어갈 수 있음
    #    - set(terms)에 넣으면 순서가 뒤죽박죽으로 깨짐
    #    - dict.fromkeys(terms)를 사용하면 파이썬 3.7+부터 입력 순서를 유지하면서 중복만 제거됨!
    query = " ".join(dict.fromkeys(terms))
    # response = search_movies(query)
    
    # 6. 완성된 특성 검색어로 벡터 유사도 검색(KNN) 수행
    response = search_vector (query, candidate_size)

    return response

@router.get('/recommend/cbf')
def cbf(list_movieId: list[int] =  Query(...)):
   """
   콘텐츠 기반 필터링(CBF) 추천 결과를 반환하는 API
   - 예시: /recommend/cbf?list_movieId=1&list_movieId=2
   """
   response =  content_based_filtering(list_movieId)
   return response['hits']['hits']

def split_train_test(test_size : float = 0.2):
    '''
    과거 평점을 학습시키고 미래 평점으로 평가하기 위한 시간 기반 Train/Test 데이터 분할 함수
    - test_size : 미래 평점의 비율 (평가/정답 데이터의 비율, 기본값 20%)

    [분할 원칙]
    - 사용자별로 타임스탬프를 정렬하여 과거 평점은 학습용(train), 최신 평점은 평가용(test)으로 분리
    - 평점이 단 1건뿐인 사용자는 분할하지 않고 학습 데이터에만 보존 (평가 불가능 방지)
    - 만약 timestamp가 동일하다면 원본 데이터 등장 순서(original_order)대로 정렬
    '''
    # 1. 평점 CSV 파일 로드
    frame_ratings = util.load_csv('ratings.csv')

    # 2. 원본 데이터의 불변성을 유지하기 위해 copy() 생성
    data = frame_ratings.copy()

    # 나중에 원본 순서대로 복원하기 위해 행 인덱스를 임시 컬럼에 보관
    data['original_order'] = range(len(data))

    # timestamp 컬럼을 안전하게 숫자 타입으로 변환
    # errors='coerce' : 변환 불가능한 값은 NaN으로 강제 치환
    # errors='ignore' : 실패 시 원본 유지
    # errors='raise'  : 실패 시 ValueError 발생 후 중단
    pd.to_numeric(data['timestamp'], errors ='coerce')

    # 유효한 타임스탬프를 가진 행만 추출 (notna: NaN이 아닌 정상 데이터)
    vaild_data = data[data['timestamp'].notna()].copy()

    # 시간이 비어있는(NaN) 데이터 분리 보관
    no_time = data[data['timestamp'].isna()].copy()

    test_indices = [ ]

    # 3. userId 기준으로 그룹핑 (sort=False: 정렬 연산을 생략하여 원래 등장 순서 유지)
    for _, group in vaild_data.groupby('userId' , sort=False) :

        # 별점을 단 1개만 매긴 사용자는 분할할 수 없으므로 건너뜀 (학습용에만 남김)
        if len(group) <= 1 :
            continue

        # 과거와 미래를 시간 순서로 나누기 위해 정렬:
        # - 1차 기준: timestamp 오름차순 (과거 -> 미래)
        # - 2차 기준: original_order (동일 시간대일 경우 원본 순서 유지)
        # - kind='stable': 동일한 값일 때 기존 정렬 순서를 엄격히 보존
        ordered = group.sort_values(['timestamp', 'original_order'] , kind='stable')

        # 전체 평점 중 test_size 비율에 해당하는 테스트 건수 계산 (올림 처리)
        test_count = math.ceil(len(ordered) * test_size) 
        if test_count < 1 :
            test_count = 1 

        # 최소 1건의 평점은 무조건 학습 데이터에 남겨야 하므로 최대치 제한
        if test_count > len(ordered) - 1 :
            test_count = len(ordered) - 1

        # max(1, test_count) : 최소값을 1건으로 보장
        max(1, test_count)

        # min(test_count, 3) : 최대값을 3건으로 제한할 때 활용
        min(test_count, 3)

        # 최종 테스트 개수 결정 (최소 1개 ~ 최대 전체길이-1개 사이)
        test_count = min(len(ordered) - 1, max(1, math.ceil(len(ordered) * test_size)))

        ordered.tail(test_count).index.tolist()

        # tail(test_count) : 시간순 정렬에서 가장 마지막에 위치한(최신) 데이터 추출
        # 최신 데이터의 인덱스(index)만 수집하여 test_indices 리스트에 추가
        test_indices.extend(ordered.tail(test_count).index.tolist())

        # 테스트할 데이터의 인덱스 수집 완료

    # --------------------------------------------------------------------------
    # [데이터 분할 단계] 수집된 인덱스를 기반으로 최종 학습/테스트 셋 분리
    # --------------------------------------------------------------------------
    # 1. 테스트 데이터 추출: 각 사용자별 최신 평점 인덱스(test_indices)에 해당하는 행만 복사
    test = vaild_data.loc[test_indices].copy()

    # 2. 학습 데이터 추출: 원본 데이터에서 테스트용 인덱스를 제외(drop)하여 과거 데이터만 유지
    train = vaild_data.drop(index=test_indices)

    # 3. 원본 순서 복구: 분할 과정에서 섞인 데이터를 원래 입력 순서(original_order)대로 정렬 후 임시 컬럼 삭제
    #    (kind='stable': 동일 값일 때 기존 정렬 순서를 보장하여 데이터 무결성 유지)
    test = test.sort_values('original_order', kind='stable').drop(columns="original_order")
    train = train.sort_values('original_order', kind='stable').drop(columns="original_order")

    # 4. 인덱스 초기화 후 반환: 0부터 시작하는 깔끔한 인덱스로 재설정하여 튜플(test, train) 형태로 반환
    return test.reset_index(drop=True), train.reset_index(drop=True)


# ==============================================================================
# 8. 사용자 기반 협업 필터링 (Collaborative Filtering, CF)
# ==============================================================================
# 핵심 개념: "나와 취향 및 평점 패턴이 비슷한 다른 사용자들은 어떤 영화를 좋아했을까?"
def collaborative_filtering(userId: int, top_k: int = 10):
    """
    Surprise 라이브러리의 KNNWithMeans 모델을 사용한 사용자 기반 협업 필터링 추천 함수
    - userId: 추천 대상 사용자의 고유 ID (Raw ID)
    - top_k: 예상 평점이 가장 높은 추천 영화 반환 개수 (기본값: 10)
    """
    # 1. 학습/테스트 데이터셋 분리 (과거 평점 데이터인 train만 모델 학습에 사용)
    test, train = split_train_test()

    # 2. 모델 학습에 필수적인 3개 컬럼만 추출 (Surprise는 사용자ID, 아이템ID, 평점 순서를 요구함)
    data = train[['userId', 'movieId', 'rating']].copy()

    # [예외 처리] 학습 데이터셋에 없는 유저는 취향을 분석할 수 없으므로(Cold Start 문제) 즉시 중단
    # (주의: data['userId'] 대신 .values 또는 .to_numpy()를 검사해야 실제 유저 ID 값을 올바르게 확인)
    # if userId not in data['userId'].values:
    if userId not in data['userId'].to_numpy():
        raise ValueError(f'[userId: {userId}]을/를 찾을 수 없습니다. 다시 입력해주세요')

    # 3. Surprise Reader 객체 생성: 평점의 유효 범위(최소점, 최대점)를 명시하여 스케일 해석 기준 설정
    reader = Reader(rating_scale=(0.5, 5.0))

    # 4. Pandas DataFrame을 Surprise 전용 Dataset 자료구조로 로드
    data_set = Dataset.load_from_df(data, reader)

    # 5. 전체 데이터를 학습용 Trainset 객체로 변환
    #    [주의] build_full_trainset 뒤에 ()를 반드시 호출해야 함수 객체가 아닌 실제 Trainset이 생성됨
    train_set = data_set.build_full_trainset()

    # --------------------------------------------------------------------------
    # [유사도 및 추천 모델 설정]
    # - KNNWithMeans: 사용자별 평점 부여 편향(항상 후하게 주거나 짜게 주는 성향의 평균값)을 보정해주는 KNN
    # - n_neighbors: 유사도 계산 시 참고할 이웃(유사 사용자) 수 (k=30)
    # - sim_options:
    #     * name: 'pearson' (피어슨 상관계수 - 유저들의 평점 경향성 유사도 측정)
    #     * user_based: True (True=사용자 기반 유사도 추천, False=아이템 기반 유사도 추천)
    # - verbose: False (학습 및 유사도 계산 진행 로그 미출력)
    # --------------------------------------------------------------------------
    n_neighbors = 30
    model = KNNWithMeans(
        k=n_neighbors,
        sim_options={
            # 'name': 'cosine',
            'name': 'pearson',
            'user_based': True
        },
        verbose=False
    )

    # 6. 모델 학습: 사용자 간 유사도 행렬을 계산하여 내부 메모리에 적재
    model.fit(train_set)

    # --------------------------------------------------------------------------
    # [Surprise ID 변환 개념]
    # - Raw ID: 원본 CSV/DB에서 쓰이는 실제 식별자 (예: 실제 movieId 1, 104 등)
    # - Inner ID: Surprise 내부 계산 효율화를 위해 0부터 연속 부여된 정수 인덱스
    # --------------------------------------------------------------------------
    # 대상 사용자의 실제 userId를 Surprise 내부 인덱스(inner_uid)로 변환
    inner_user_id = train_set.to_inner_uid(userId)

    # 7. 대상 사용자가 이미 평가(시청)한 영화 목록 수집
    #    - train_set.ur: User-Ratings 딕셔너리 {inner_uid: [(inner_iid, rating), ...]}
    #    - to_raw_iid(): 내부 영화 인덱스를 실제 movieId로 변환하여 집합(set)에 보관 (중복 방지 및 빠른 탐색)
    rated_movies = set()
    for inner_movie_id, _ in train_set.ur[inner_user_id]:
        rated_movies.add(train_set.to_raw_iid(inner_movie_id))

    # 8. 추천 후보 영화(Candidate) 선정: 학습 셋에 등록된 전체 영화 중 "아직 평가하지 않은 영화"만 필터링
    #    - train_set.n_items: 전체 고유 영화 수
    candidate_movies = [
        train_set.to_raw_iid(inner_movie_id)
        for inner_movie_id in range(train_set.n_items)
        if train_set.to_raw_iid(inner_movie_id) not in rated_movies
    ]

    # 9. 미평가 영화들에 대한 예상 평점(Predicted Rating) 추정
    #    - model.predict(userId, movieId).est: 유사한 이웃들의 평가를 가중 평균하여 예상한 점수
    recommend = []
    for movieId in candidate_movies:
        score = model.predict(userId, movieId).est
        recommend.append({
            'movieId': movieId,
            'score': score
        })

    # 10. 예상 평점 내림차순 정렬 (높은 점수를 받을 것으로 예측된 영화가 맨 위로 오도록)
    recommend.sort(key=lambda x: x['score'], reverse=True)

    # 상위 top_k개 결과 슬라이싱 반환
    return recommend[:top_k]


# ==============================================================================
# 9. 추천 API 엔드포인트
# ==============================================================================
@router.get('/es/recommend/cf')
def cf(userId: int, top_k: int = 10):
    """
    특정 사용자(userId)에게 취향이 유사한 다른 유저 기반의 영화 top_k개를 추천하는 GET API
    - Swagger 호출 예시: /es/recommend/cf?userId=1&top_k=10
    """
    return collaborative_filtering(userId, top_k)

# Recall@K (재현율 지표)
# 개념: 전체 정답 개수 중에 추천 시스템이 맞힌 개수의 비율 (순위는 고려하지 않음)
# 계산 공식: (추천 결과 중 정답 개수) / (전체 정답 개수)
def recall_at_k(
        userId: int,
        test : pd.DataFrame,    # 정답 데이터 (평가용 테스트셋)
        recommend : list[dict], # 모델이 생성한 추천 목록 
        threshold: float = 4.0, # 사용자가 좋아했다고 판단할 최소 평점 기준
        k: int =10              # 상위 몇 개의 추천 결과를 검사할 것인가 (K개)
):      
        # 1. 정답 데이터(test)에서 사용자가 threshold(예: 4.0점) 이상 높은 평점을 준 영화 목록(정답셋) 필터링
        #    - pandas.Series 객체는 set으로 자동 형변환이 안 되므로 set()으로 명시적 형변환
        #    - relevant_movies : 사용자가 실제로 선호한(관련된) 정답 영화 집합
        relevant_movies = set(test.loc)[
            # 첫 번째 전달인자 : 조건 (해당 유저이면서 기준 평점 이상)
            (test['userId'] == userId)
            & (test['rating'] >= threshold),
            # 두 번째 전달인자 : 가져올 특정 컬럼 ('movieId')
            'movieId'
        ]
        # 정답 데이터에 조건에 맞는 영화가 없다면 분모가 0이 되므로 Recall 계산 불가 (-1.0 반환)
        if len(relevant_movies) == 0:
            return -1.0

        # 2. 추천 목록 상위 k개에서 movieId만 모아서 set 집합으로 생성 (묵시적/내포 집합 생성)
        recommend_movies = {
            item['movieId'] for item in recommend[:k]
        }

        # 3. 추천 목록 중 사용자가 좋아한 정답 영화의 개수 (교집합 연산)
        #    - len(relevant_movies & recommend_movies)의 의미로 작성된 연산
        hit_count = len (relevant_movies) & len (recommend_movies)

        # 4. Recall@K = 맞힌 개수 / 전체 정답 개수
        result = hit_count / len(relevant_movies)
        return result
        
@router.get('/recommend/recall')
def recall(userId: int):
    """
    특정 유저에 대한 협업 필터링 추천 결과의 Recall@K 지표를 계산하는 API
    """
    test,_ = split_train_test()
    recommend = collaborative_filtering(userId, 50)
    threshold = 2.0 # 평점 2.0 이상을 선호한 영화로 가정
    k = 50          # 상위 50개 추천 결과 내에서 평가

    return  recall_at_k(userId, test, recommend, threshold, k)

# 하이브리드 추천 : CBF (콘텐츠 기반) + CF (협업 필터링)
# 개념: 두 가지 알고리즘의 추천 결과를 결합하고, RRF(상호 순위 융합) 방식으로 점수를 매겨 최종 순위 결정
def hybrid_filtering(
     list_movieId : list [int], # CBF에서 사용할 사용자의 시청 영화 목록
     userId:int,                # CF에서 사용할 사용자 ID 
     top_k:int = 10,            # 최종 반환할 결과 개수
     candidate_size:int = 50    # 각 추천 알고리즘별로 추출할 후보군 크기
):
    pass
    # --------------------------------------------------------------------------
    # [1단계: CBF 추천 수행]
    # --------------------------------------------------------------------------
    # def content_based_filtering(list_movieId: list):
    response_cbf = content_based_filtering(list_movieId, candidate_size)
    # return response_cbf

    # 조회된 결과 중 사용자가 이미 본 영화(list_movieId)는 제외하고 중복 없이 movieId 수집
    result_cbf = set()
    for hit  in  response_cbf['hits']['hits']:
        movieId  = int(hit['_source']['movieId'])
        # 내가 안 본 영화 id만 중복 없이 담는다.
        if movieId not in list_movieId:
            result_cbf.add(movieId)
     
    # --------------------------------------------------------------------------
    # [2단계: CF 추천 수행]
    # --------------------------------------------------------------------------
    response_cf = collaborative_filtering(userId, candidate_size)
    result_cf = set()
    for hit in response_cf:
        movieId = hit.get('movieId')
        if movieId not in list_movieId:
            result_cf.add(movieId)

    # --------------------------------------------------------------------------
    # [3단계: RRF (Reciprocal Rank Fusion) 상호 순위 점수 계산]
    # --------------------------------------------------------------------------
    # RRF 공식: 1 / (60 + 순위) -> 높은 순위일수록 분모가 작아져서 더 높은 점수를 얻음
    rrf_score = {}

    # CBF 결과에 대한 RRF 점수 누적 (start=1 : 1위부터 시작)
    for index, movieId in enumerate(result_cbf, start=1):
        # rrf_score 딕셔너리에 movieId 키가 이미 존재한다면 기존 점수에 합산
        if rrf_score.get(movieId) : 
            rrf_score[movieId] += 1 / (60 + index)
        else :
            rrf_score[movieId] = 1 / (60 + index)

    # CF 결과에 대한 RRF 점수 누적 (두 알고리즘 모두에서 상위에 든 영화일수록 점수가 대폭 상승)
    for index, movieId in enumerate(result_cf, start=1):
        if rrf_score.get(movieId) : 
            rrf_score[movieId] += 1 / (60 + index)
        else :
            rrf_score[movieId] = 1 / (60 + index)

    # --------------------------------------------------------------------------
    # [4단계: 최종 점수 기준 내림차순 정렬 및 상위 K개 추출]
    # --------------------------------------------------------------------------
    # 점수가 높은 순(reverse=True)으로 정렬 
    result = sorted(
        rrf_score.items(),
        key=lambda x:x[1], 
        reverse=True
    )

    # 상위 목록 top_k만큼 잘라서 돌려주기
    return result[:top_k]

@router.get('/recommend/hybrid')
def hybrid(
    userId:int,                             # CF에서 사용할 사용자 ID 
    top_k:int = 10,                         # 최종 반환할 결과 개수
    candidate_size:int = 50,                # 각 추천의 후보 수
    list_movieId : list [int] = Query(...), # CBF에서 사용할 영화 목록 (쿼리 파라미터)
):
    """
    CBF와 CF를 결합한 하이브리드 추천 결과를 영화 제목과 함께 반환하는 API
    """
    # 1. 하이브리드 추천 순위 결과 [(movieId, score), ...] 계산
    result_hybrid =  hybrid_filtering(list_movieId, userId, top_k, candidate_size)
    
    # 2. movieId에 대응하는 영화 제목을 조회하기 위해 영화 메타데이터 로드
    df_movies = util.load_csv('movies.csv')
    result = {}
    
    # 3. 각 추천 결과의 movieId로 제목(title)을 매핑하여 최종 딕셔너리 구성
    for i in result_hybrid:
            movieId = i[0]
            score = i[1]
            # 해당 movieId를 가진 행의 title 값을 추출 (.iloc[0] : 첫 번째 매칭 행)
            title = df_movies.loc [
                df_movies['movieId'] == movieId,
                'title'
            ].iloc[0] # 행의 순서
            
            result[movieId] = {
                'title' : title,
                'score' : score
            }

    return result