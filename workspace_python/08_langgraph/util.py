import pandas as pd 
from  pathlib import Path
import traceback
from dotenv import load_dotenv
load_dotenv()
import os

from google import genai
from google.genai import types

import time

from openai import OpenAI
from elasticsearch import Elasticsearch
es = Elasticsearch(os.getenv('ELASTIC_ENDPOINT'))

def load_csv(fileName):
    BASE_DIR = Path(__file__).resolve().parents[0]
    DOCUMENT_FILE = BASE_DIR / "data" / "ml-latest-small" / fileName
    # print(DOCUMENT_FILE)

    frame = None
    try:
        frame = pd.read_csv(DOCUMENT_FILE)
    except Exception as e :
        traceback.print_exc()
        print('read_csv 파일 로딩 오류' , e)

    return frame

def embedding_with_gemini(chunks) :
    api_key = os.getenv('GEMINI_API_KEY')
    client = genai.Client(api_key=api_key)

    actions= []
    for chunk in chunks:
        result = client.models.embed_content(
            model='gemini-embedding-2',
            contents=[
                types.Content(
                    parts=[
                        types.Part.from_text(text=chunk['content'])
                    ]
                )
            ],
            config=types.EmbedContentConfig(
               output_dimensionality=768
               # 토큰에 영향을 주지 않는다
               # 저장공간이 커지고 검색이 느려진다
            )
        )
        chunk['embedding'] = result.embeddings[0].values

        actions.append(
            {
                    '_index' : os.getenv('ES_INDEX'),
                    '_id' : f'{chunk['movieId']} - {chunk['chunk_index']}',
                    '_source': chunk
            }
        )

        time.sleep(0.7) # 0.7초 멈춤

    return actions

def embedding_with_openai(chunks):
    api_key = os.getenv('OPEN_API_KEY')
    client = OpenAI(api_key=api_key)

    actions = []
    last_index = 0 
    time_before = time.time()

    contents =  [chunk['content']  for chunk in chunks]
    for idx_start in range(0, len(contents), 2047):
        contents_part = contents[idx_start : idx_start + 2047] 

        # 임베딩 하기 
        # openai는 list를 주면 결과도 list로 나온다
        result = client.embeddings.create(
            model='text-embedding-3-small',
            input=contents_part,
            encoding_format='float', # 기본값 : base64
            dimensions=768
        )
        # 혹시 몰라서 내용 중의 index로 재정렬
        vectors = [sort_data.embedding for sort_data  in  sorted (result.data , key=lambda item: item.index)]

        for  idx, vector in enumerate(vectors) : 
            chunks[last_index]['embedding'] = vector

            actions.append(
            {
                '_index' : os.getenv('ES_INDEX'),
                '_id' : f'{chunks[last_index]['movieId']} - {chunks[last_index]['chunk_index']}',
                '_source': chunks[last_index]
            })

            last_index += 1 

        time_after = time.time()
        print('걸린 시간(2047개)'  , time_after - time_before)
        time_before = time.time()

    return actions

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