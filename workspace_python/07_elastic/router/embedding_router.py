# 정규표현식(Regular Expression) 사용을 위한 모듈
import re
import time
from elasticsearch import helpers
from fastapi import APIRouter
from google.genai import types
from utill import es, formatter, gemini, load_documents

# APIRouter 인스턴스 생성 (tags: Swagger UI 문서에서 그룹화 표시에 사용)
router = APIRouter(tags=['임베딩 관련 라우터'])


# ==============================================================================
# 1. 텍스트 분할 및 청킹 (Chunking) 처리
# ==============================================================================
@router.get('/embed/split')
def split(text):
    """입력받은 텍스트를 문장 단위로 분리하고 지정된 길이로 청킹한 결과를 반환합니다."""
    return split_text(text)


def split_text(text):
    """
    긴 본문 텍스트를 문장 단위로 분할하고 적절한 크기의 청크(Chunk)로 결합한 후,
    문맥 단절을 방지하기 위해 앞 청크의 끝부분을 오버랩(Overlap)하여 반환합니다.
    """
    # 1. 마침표, 물음표, 느낌표(.!?) 뒤에 하나 이상의 공백(\s+)이 있는 지점을 기준으로 문장 분리
    sentences = re.split(
        r'(?<=[.!?])\s+',
        text.strip(),  # 본문 양 끝 공백 제거
    )

    # 2. 빈 문자열("")이나 단순 공백만 남은 문장 제거 및 양쪽 공백 정리
    sentences2 = []
    for s in sentences:
        if s.strip():
            sentences2.append(s.strip())
    sentences = sentences2

    # 3. 청킹(Chunking): chunk_size보다 작은 문장들을 하나로 합쳐서 일정한 크기로 묶기
    chunks = []
    chunk_size = 30  # 청크의 기준 글자 수

    temp = ''  # 문장들을 임시로 이어붙여 둘 버퍼 문자열
    for sentence in sentences:
        # 기존 버퍼(temp)에 현재 문장을 공백으로 이어붙여 후보군(candidate) 생성
        if len(temp) > 0:
            candidate = f'{temp} {sentence}'
        else:
            candidate = sentence

        # 합친 길이가 기준 청크 사이즈(30자) 이하라면 버퍼에 누적 유지
        if len(candidate) <= chunk_size:
            temp = candidate
        else:
            # 기준 길이를 초과하면, 지금까지 누적된 버퍼(temp)를 하나의 청크로 확정
            if len(temp) > 0:
                chunks.append(temp)
            # 넘쳐서 못 들어간 현재 문장으로 새로운 버퍼 시작
            temp = sentence

    # 루프 종료 후 버퍼(temp)에 남아있는 마지막 문장 덩어리 청크에 추가
    if len(temp) > 0:
        chunks.append(temp)

    # 4. 오버랩(Overlap) 적용: 청크 간 경계에서 문맥 단절을 방지하기 위해 앞 청크의 뒷부분(6자)을 가져와 접두사로 결합
    overlap_size = 6
    overlap_chunks = []
    for index, chunk in enumerate(chunks):
        if index == 0:
            # 첫 번째 청크는 이전 청크가 없으므로 원본 그대로 추가
            overlap_chunks.append(chunk)
            continue

        before = chunks[index - 1]  # 직전 청크
        prefix = before[-overlap_size:]  # 직전 청크의 마지막 6글자 추출
        now = f'{prefix} {chunk}'.strip()  # 현재 청크 앞에 붙여 문맥 연결
        overlap_chunks.append(now)

    return overlap_chunks


# ==============================================================================
# 2. Elasticsearch 인덱스 생성 및 매핑 정의
# ==============================================================================
@router.post('/embed/create')
def create_embed_index():
    """
    'computer_chunk' 인덱스를 초기화하고 dense_vector 필드를 포함한 매핑을 새로 정의합니다.
    """
    # 기존 인덱스가 존재하면 삭제 (테이블 DROP과 유사)
    if es.indices.exists(index='computer_chunk'):
        es.indices.delete(index='computer_chunk')

    # 새로운 인덱스 및 필드 매핑 생성
    es.indices.create(
        index='computer_chunk',
        mappings={
            'properties': {
                'id': {'type': 'integer'},
                'title': {
                    'type': 'text'
                },  # 형태소 분석 기반 유연한 텍스트 검색 가능
                'category': {
                    'type': 'keyword'
                },  # 부분 일치 없이 완벽히 일치하는 단어로만 필터링
                'price': {'type': 'integer'},
                'rating': {'type': 'float'},
                'created_at': {'type': 'date'},
                'content': {'type': 'text'},
                'chunk_index': {
                    'type': 'integer'
                },  # 문서 내 몇 번째 청크인지를 식별하는 인덱스
                'embedding': {
                    'type': 'dense_vector',
                    'dims': 384,  # Gemini 임베딩 벡터 차원 수 (output_dimensionality와 일치)
                },
            }
        },
    )
    return 'computer_chunk index 생성 완료'


