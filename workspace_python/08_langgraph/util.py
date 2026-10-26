import pandas as pd 
from  pathlib import Path
import traceback
from dotenv import load_dotenv
load_dotenv()
import os

from google import genai
from google.genai import types

import time

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