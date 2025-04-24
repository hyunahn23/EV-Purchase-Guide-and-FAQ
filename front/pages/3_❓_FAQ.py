import streamlit as st
import asyncio
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("API_KEY")
# 페이지 제목
st.markdown("<h1 style='text-align: center;'>EV를 필요로 하는 당신, \n 무엇이든 물어보세요!</h1>", unsafe_allow_html=True)
st.write("---")

# 질문과 답변 리스트
faq_list = [
    ("Q1. 차는 얼마인가요?", "🚗 전기차 가격은 모델과 사양에 따라 다르지만, 일반적으로 4,000만 원에서 1억 원 이상입니다."),
    ("Q2. 충전 시간은 얼마나 걸리나요?", "⚡ 급속 충전은 약 30분~1시간, 완속 충전은 6~8시간 정도 소요됩니다."),
    ("Q3. 주행거리는 얼마나 되나요?", "🛣️ 최신 EV 모델은 한 번 충전으로 최대 500km 이상 주행할 수 있습니다."),
    ("Q4. 배터리 수명은 얼마나 되나요?", "🔋 EV 배터리는 평균 8~10년 사용이 가능하며, 제조사에 따라 보증 기간이 제공됩니다."),
    ("Q5. 충전소는 어디에서 찾을 수 있나요?", "🗺️ 전국 고속도로 휴게소, 대형 마트, 공공기관 등 다양한 장소에서 충전소를 이용할 수 있습니다."),
    ("Q6. EV 유지비는 얼마나 드나요?", "💸 전기차는 연료비와 유지비가 내연기관 차량에 비해 최대 70% 절감됩니다."),
    ("Q7. 국고 보조금은 얼마나 받을 수 있나요?", "💰 국고 보조금은 모델과 지역에 따라 다르며, 최대 800만 원까지 지원됩니다."),
    ("Q8. 겨울철 주행거리는 얼마나 감소하나요?", "❄️ 겨울철에는 난방으로 인해 주행거리가 약 10~20% 감소할 수 있습니다."),
    ("Q9. EV의 충전 비용은 얼마인가요?", "🔌 충전 비용은 kWh당 약 300~400원으로, 내연기관 대비 매우 경제적입니다."),
    ("Q10. EV는 얼마나 안전한가요?", "🛡️ EV는 낮은 무게 중심과 최신 안전 기술 덕분에 매우 안전합니다. 대부분의 모델은 최고 안전 등급을 획득했습니다.")
]



# FAQ 토글 생성
for question, answer in faq_list:
    with st.expander(question):
        st.write(answer)

# 하단 라인
st.write("---")
st.markdown("<h5 style='text-align: center;'>📞 추가 문의는 고객센터로 연락주세요.\n [경기도 광주지점]010-1234-5678</h5>", unsafe_allow_html=True)


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


user_input = st.chat_input("입력")

# localDB.insertData('Me',user_input)

def format_chat_history():
    history_text = ""
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            history_text += f"나: {message['content']}\n"
        else:
            history_text += f"AI: {message['content']}\n"
    return history_text

ai_prompt = ChatPromptTemplate.from_messages([
    ("system", "너는 기본적으로 한국어로 대답해야해 그리고 전기자동차 또는 자동차에 대한 FAQ를 제외하고 다른 내용을 물어볼 경우에는 답할 수 없다고 해"),
    ("user", "대화 내용:\n{chat_history}\n나: {prompt}\nAI:")
])

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    google_api_key=API_KEY,
    temperature=0
)

output_parser = StrOutputParser()

chain = ai_prompt | llm.with_config({"run_name": "model"}) | output_parser.with_config({"run_name": "Assistant"})

def display_chat_history():
    """대화 내역 전체를 출력 (스트리밍 응답 전까지 고정)"""
    for message in st.session_state.chat_history:
        role = "나" if message["role"] == "user" else "AI"
        st.write(f"**{role}:** {message['content']}")

async def generate_response(user_text, ai_placeholder):
    """이전 대화 내용과 함께 AI 응답을 스트리밍"""
    result_text = ""
    conversation_history = format_chat_history()
    prompt_vars = {"chat_history": conversation_history, "prompt": user_text}
    
    async for chunk in chain.astream_events(prompt_vars, version="v1", include_names=["Assistant"]):
        if chunk.get("event") in ["on_parser_start", "on_parser_stream"]:
            if "data" in chunk:
                data = chunk["data"]
                if isinstance(data, dict):
                    data = data.get("chunk", "")
                result_text += data
                
                ai_placeholder.markdown(f"**AI:** {result_text}")
                
    st.session_state.chat_history.append({"role": "assistant", "content": result_text})
    return result_text

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    
    display_chat_history()
    
    ai_placeholder = st.empty()
    
    try:
        asyncio.run(generate_response(user_input, ai_placeholder))
    except Exception as e:
        st.error(f"에러 발생: {e}")
