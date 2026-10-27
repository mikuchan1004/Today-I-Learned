"""
[엘라스틱서치/임베딩 전처리 라우터]
영화 추천 및 검색 시스템 구축을 위한 데이터 전처리 모듈입니다.
1. CSV 파일(영화, 태그, 평점) 로드 및 미리보기
2. 데이터 정합성 검증(결측치, ID 일치 여부, 평점 범위)
3. 텍스트 결합 (영화 제목 + 장르 리스트 + 태그 리스트 -> 검색용 통합 텍스트)
4. 텍스트 청킹 (Sliding Window 방식으로 고정 크기 분할)
5. Gemini/GPT 임베딩 연동 준비
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
# 추천 시스템
#-----------------------------------

@router.get('/recommend/test/counter')
def test_counter():
    str = 'hello world'
    print( Counter(str))

    list_counter = ['hi' , 'hey' , 'hi' , 'hello'  , 'hi' , 'nihao' , 'hey'] 
    print(Counter(list_counter))

    food_counter = Counter()
    list_food = ['떡만두국' , '제육덮밥' , '참치김밥' , '돈까스' , '참치김밥', '돈까스']
    for food in list_food :
        food_counter.update(food)
    print(1, food_counter)

    food_counter2 = Counter()
    for food in [list_food] :
        food_counter2.update(food)
    print(2, food_counter2)

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

# CBF 콘텐츠 기반 필터링 Content-Based Filtering
# "내가 뭘 좋아했지?"
def content_based_filtering(list_movieId: list):
    selected = term_movieId(list_movieId)

    # return selected

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
    # 장르와 태그를 각각 집계한 뒤 : counter
    # 빈도가 높은 특성부터 검색어에 반영한다
    # most_common : 기본값 None - 모두 다 
    # most_common의 리턴은 내용과 숫자가 나온다
    # 사용하지 않는 변수는 보통 _로만 표시한다
    terms_genre  = [term for term, _ in genre_counter.most_common(max)]

    terms_tag  = [term for term, _ in tag_counter.most_common(max)]

    # list는 +로 합칠 수 있는데 하나씩 더해 나갈 때 마다 메모리를 차지한다.

    terms = terms_genre + terms_tag

    # extend를 사용하면 메모리를 절약할 수 있다.
    terms = []
    terms.extend(terms_genre)
    terms.extend(terms_tag)
    # return terms

    # 단점 : 중복 데이터가 있을 수 있다
    # " ".join(terms)
    # 그래서 set에 넣어보자
    # 그런데 순서를 보장하지 않는다
    # " ".join(set(terms))
    # 나는 순서를 유지하면서 중복을 제거하고 싶다
    # dict.fromkeys()를 사용하면 된다.
    # [a,b,c] >>>> {a: None, b : None}
    # 이걸 join 하면 key만 빼올 수 있다.
    query = " ".join(dict.fromkeys(terms))
    response = search_movies(query)

    return response

@router.get('/recommend/cbf')
def cbf(list_movieId: list[int] =  Query(...)):
   response =  content_based_filtering(list_movieId)
   return response['hits']['hits']

def split_train_test(test_size : float = 0.2):
    '''
    과거 평점을 학습시키고 미래 평점으로 평가하자
    test_size  : 미래 평점의 비율(정답 데이터의 비율)

    사용자 별로 
    최신 평점은 평가용
    과거 평점은 학습용 

    평점이 한 건뿐인 사용자는 학습 데이터에만 둔다 
    만약에 timestamp가 같으면 원본 행 순서대로 정렬한다
    '''
    # 평점 파일 일기 
    frame_ratings = util.load_csv('ratings.csv')

    # 원본 유지를 위해 
    data = frame_ratings.copy()

    data['original_order'] = range(len(data))

    # timestamp을 숫자 타입으로 변경
    # errors='coerce' : 변경이 안 되는건 NaN으로 강제 변경
    # errors ='ignore'  : 변경 실패 시 원본 유지 
    # errors = 'raise'  :  ValueError 발생하고 즉시 중단
    pd.to_numeric(data['timestamp'], errors ='coerce')

    # N/A가 아닌 것만 뽑아준다 
    # data[ True/False] >>> 참인 행 (row 또는 document)만 반환
    vaild_data = data[data['timestamp'].notna()].copy()

    # 시간이 N/A 즉 비어있는 것만 뽑아준다
    no_time = data[data['timestamp'].isna()].copy()

    test_indices = [ ]

    # userId가 같은 데이터끼리 groupby 
    # sort의 기본값은 True >> userId로 정렬하지 않고 원래 등장 순서를 유지 
    # 원래 id, value 반환인데 Id는 안 쓸 거라서
    for _, group in vaild_data.groupby('userId' , sort=False) :

        # 별점을 하나만 준 사용자는 건너뛰기 
        # 지금은 학습과 정답 데이터를 나누는 거라서
        if len(group) <= 1 :
            continue

        # 과거와 미래를 나누기 위해서 
        # timestamp 기준으로 정렬한다 
        # 같은 게 있다면 original_order 기준으로 정렬해라
        #  kind stable : 그래도 같은 게 있다면 정렬 전 순서 유지 
        # kind에 사용할 수 있는 것
        # quicksort(기본값) , mergesort, heapsort, stable
        # 오름차순
        ordered = group.sort_values(['timestamp', 'original_order'] , kind='stable')

        # 전체 데이터 중 test_size 비율로 뽑았다 
        # 0.4 등의 결괴를 1로 만든다
        test_count = math.cell(len(ordered) * test_size) 
        if test_count < 1 :
            test_count = 1 

        if test_count > len(ordered) - 1 :
            test_count = len(ordered) - 1

        # max : 둘 중의 큰 값을 돌려준다 
        # 최소값을 지정할 떄 사용
        max(1, test_count)

        # min : 둘 중의 작은 값을 돌려준다
        # 최대값을 지정할 때 사용
        min(test_count, 3)

        test_count = min(len(ordered)) - 1, max(1, math.cell(len(ordered) * test_size))

        ordered.tail(test_count).index.tolist()

        # tail : 끝에서 몇 개 
        # 미리 시간 오름차순으로 정렬해 둬서 최신 데이터는 끝에 있다
        # index만 모은다 = 나중에 학습 데이터 분리할 때 사용하려고
        test_indices.extend(ordered.tail(test_count).index.tolist())

        # 테스트 할 데이터의 index는 모아둔 상태 

        # 실제 테스트 데이터 추출 

        # 학습 데이터 추출