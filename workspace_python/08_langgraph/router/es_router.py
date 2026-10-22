from fastapi import APIRouter
from  pathlib import Path
import pandas as pd 
import traceback 

router = APIRouter(tags=["엘라스틱서치"])

@router.get('/read/head')
def read(fileName):
    frame = load_csv(fileName)
    if frame is None:
        return {'ERROR' : '파일을 불러오지 못했습니다.'}

    '''
    head : 상위 몇개의 데이터만 추출 (기본값 : 5)
    astype : 형변환, 기본값 : NumPy.int64
    to_dict : dict로 변환 
    orient = 'records' : 컬럼명: 값 형태. 기본값 = dict : 인덱스가 키가 된다 
    '''
    preview =   frame.head().astype(object).to_dict(orient='records')
    return preview

def load_csv(fileName):
    BASE_DIR = Path(__file__).resolve().parents[1]
    DOCUMENT_FILE = BASE_DIR / "data" / "ml-latest-small" / fileName
    # print(DOCUMENT_FILE)

    frame = None
    try:
        frame = pd.read_csv(DOCUMENT_FILE)
    except Exception as e :
        traceback.print_exc()
        print('read_csv 파일 로딩 오류' , e)

    return frame

if __name__ == "__main__":
    print('Path(__file__) :' , Path(__file__))
    load_csv('moives.csv')