# ==============================================================================
# 3. 데이터 벌크 수집 (Bulk Ingestion) 및 임베딩 처리
# ==============================================================================
@router.post('/embed/insert/bulk')
def ingest_embed_documents():
    """
    JSON 원본 문서를 청크로 분할하고, Gemini API로 벡터 임베딩을 생성한 후
    Elasticsearch에 대량(Bulk)으로 색인합니다.
    """
    documents = load_documents()  # 원본 JSON 파일/DB에서 문서 리스트 로드

    actions = []
    call_count = 0  # API 호출 횟수 카운터

    for doc in documents:
        # 각 문서의 본문(content)을 청크 단위로 분할
        chunks = split_text(doc['content'])

        for index, chunk in enumerate(chunks):
            # Gemini 임베딩 모델을 호출하여 384차원 벡터 생성
            embedding = get_embedding_with_llm(doc['title'], chunk)
            call_count += 1
            print(f'[{call_count}번째 청크 임베딩 완료]')

            # Gemini 무료 티어의 분당 호출 수(RPM) 제한 준수를 위해 매 호출마다 슬립 설정 권장
            time.sleep(0.7)

            if call_count % 30 == 0:
                print(f'>>> {call_count}회 호출 누적 완료')

            # [중요] .copy()로 복사본을 만들어야 루프 내에서 이전 청크 데이터가 오염되지 않음
            doc2 = doc.copy()
            doc2['chunk_index'] = index  # 현재 청크의 순번 기록
            doc2['content'] = chunk # 쪼갠 텍스트로 덮어쓰기
            doc2['embedding'] = embedding  # 추출한 384차원 임베딩 벡터 주입

            # Elasticsearch 벌크 작업 리스트에 추가 (도큐먼트 ID는 "문서ID-청크번호"로 고유화)
            actions.append({
                '_index': 'computer_chunk',
                '_id': f'{doc2["id"]}-{index}',
                '_source': doc2,
            })

    # bulk API를 이용해 한 번의 요청으로 대량 색인 실행
    success, errors = helpers.bulk(
        es,
        actions,
        stats_only=False,  # False 설정 시 실패한 건의 상세 에러 로그까지 반환
    )

    return {'msg': {'success': success, 'errors': errors}}


# ==============================================================================
# 4. 벡터 임베딩 추출 함수군
# ==============================================================================
def get_embedding(title, content):
    """Elasticsearch 내장 추론 모델(.multilingual-e5-small)을 이용한 저장용 벡터 생성"""
    text = f'title : {title}\ncontent: {content}'
    result = es.inference.text_embedding(
        inference_id='.multilingual-e5-small-elasticsearch',
        input=text,
        input_type='ingest',  # 색인/저장용
    )
    return result['text_embedding'][0]['embedding']


def get_embedding_with_llm(title, content):
    """Google Gemini LLM을 이용하여 문서 저장용 384차원 벡터 생성"""
    # 태스크 지시사항(Task Prompt)을 붙여 검색 정확도 향상 유도
    prompt = f"""
        task: retrieval document
        title: {title}
        content: {content}
    """
    result = gemini.models.embed_content(
        model='gemini-embedding-2',
        contents=[types.Content(parts=[types.Part.from_text(text=prompt)])],
        config=types.EmbedContentConfig(output_dimensionality=384),  # 차원 축소 설정
    )
    return result.embeddings[0].values


def get_keyword_embedding(keyword):
    """Elasticsearch 내장 추론 모델을 이용한 검색 쿼리용 벡터 생성"""
    result = es.inference.text_embedding(
        inference_id='.multilingual-e5-small-elasticsearch',
        input=keyword,
        input_type='search',  # 질의/검색용
    )
    return result['text_embedding'][0]['embedding']


def get_keyword_embedding_with_llm(keyword):
    """Google Gemini LLM을 이용하여 사용자 검색 질의(Query)용 384차원 벡터 생성"""
    prompt = f"""
        task: retrieval query
        query: {keyword}
    """
    result = gemini.models.embed_content(
        model='gemini-embedding-2',
        contents=[types.Content(parts=[types.Part.from_text(text=prompt)])],
        config=types.EmbedContentConfig(output_dimensionality=384),
    )
    return result.embeddings[0].values


