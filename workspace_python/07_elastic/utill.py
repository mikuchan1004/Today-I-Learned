from pathlib import Path # 경로 관련 라이브러리
import json
from config import ELASTIC_ENDPOINT, ELASTIC_API_KEY
from elasticsearch import Elasticsearch
from elasticsearch import helpers

es = Elasticsearch(
    ELASTIC_ENDPOINT, # DB 연결 주소
    api_key = ELASTIC_API_KEY # DB 계정
)

# json 파일 읽어오기 
def load_documents() :
    result = {}
    
    # print('__file__ :' , __file__) 
    # # __file__ : 현재 실행한 파일의 전체 경로
    # print(Path(__file__).resolve().parents)
    # print(Path(__file__).resolve().parents[2]) # 부모 폴더 몇 개 올라가는지
    # print(Path(__file__).resolve().parents[1]) 
    # print(Path(__file__).resolve().parents[0])

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