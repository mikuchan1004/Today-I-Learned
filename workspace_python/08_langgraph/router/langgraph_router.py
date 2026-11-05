import os
from typing import Literal, Optional
from dotenv import load_dotenv
from fastapi import APIRouter, Query
from pydantic import BaseModel

# LangChain & LangGraph 관련 모듈
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser
from langgraph.graph import StateGraph, START, END

# Elasticsearch 및 추천 알고리즘 함수
from router.es_router import content_based_filtering, collaborative_filtering, search_movies, term_movieId

router = APIRouter(tags=["langgraph"])
load_dotenv()

'''
[워크플로우 요약]
1. 사용자 입력 접수: list_movieId, userId, question 등
2. 추천 방식 라우팅 (recommend_select): 질문 의도를 파악하여 CBF, CF, BM25 중 하나 선택
3. 추천 엔진 실행 (cbf, cf, bm25): 선택된 알고리즘으로 영화 검색 및 표준화(normalize)
4. 결과 설명 생성 (explain): 추천된 영화 목록을 바탕으로 LLM이 사용자 맞춤 설명 생성 후 종료
'''

# ==========================================
# 1. State 정의 (LangGraph 공유 데이터 모델)
# ==========================================
class State(BaseModel):
    """
    LangGraph의 각 노드가 읽고 쓰는 공유 상태 객체.
    노드 함수가 반환(return)하는 딕셔너리의 key 이름과 일치하는 필드가 자동으로 업데이트됨.
    """
    list_movieId: Optional[list[int]] = None       # CBF(콘텐츠 기반)에 사용할 기준 영화 ID 목록
    userId: Optional[int] = None                   # CF(협업 필터링)에 사용할 사용자 ID
    top_k: int = 10                                # 최종 추천 결과 개수
    
    question: str                                  # 사용자 입력 질문

    recommend_type: Optional[str] = None           # 선정된 추천 방식 ('CBF', 'CF', 'BM25')
    recommend_type_reason: Optional[str] = None    # 해당 추천 방식을 선정한 이유

    # 주의: 리스트 형태[dict, dict, ...]로 유지되어야 함 (Pydantic ValidationError 방지)
    recommends: Optional[list[dict]] = []          # 정규화된 영화 추천 결과 리스트

    explain: Optional[str] = "LLM 응답 없음"       # 최종 LLM 생성 설명 텍스트

    error : Optional[str] = None # 에러 메시지


# ==========================================
# 2. 구조화된 출력(Structured Output) 스키마
# ==========================================
class RecommendType(BaseModel):
    """LLM이 질문을 분석하고 반환할 JSON 구조"""
    recommend_type: Literal['CBF', 'CF', 'BM25'] = 'CBF'  # 결정된 추천 알고리즘
    recommend_type_reason: str                            # 판단 근거


# ==========================================
# 3. 노드(Node) 함수 정의
# ==========================================

def recommend_select(state: State):
    """[노드 1] 질문 분석 및 적절한 추천 알고리즘 선정"""
    prompt = ChatPromptTemplate.from_messages([
        ('system', '''
            당신은 영화 추천 시스템의 추천 방식을 선택하는 역할이다.
            사용자 질문의 의도를 분석하고 파악해서 세가지 중 하나만 선택하시오.

            1. [CBF]
                - 특정 영화와 비슷한 영화를 찾는 경우
                - 장르와 사용자들의 태그 기반으로 추천하는 경우 
            2. [CF]
                - 사용자의 취향과 비슷한 다른 사람들의 평점 패턴 분석 기반으로 추천하는 경우
            3. [BM25]
                - 제목, 장르, 태그 등의 키워드로 검색하는 경우
        '''),
        ('human', '*** 사용자 질문 : {question}')
    ])

    model = ChatOpenAI(
        model='gpt-5.5',
        temperature=0,
        api_key=os.getenv('OPENAI_API_KEY')
    )
    
    # 구조화된 출력(Pydantic) 파이프라인 생성
    chain = prompt | model.with_structured_output(RecommendType)

    result = chain.invoke({
        'question': state.question
    })
    print('recommend_select >> result : ', result)

    # State의 recommend_type 및 recommend_type_reason 필드 업데이트
    return {
        'recommend_type': result.recommend_type,
        'recommend_type_reason': result.recommend_type_reason
    }


def normalize(response, top_k):
    """Elasticsearch 검색 결과(hit)를 State.recommends에 맞는 순수 리스트 구조로 정규화"""
    movieIds = set()
    recommends = []

    for hit in response['hits']['hits']:
        source = hit['_source']
        movieId = source.get('movieId')
        
        # 중복 영화 ID 제거
        if movieId not in movieIds: 
            movieIds.add(movieId)
            recommends.append({
                'movieId': movieId,
                'title': source.get('title', ' '),
                'genres': source.get('genres', []),
                'tags': source.get('tags', []),
                'score': hit.get('_score', -1)
            })

    # 중요: 딕셔너리가 아닌 순수 리스트(list[dict])로 반환해야 State.recommends 타입 오류가 안 남
    return recommends[:top_k]


