from fastapi import APIRouter
from config import ELASTIC_ENDPOINT, ELASTIC_API_KEY
from elasticsearch import Elasticsearch
from elasticsearch import helpers
import json
from pathlib import Path # 경로 관련 라이브러리

router = APIRouter(tags=['엘라스틱서치 관련 라우터']) # tags : 스웨거용 글씨

es = Elasticsearch(
    ELASTIC_ENDPOINT, # DB 연결 주소
    api_key = ELASTIC_API_KEY # DB 계정
)

@router.get('/es/health')
def health() :
    connected = es.ping()
    print('엘라스틱서치 연결 상태 : ' , connected)
    return {
        'connected' : connected,
        'msg' : "Elasticsearch 연결 " + "성공"  if connected else "실패"
    }

# insert는 아니지만 행동을 하는 것은 POST가 어울린다.
@router.post('/es/create')
def create_index():
    result = {
        'msg' : None
    }
    # 엘라스틱서치의 특성

    # 모든 요청은 REST API를 사용한다 
    # 즉 주소기반으로 CRUD한다.

    # 엘라스틱서치 VS RDBMS
    #  index : table 
    #  docoument  : 줄, row, record, 튜플
    # field : column
    # mapping : int,varchar등의 타입 
    if es.indices.exists(index='computer') : 
        print('computer index가 이미 있습니다.')
        result['msg']  = 'computer index가 이미 존재합니다.'
        return result
    
    es.indices.create(
            index='computer',
            mappings= {
                'properties' : {
                    'id' : {'type' : 'integer'},
                    'title' : {'type' : 'text'}, #유연한값 :  백터로 분석해서 유연한 검색이 가능하다.
                    'category' : {'type' :  'keyword'},  # 정확한값 :  딱 완전 똑같은  단어로만 검색이 가능하다.
                    'price' : {'type' : 'integer'},
                    'rating' : {'type' : 'float'},
                    'created_at' : {'type' : 'date'},
                    'content' : {'type' : 'text'}
                }
            }
        )
    print(' computer index 생성 완료')
    result['msg'] = 'computer index 생성 완료'
    return result

@router.post('/es/insert/bulk')
# insert 할건데
# insert 대신 수집한다는 뜻의 ingest를 한번 써봤다.
def ingest_documents() :
    documents = load_documents()

    actions = [ ]
    for doc in documents :
        actions.append ({
            '_index' : 'computer',
            '_id' : doc['id'],
            '_source' : doc
        })

    success, errors = helpers.bulk(es, actions , stats_only=False)
    print( 'success :' , success)
    print('errors : ', errors)

    return {
        'msg' : {
            'success' : success,
            'errors' : errors
        }
    }

def load_documents() :
    result = {}
    print('__file__ :' , __file__) 
    # __file__ : 현재 실행한 파일의 전체 경로
    print(Path(__file__).resolve().parents)
    print(Path(__file__).resolve().parents[2]) # 부모 폴더 몇 개 올라가는지
    print(Path(__file__).resolve().parents[1]) 
    print(Path(__file__).resolve().parents[0])

    BASE_DIR  = Path(__file__).resolve().parents[1]
    DOCUMENT_FILE = BASE_DIR / 'data' / 'data.json' # 경로 합치기 
    #Path에서는  / 가 더하기 역할을 한다. 
    
    try: # 혹시 파일이 없을까봐 
        with open(DOCUMENT_FILE , 'r', encoding='utf-8') as file:  # 파일을 읽기 (r) 모드로 열어라 
            # print(file)  # 포장지만 나온다

            # json을 딕서녀리로 변환 
            result = json.load(file)
            # 참고로 딕셔너리를 json으로 변환하려면 json.dump()
            print(result)
    except Exception as e :
        print('open 하다가 오류 발생 :' , e)

    return result

