import os
from dotenv import load_dotenv
import openai
from openai import OpenAI

# 파일 불러오기
load_dotenv()
api_key = os.getenv('open_ai_key')
# print("확인 : ",api_key)

# 외부연결이기에 try-except
client = OpenAI(api_key=api_key)
# message1 = input('챗gpt 검색을 시작합니다. 검색할 내용을 입력하세요.>> ')
try:
    # 챗gpt 연결
    response = client.responses.create(
        model = 'gpt-5.6',  # 사용할 모델
        instructions = "한국어로 친절하고 간결하게 답해줘요.",  # 지시사항,규칙
        # input = message1   # 전달메세지
        input = 'api 연결확인 환영문자를 짧게 작성해 주세요.'
    )
except openai.APIConnectionError as error:
    print(f'api 연결에러 : {error}')
except openai.RateLimitError as error:
    print(f'api 요청한도에러 : {error}')
except openai.APIError as error:
    print(f'api 요청실패 {error}')

result = response.output_text.strip()
if not result:
    raise RuntimeError('api 응답에 표시할 텍스트가 없습니다.')
print('-'*40)
print(response)
print('-'*40)
print('[ 응답 ]',result)




