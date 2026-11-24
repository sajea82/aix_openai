import json
import os
from pathlib import Path
from dotenv import load_dotenv
from django.http import JsonResponse
from django.shortcuts import render
import openai
from openai import OpenAI

# -------------------------------------------------------------------
# 1. key 가져오기
# views.py 위치: .../webProject/tour_pjt/tour/views.py
# .env 위치: .../aix_openai/.env -> parents[3]
BASE_DIR = Path(__file__).resolve().parents[3]
envFile = BASE_DIR / ".env"
load_dotenv(envFile)

api_key = os.getenv("open_ai_key") or os.getenv("OPENAI_API_KEY")

# -------------------------------------------------------------------
# 여행지 소개 txt 파일 경로 (tour 폴더 바로 아래 tour_intro.txt)
INTRO_FILE = Path(__file__).resolve().parent / "tour_intro.txt"


def get_intro_from_txt(place_name: str) -> str:
    """tour_intro.txt에서 입력한 여행지 소개를 찾아 반환합니다."""
    if not INTRO_FILE.exists():
        return "tour_intro.txt 파일을 찾을 수 없습니다."

    raw_text = INTRO_FILE.read_text(encoding="utf-8")
    blocks = raw_text.strip().split("\n\n")

    for block in blocks:
        if place_name in block:
            return block.strip()

    return f"'{place_name}'에 대한 직접 전달 소개 내용이 tour_intro.txt에 아직 없습니다."


def generate_bus_course(place_name: str) -> str:
    """1박 2일 여행 코스(여행일정, 여행지, 숙소, 식사추천)를 생성합니다."""
    client = OpenAI(api_key=api_key)
    response = client.responses.create(
        model="gpt-5.6",  # 현재 사용 중인 모델명 유지
        instructions=(
            "당신은 여행설계 전문가입니다."
            "여행 일정을 1박2일 코스로 설계해 주세요."
            "[여행]으로 알려주세요."
            "반드시 [여행일정], [여행지], [숙소], [식사추천] 항목을 포함해 주세요."
            "여행자가 이해하기 쉽게 간략하게 답합니다."
        ),
        input=(
            f"{place_name}를 가지고 [1박2일코스]-여행으로 설계해 주세요. "
            "구성: 여행일정, 여행지, 숙소, 식사추천"
        ),
        max_output_tokens=1000,
    )
    result = (response.output_text or "").strip()
    if not result:
        raise RuntimeError("응답결과 내용이 없습니다.")
    return result


# -------------------------------------------------------------------
# 2. 뷰 처리 (GET: 페이지 렌더링 / POST: AJAX JSON 응답)
def tour(request):
    if request.method == "POST":
        place_name = ""
        if request.content_type and "application/json" in request.content_type:
            body = json.loads(request.body.decode("utf-8") or "{}")
            place_name = (body.get("place") or "").strip()
        else:
            place_name = (request.POST.get("place") or "").strip()

        if not place_name:
            return JsonResponse(
                {"error": "여행지를 입력하셔야 검색이 가능합니다."},
                status=400,
            )

        intro_text = get_intro_from_txt(place_name)

        try:
            course_text = generate_bus_course(place_name)
        except openai.APIConnectionError as error:
            return JsonResponse(
                {"error": f"인터넷연결, 방화벽 문제 등 확인 : {error}"},
                status=500,
            )
        except openai.RateLimitError as error:
            return JsonResponse(
                {"error": f"요청량 또는 프로젝트 사용한도 확인 : {error}"},
                status=500,
            )
        except openai.APIError as error:
            return JsonResponse(
                {"error": f"인증,권한 등 api 오류 확인 : {error}"},
                status=500,
            )
        except Exception as error:
            return JsonResponse(
                {"error": f"처리 중 오류 발생 : {error}"},
                status=500,
            )

        return JsonResponse({
            "place": place_name,
            "intro": intro_text,
            "course": course_text,
        })

    return render(request, "tour.html")