# ==============================================================================
# 5. 검색 엔드포인트 (KNN 벡터 검색 vs RRF 하이브리드 검색)
# ==============================================================================
@router.get('/embed/search/vector')
def search_vector(keyword):
    """
    순수 KNN(K-Nearest Neighbors) 벡터 검색:
    입력된 키워드의 의미적 유사도(코사인 유사도 등)를 기준으로 근접한 문서를 검색합니다.
    """
    # 검색어를 384차원 벡터로 변환
    vector_keyword = get_keyword_embedding_with_llm(keyword)

    size = 5  # 최종적으로 가져올 상위 문서 개수
    response = es.search(
        index='computer_chunk',
        knn={
            'field': 'embedding',  # 비교할 인덱스 내 벡터 필드명
            'query_vector': vector_keyword,  # 사용자 질의 벡터
            # 후보군(num_candidates): 전체 데이터에서 근사치로 먼저 넉넉하게 뽑아둘 후보 수 (최소 50개)
            'num_candidates': max(size * 10, 50),
            # 후보군 중 가장 유사도가 높은 최상위 k개 선택
            'k': size,
        },
        size=size,
    )

    return formatter(response)


@router.get('/embed/search/hybrid')
def hybrid(keyword):
    """
    하이브리드 검색 (Hybrid Search):
    1) BM25 키워드 일치 검색(multi_match)
    2) KNN 의미론적 벡터 유사도 검색
    두 검색 결과의 순위를 RRF(Reciprocal Rank Fusion) 알고리즘으로 결합하여 최적의 결과를 도출합니다.
    """
    size = 5
    vector_keyword = get_keyword_embedding_with_llm(keyword)

    response = es.search(
        index='computer_chunk',
        size=size,
        # Elasticsearch 8.x 이상에서 지원하는 retriever 기능 활용
        retriever={
            'rrf': {
                'rank_constant': 60,  # 랭킹 점수 계산 가중치 상수 (순위 격차 영향력 완화)
                'rank_window_size': max(
                    size * 10, 50
                ),  # RRF 결합 연산에 포함할 상위 순위 범위
                'retrievers': [
                    # 1. 형태소 기반 키워드 검색기 (BM25)
                    {
                        'standard': {
                            'query': {
                                'multi_match': {
                                    'query': keyword,
                                    'fields': ['title', 'content'],
                                }
                            }
                        }
                    },
                    # 2. 코사인 유사도 기반 KNN 벡터 검색기
                    {
                        'knn': {
                            'field': 'embedding',
                            'query_vector': vector_keyword,
                            'num_candidates': max(size * 20, 100),
                            'k': size * 10,
                        }
                    },
                ],
            }
        },
    )
    return formatter(response)

# RAG (Retrieval-Augmented Generation) 검색 증강 생성 
@router.get('/embed/ask')
def ask_rag(question):
    # 하이브리드 검색
    results = hybrid(question)['results']

    # 검색 결과를 제미나이용으로 가공 
    contexts = [ ]
    for idx,  result in enumerate(results):
        print('>>>>>>>>>>>>' , result)
        contexts.append(f'''
            [검색 결과 : {idx}]
            문서 ID : {result['document']['id']}
            청크 번호 : {result['document']['chunk_index']}
            제목 : {result['document']['title']}
            카테고리 : {result['document']['category']}
            내용 : {result['document']['content']}
        ''')

    # 리스트를 string으로 변환 
    context =  "\n--------\n".join(contexts)

    prompt = f'''
        너는 문서 기반 지식 검색 도우미야.

        아래의 **context**에 포함된 내용만으로 질문에 답해야만해.

        ** 규칙 : 
        1 절대 추론이나 다른 내용을 담으면 안돼.
        2 내용에 없는 질문이라면 "문서에서 확인할 수 없는 질문입니다" 라고 답변해줘.
        3 한국어로 답변해줘
        4 불필요하게 긴 설명을 하지 말아줘
        5 답변에 대한 근거를 자연스럽게 설명해줘

        ** 질문 : {question} 

        ** context  : {context}
    '''.strip()
    print('prompt : ' , prompt)

    answer = ask_gemini(prompt)
    print('answer :' , answer)

    return answer

def ask_gemini(prompt) :

    response =  gemini.models.generate_content(
        model='gemini-3.8-flash',
        contents=prompt
    )
    print('ask_gemini : ' , response)
    return response.text
    


