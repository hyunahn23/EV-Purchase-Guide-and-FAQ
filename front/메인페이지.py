
import streamlit as st
import streamlit.components.v1 as html
import base64
from PIL import Image, ImageSequence
import os

# 현재 스크립트 파일의 절대 경로를 구합니다.
current_dir = os.path.dirname(os.path.abspath(__file__))


# st.title('The Ultimate EV Choice! ⚡')
# st.write('---')
# st.header('현대·기아·테슬라 전기차 비교, 최고의 선택을 위한 인사이트!')
# # st.markdown('3가지 전기 자동차 브랜드 관련 정보를 제공합니다.')
# # st.markdown('메뉴에서 원하는 페이지를 선택하세요!')


# # 로컬 GIF 파일 경로
# gif_path = "C:/Users/Playdata/OneDrive/바탕 화면/ev.gif"  # 여기에 로컬 GIF 파일의 경로를 입력하세요.

# # Base64로 GIF 읽기 및 HTML 삽입
# with open(gif_path, "rb") as gif_file:
#     gif_data = gif_file.read()
#     gif_base64 = base64.b64encode(gif_data).decode("utf-8")

# st.markdown(
#     f'<img src="data:image/gif;base64,{gif_base64}" alt="EV Comparison" style="width:100%; height:auto;">',
#     unsafe_allow_html=True,
# )


# GIF 파일 경로 설정 (Menu.py 기준 상대 경로)
gif_path = "./pages/gif/ev.gif"  # 슬래시(/)를 사용한 상대 경로

# GIF 파일 존재 여부 확인
try:
    with open(gif_path, "rb") as gif_file:  # GIF 파일 열기
        gif_data = gif_file.read()  # 파일 데이터를 읽습니다.
        gif_base64 = base64.b64encode(gif_data).decode("utf-8")  # Base64 인코딩

    # Streamlit에서 GIF 표시
    st.title('The Ultimate EV Choice! ⚡')  # 제목 표시
    st.write('---')  # 구분선 표시
    st.header('현대·기아·테슬라 전기차 비교, 최고의 선택을 위한 인사이트!')  # 헤더 표시

    # HTML <img> 태그를 사용해 Base64 인코딩된 GIF 표시
    st.image("./pages/gif/ev.gif", use_container_width=True)
    # st.markdown(
    #     f'<img src="data:image/gif;base64,{gif_base64}" alt="EV Comparison" style="width:1000; height:770;">',
    #     unsafe_allow_html=True,
    # )
except FileNotFoundError:
    st.error(f"GIF 파일을 찾을 수 없습니다: {gif_path}")