def bm25(state: State):
    """[노드 2-A] 키워드 기반 BM25 영화 검색"""
    response = search_movies(state.question)
    recommends = normalize(response, state.top_k)
    return {
        'recommends': recommends
    }


def cbf(state: State):
    """[노드 2-B] 콘텐츠 기반 필터링 (영화 태그/장르 유사도)"""
    response = content_based_filtering(state.list_movieId)
    recommends = normalize(response, state.top_k)
    return {
        'recommends': recommends
    }


def cf(state: State):
    """[노드 2-C] 사용자 평점 패턴 기반 협업 필터링"""
    result = collaborative_filtering(state.userId)
    movieIds = set()
    for info in result:
        movieIds.add(info.get('movieId', 0))
    
    # TODO: 추출한 movieIds를 기반으로 term_movieId 조회 후 normalize 처리 로직 보완 필요
    response = term_movieId(list(movieIds)) if callable(term_movieId) else {}
    recommends = normalize(response, state.top_k) if response else []
    
    return {
        'recommends': recommends
    }


def explain(state: State):
    """[노드 3] 추천된 영화 목록을 분석하여 사용자 맞춤형 설명 텍스트 작성"""
    prompt = ChatPromptTemplate.from_messages([
        ('system', '''
            당신은 영화 추천 시스템의 추천 결과를 설명하는 역할이다.
            설명을 상세하게 해서 꼭 볼 수 밖에 없는 설득력을 가지고 있다.
            간략하게 주요 내용만 설명한다

            [주의사항]
                - 결과에 없는 영화를 추천하지 않는다.
                - 제목을 한국것으로 검색해서 원제와 함께 알려준다.
        '''),
        ('human', ''' 
            [사용자 질문] : {question}
            [검색 방식] : {recommend_type}
            [검색 결과] 
            {recommends}
            [할 일] : 위 정보로 사용자에게 잘 설명하시오.
        ''')
    ])

    model = ChatOpenAI(
        model='gpt-5.5',
        temperature=0,
        api_key=os.getenv('OPENAI_API_KEY')
    )
    chain = prompt | model | StrOutputParser()

    # 프롬프트의 {question}, {recommend_type}, {recommends}를 매핑하여 호출
    result = chain.invoke({
        'question': state.question,
        'recommend_type': state.recommend_type,
        'recommends': state.recommends
    })
    print('explain >> result : ', result)

    # State의 explain 필드 업데이트
    return {
        'explain': result
    }

def validator(state : State):

    rec_type = state.recommend_type

    if rec_type == 'CBF' and not state.list_movieId:
            return 'ERROR'

    if rec_type == 'CF' and state.userId is None :
            return 'ERROR'

    return rec_type

def makeErrorMessage(state : State):

    rec_type = state.recommend_type

    error = "요청을 처리할 수 없습니다."
    
    if rec_type == 'CBF' and not state.list_movieId:
            error = 'list_movieId는 필수입니다.'
    elif rec_type == 'CF' and state.userId is None:
            error = 'userId는 필수입니다.'

    return {
        'error' : error
    }

# ==========================================
# 4. FastAPI 엔드포인트 및 Graph 조립
# ==========================================
@router.post('/langgraph/recommend')
def recommend(param: State):
    """FastAPI 진입점: StateGraph 구성, 컴파일 및 워크플로우 실행"""
    print(param)

    # 1. State 기반 그래프 생성
    graph = StateGraph(State)

    # 2. 노드 등록
    graph.add_node('select', recommend_select)
    graph.add_node('CBF', cbf)
    graph.add_node('CF', cf)
    graph.add_node('BM25', bm25)
    graph.add_node('explain', explain)
    graph.add_node('makeErrorMessage' , makeErrorMessage)

    # 3. 엣지 연결: 시작 노드 지정
    graph.add_edge(START, 'select')

    # 4. 조건부 분기 (Conditional Edge): recommend_select의 결과(recommend_type)에 따라 분기
    graph.add_conditional_edges(
        'select', 
        # lambda s: s.recommend_type,
        validator,
        {
            'CBF': 'CBF',
            'CF': 'CF',
            'BM25': 'BM25',
            'ERROR'  : "makeErrorMessage"
        }
    )

    # 5. 각 추천 노드 종료 후 explain 노드로 집결
    graph.add_edge('CBF', 'explain')
    graph.add_edge('CF', 'explain')
    graph.add_edge('BM25', 'explain')
    
    # 6. 설명 생성 완료 후 종료(END)
    graph.add_edge('explain', END)
    graph.add_edge('makeErrorMessage' , END)

    # 7. 그래프 컴파일 및 실행
    recommend_graph = graph.compile()
    result = recommend_graph.invoke({
        'list_movieId': param.list_movieId,
        'userId': param.userId,
        'top_k': param.top_k,
        'question': param.question,
        'recommends': [],
    })

    return result