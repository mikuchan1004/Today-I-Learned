from fastapi import APIRouter
import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from openai import OpenAI
from google import genai
from google.genai import types
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

router = APIRouter(tags=["langchain"])
load_dotenv()

# 그냥 gpt에 말하기 (단발성)
@router.get('/langchain/gpt')
def gpt(prompt:str):
    model = ChatOpenAI(
        model='gpt-5.5',
        temperature=0,
        api_key=os.getenv('OPENAI_API_KEY')
    )
    output = model.invoke(prompt)
    return output

# 멀티턴으로 gpt에 말하기
@router.get('/langchain/gpt/multi')
def gpt_multi(prompt:str):
    model = ChatOpenAI(
        model='gpt-5.5',
        temperature=0,
        api_key=os.getenv('OPENAI_API_KEY')
    )

    messages= [
        {'role' : 'system', 'content' : '너는 친절한 조수야'},
        {'role' : 'user' , 'content' : '내 이름은 상우야'},
        {'role' : 'assistant' , 'content' : '안녕하세요! 상우님! 어떤 도움이 필요하신가요?'},
        {'role' : 'user' , 'content' : prompt}
    ]
    output = model.invoke(messages)
    # 실제 대답은 output.content에 들어있다.
    return output

@router.get('/original/gpt')
def original_gpt(prompt:str):
# 쌩으로 apenai 모델 사용법
    client = OpenAI(api_key = os.getenv('OPENAI_API_KEY'))

    messages= [
            {'role' : 'system', 'content' : '너는 친절한 조수야'},
            {'role' : 'user' , 'content' : '내 이름은 상우야'},
            {'role' : 'assistant' , 'content' : '안녕하세요! 상우님! 어떤 도움이 필요하신가요?'},
            {'role' : 'user' , 'content' : prompt}
        ]

    output = client.chat.completions.create(
        model='gpt-5.5',
        messages=messages
        )
    # 실제 대답은 choices[0].message.content에 들어있다.
    return output

# genai 모듈 사용
@router.get('/original/gemini')
def original_gemini(prompt:str):
    # 쌩으로 genai 모듈 사용법
    client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

    # gemini는 사용할 때 
    # role에 system 없음
    # parts로 적어야함
    messages= [
        # {'role' : 'system', 'content' : '너는 친절한 조수야'},
        {'role' : 'user' , 'parts' : [{'text' : '내 이름은 상우야'}]},
        # {'role' : 'assistant' , 'content' : '안녕하세요! 상우님! 어떤 도움이 필요하신가요?'},
        {'role' : 'model' , 'parts' : [{'text' : '안녕하세요! 상우님! 어떤 도움이 필요하신가요?'}]},
        {'role' : 'user' , 'parts' : [{'text' : prompt}]}
    ]

    output = client.models.generate_content(
        model='gemini-3.8-flash',
        contents = messages,
        config=types.GenerateContentConfig(
            system_instruction="너는 친절한 조수야",
            temperature=0.0
        )
    )
    # 실제 대답은 candidates[0].content.parts[0].text에 들어있다.
    return output

# langchain 모듈 사용
@router.get('/langchain/gemini')
def langchain_gemini(prompt:str):
    model = ChatGoogleGenerativeAI(
        model='gemini-3.8-flash',
        temperature=0,
        api_key=os.getenv('GEMINI_API_KEY')
    )
    messages= [
            {'role' : 'system', 'content' : '너는 친절한 조수야'},
            {'role' : 'user' , 'content' : '내 이름은 상우야'},
            {'role' : 'assistant' , 'content' : '안녕하세요! 상우님! 어떤 도움이 필요하신가요?'},
            {'role' : 'user' , 'content' : prompt}
        ]
    output = model.invoke(messages)

    # 실제 대답은 output.content[0].text
    return output

# langchain의 message 모듈 사용해서 질문하기
@router.get('/langchain/gpt/message')
def gpt_message(prompt:str):
    model = ChatOpenAI(
        model='gpt-5.5',
        temperature=0,
        api_key=os.getenv('OPENAI_API_KEY')
    )

    # provider에 따라 형식을 맞춰준다
    messages= [
        SystemMessage("너는 친절한 조수야"),
        HumanMessage("내 이름은 상우야"),
        AIMessage("안녕하세요. 상우님! 친절히 알려드릴게요"),
        HumanMessage(prompt)
  
    ]
    
    output = model.invoke(messages)

    # 실제 대답은 output.content에 들어있다.
    return output

# stream으로 출력하기
@router.get('/langchain/gpt/stream')
def gpt_stream(prompt:str):
    model = ChatOpenAI(
        model='gpt-5.5',
        temperature=0,
        api_key=os.getenv('OPENAI_API_KEY')
    )

    # provider에 따라 형식을 맞춰준다
    messages= [
        SystemMessage("너는 친절한 조수야"),
        HumanMessage("내 이름은 상우야"),
        AIMessage("안녕하세요. 상우님! 친절히 알려드릴게요"),
        HumanMessage(prompt)
  
    ]

    for chunk in model.stream(messages):
        print(chunk.content, end="" , flush=True)

@router.get('/langchain/gpt/chat_prompt_template')
def chat_prompt_template(name: str, prompt:str):
    prompt_template = ChatPromptTemplate.from_messages([
        ("system" , "너는 친절한 조수야"),
        ("human" , "내 이름은 {name}야"),
        ("ai" , "안녕하세요. {name}님! 친절하게 알려드릴게요"),
        ("human" , "{prompt}") # 아직 "{prompt}"라는 글씨일 뿐이다.
    ])

    prompt_template.invoke({
        "name" : name,
        "prompt" : prompt 
    })

    print(prompt_template)

@router.get('/langchain/gpt/message_placeholder')
def message_placeholder(name: str, prompt:str):
    prompt_template = ChatPromptTemplate.from_messages([
        ("system" , "너는 친절한 조수야"),
        MessagesPlaceholder("history" , optional=True),
        ("human" , "내 이름은 {name}야"),
        ("ai" , "안녕하세요. {name}님! 친절하게 알려드릴게요"),
        ("human" , "{prompt}") # 아직 "{prompt}"라는 글씨일 뿐이다.
    ])

    prompt_template.invoke({
        "history" : [
            HumanMessage("내 이름은 상우야"),
            AIMessage("안녕하세요, 상우님! 친절히 알려드릴게요")
        ],
        "name" : name,
        "prompt" : prompt 
    })

    print(prompt_template)