from fastapi import APIRouter
from utill import es, load_documents
from elasticsearch import helpers

# 정규표현식 (regular expression, regExp) 사용을 위한 모듈
import re 

router = APIRouter(tags=['임베딩 관련 라우터']) # tags : 스웨거용 글씨

@router.get('/embed/split')
def split(text):
    return split_text(text)

def split_text(text) :
    # print('text : ' , text)
    sentences = re.split(
        r"(?<=[.!?])\s+", # .!? 다음에  공백(\s+)이 있으면 분리한다.
        text.strip() # 문자의 앞뒤 공백 제거한 것을 대상으로 
    )
    # print('setences : ' , sentences)
    # return sentences
    
    # 혹시 몰라서 각 리스트 요소의 양쪽 공백 제거 
    sentences2 = [ ]
    for s in sentences :
        if s.strip() : # 공백 제거 후에도 글이 있으면 
            sentences2.append(s.strip()) # 그 글로 리스트에 추가
    sentences = sentences2

    chunks = [ ]
    chunk_size = 30
    '''
        고양이는 귀엽다. 고양이는 털이 많다. 이미지도 깔끔해요.
        [
            '고양이는 귀엽다.',
            '고양이는 털이 많다.' ,
            '이미지도 깔끔해요.'
        ]
    '''
    # 청크보다 작은 문장은 합칠 수 있으면 합치자
    # 큰 건 어쩔 수 없고

    # 임시 저장소
    temp = ' '
    for sentence in sentences : 
        # print('길이, 글씨 : ' ,len(sentence) , sentence)

        # chunk_size 보다 짧은데 최대한 채워서 chunk에 넣겠다.

        candidate = ' ' # 일단 다음 문장을 붙여본다

        #이전 문장이 있으면 
        if len(temp) > 0 :
            # 뒤에 지금 문장을 붙여본다
            candidate = f'{temp} {sentence}'
        else :
            candidate = sentence

        # 붙인게 아직 모자라면 더 붙여보기
        if len(candidate) <= chunk_size:
            temp = candidate 
        else : 
            # 붙인게 넘치면, 붙이기 전의 안붙은걸 청크로 확정한다.
            if len(temp) > 0 :
                chunks.append(temp)
            #     temp = ' '
            # elif len(temp) == 0:
            #     # 처음부터 큰게 들어왔으면 그 것들 청크로 확정한다.
            #     chunks.append(sentence)
            temp = sentence

    if len(temp) > 0 :
        chunks.append(temp)

    # print(chunks)

    overlap_size = 6   
    overlap_chunks = [ ]
    for index, chunk in enumerate(chunks):
        if index == 0 :
            overlap_chunks.append(chunk)
            continue  

        before = chunks[index - 1]
        prefix  = before[-overlap_size:] # 뒤에서 overlap_size 만큼부터 끝까지
        now = f' {prefix} {chunk}'.strip()
        overlap_chunks.append(now)

    # print(overlap_chunks)
    return overlap_chunks

@router.post('/embed/create')
def create_embed_index():
    if es.indices.exists(index='computer_chunk'):
        #테이블 삭제
        es.indices.delete(index='computer_chunk')
        # es.delete_by_query(
        #     index='computer_chunk',
        #     query={
        #         'match_all' : { }  # 모든 문서 대상 
        #     },
        #     refresh=True # 삭제 결과를 즉시 검색에 반영
        # )
        # return 'computer_chunk가 이미 있습니다.'

    es.indices.create (
        index='computer_chunk',
        mappings= {
            'properties' : {
                'id' : {'type' : 'integer'},
                'title' : {'type' : 'text'}, #유연한값 :  백터로 분석해서 유연한 검색이 가능하다.
                'category' : {'type' :  'keyword'},  # 정확한값 :  딱 완전 똑같은  단어로만 검색이 가능하다.
                'price' : {'type' : 'integer'},
                'rating' : {'type' : 'float'},
                'created_at' : {'type' : 'date'},
                'content' : {'type' : 'text'},
                'chunk_index' : {'type' : 'integer'},
                'embedding' : {
                    'type' : 'dense_vector',
                    'dims' : 384
                }
            }
        }
    )
    return 'computer_chunk index 생성 완료'

@router.post('/embed/insert/bulk')
def ingest_embed_documents():
    # json 가져오기 
    documents = load_documents()

    actions = [ ]
    for doc in documents : 
        # chunk 만들기 
        chunks = split_text(doc['content'])

        for index, chunk in enumerate(chunks) :

            # 백터로 변환
            embedding =  get_embedding(doc['title'], chunk)

            # 살짝 변환 
            doc2 = doc
            doc2['chunk_index' ] = index
            doc2['embedding'] = embedding

            #actions에 추가 
            actions.append({
                '_index' : 'computer_chunk',
                '_id' : f'{doc2["id"]}-{index}',
                '_source' : doc2
            })

    success, errors = helpers.bulk(
        es,
        actions,
        stats_only=False    # 기본값 True 
                                                # True : 성공 실패 숫자만 
                                                # False : 성공 실패 숫자 + 에러 메세지
        )
    
    return {
        'msg' : {
            'success' : success,
            'errors' : errors
        }
    }

def get_embedding(title, content):
    text = f'title : {title}\ncontent: {content}'
    # 임베딩을 저장용으로 요청한다
    result = es.inference.text_embedding(
        inference_id=".multilingual-e5-small-elasticsearch",
        input=text,
        input_type="ingest" # ingest : 저장할 때  # search : 검색할 때 
    )
    # print('-' * 30)
    # print(text)
    # print(result)

    # 생성한 백터를 반환한다
    # print('차원 :' , len(result['text_embedding'][0]['embedding']))
    return result ['text_embedding'][0]['embedding']