@router.get('/es/select/all')
def select_all():
    # 그냥 전체 선택
    # select * form computer 
    # response = es.search(
    #     index='computer',
    #     query={'match_all' : {}}
    # )
    # print(reseponse)
    # return reseponse

    # GROUP  BY 
    # select category from computer 
    # group by category 
    response = es.search(
        index='computer',
        query={'match_all' : {}},
        aggs= {
            'categories' : { # 우리 컬럼이 아니라 정해진 말 
                'terms'  : {
                    'field'  : 'category' # 컬럼명 category
                }
            }
        }      
    )
    # print(response)
    '''
       "aggregations": {
        "categories": {
          "doc_count_error_upper_bound": 0,
          "sum_other_doc_count": 0,
          "buckets": [
            {
              "key": "노트북",
              "doc_count": 3
            },
            {
              "key": "네트워크",
              "doc_count": 2
            },
            {
              "key": "모니터",
              "doc_count": 1
            },
            {
              "key": "저장장치",
              "doc_count": 1
            },
            {
              "key": "주변기기",
              "doc_count": 1
            }
          ]
        }
    }
    '''
    results = [ ]
    for hit in response['hits']['hits'] :
        document = hit.get('_source' , {})
        results.append(document)

    return {
        'msg' : {
        'results' : results,
        'total' : response['hits']['total']['value']
        }
    }

def formatter(resp) :
    results = [ ]
    # 우리가 넣은 내용만 쏙 빼온다.
    for hit in resp['hits']['hits'] :
        document = hit.get('_source' , {})

        results.append({
            'document' : hit.get('_source' , {}),
            'score' : hit.get('_score')
        })

    return {
                'results' : results,
                'total' : resp['hits']['total']['value']
            }

# match
# where랑 비슷함 
# 백터 검색 (자연어 검색)
# 검색어를 분석한 뒤에 토큰 단위로 검색
@router.get('/es/select/match')
def match(keyword:str) :
    response = es.search(
        index='computer',
        query={
            "match" : {
                'content' : keyword
            }
        }
    )
    return {
        "msg" : formatter(response)
    }

# multi_match
# 여러 필드에서 match 검색
@router.get('/es/select/multi_match')
def multi_match(keyword: str):
    response = es.search(
        index='computer',
        query={
            "multi_match" : {
                'query' : keyword,
                'fields' : ['title' , 'content']
            }
        }
    )
    return {
        "msg" : formatter(response)
    }

# term 
# select의 like 처럼 정확히 일치하는 값
@router.get('/es/select/term')
def term(keyword: str):
    response = es.search(
        index='computer',
        query={
            "term" : {
                # 'category' : keyword
                'content' : keyword
            }
        }
    )
    return {
        "msg" : formatter(response)
    }

@router.get('/es/select/range')
def range_(max : int , min : int = 0):
    response = es.search(
        index='computer',
        query={
            "range" : {
                # 'category' : keyword
                'price' : {
                    'gte' :  min, 
                    'lte' : max
                }
            }
        }
    )
    return {
        "msg" : formatter(response)
    }

# bool 복합 쿼리 
# filter : 쿼리가 참인 것 검색 (스코어 계산을 하지 않아 빠르다), 여러개 쓰면 AND
# must : 쿼리가 참인 것 검색 
# must_not : 거짓인 것만 검색
# should : 쿼리가 참인 것의 점수를 높인다, 여러개 쓰면 OR
@router.get('/es/select/filter') 
def filter_(category, keyword) :
    response = es.search(
        index='computer',
        query={
            "bool" : {
                'filter' : [{
                    'term' :  {'category' : category}
                }],
                'must' : [{
                    'match' : {'content' : keyword}
                }]
            }
        }
    )
    return {
        "msg" : formatter(response)
    }

@router.get('/es/select/orderby')
def orderby(sort_field,order = 'asc'):

    if order != 'asc' and order != 'desc' :
        return {'msg' : 'order는 asc 또는 desc여야 합니다.'}

    response = es.search(
        index='computer',
        query={"match_all" : {}},
        sort = [{
            sort_field : {'order' : order}
        }],
        size = 20 
    )
    return {
        "msg" : formatter(response)
    }
