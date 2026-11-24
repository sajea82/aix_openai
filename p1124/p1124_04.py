# 경제전문가입니다.
# 2027년 주식시세가 어떻게 될지 알려주는 프로그램을 구현하시오.
# 반도체주, 전력시설주, 우주항공주
# 500자 이내로 짧게 알려줘

import os
from pathlib import Path
from dotenv import load_dotenv
import openai
from openai import OpenAI

# key 가져오기
BASE_DIR = Path(__file__).resolve().parent.parent
envFile = BASE_DIR/'.env'
load_dotenv(envFile)
api_key = os.getenv('open_ai_key')
print(api_key)

# 검색어 입력부분
while True:
    txt_input = input('2027년 알고싶은 주식을 입력하세요.>> ').strip()
    if txt_input : break
    print('주식 이름을 입력하셔야 검색이 가능합니다.')
    print()

# OpenAI client 연결부분
client = OpenAI(api_key=api_key)

try: 
    response = client.responses.create(
        model = 'gpt-5.6',
        instructions = (
            "당신은 주식시세 경제전문가입니다. "
            "2027년 주식시세를 알려주세요. "
            "[반도체주]만 다루어 알려주세요. "
            "초보자도 쉽게 이해하기 쉽게 500자 이내로 간략하게 답합니다."
        ),
        input=(
            f"종목명: {txt_input} (반도체주)\n"
            "2027년 주식시세 전망을 초보자가 이해하기 쉽게 아래 4가지 항목을 포함해 500자 이내로 알려주세요.\n"
            "1. 현재 주가 흐름 및 2027년 전반적 시세 전망\n"
            "2. 핵심 상승 동력 (HBM 장기공급계약, AI 수요, 주주환원)\n"
            "3. 주요 리스크 요인 (빅테크 AI 투자 둔화 우려, 2028년 메모리 공급 증가 가능성)\n"
            "4. 투자 시 체크포인트 한 줄 요약"
        ),
        max_output_tokens=500,
    )

except openai.APIConnectionError as error:
    print(f"인터넷연결, 방화벽 문제 등 확인 : {error}")
except openai.RateLimitError as error:
    print(f"요청량 또는 프로젝트 사용한 확인 : {error}")
except openai.APIError as error:
    print(f"인증,권한 등 api 오류 확인 : {error}")
    
# 결과확인
result = response.output_text.strip()
if not result:
    raise RuntimeError('응답결과 내용이 없습니다.')
print(f'[ {txt_input} 주식시세정보]')
print(result)

print('완료!')




