import streamlit as st
import plotly.graph_objects as go
import requests

url = 'http://127.0.0.1:8000/api'

# 데이터 불러오기
data = requests.get(url + '/brand-info').json()["resData"]
car_data = requests.get(url + '/car-info').json()["resData"]
regions = requests.get(url + '/region-info').json()["resData"]

# 영문 필드명을 한글로 매핑하는 딕셔너리 (SUBSIDY 값을 "국고 지원금"으로 변경)
korean_mapping = {
    "CAR_CODE": "자동차 코드",
    "MODEL_NAME": "모델명",
    "PRICE": "가격",
    "CAR_TYPE": "차종",
    "FUEL_EFFICIENCY": "연비",
    "FUEL_TYPE": "연료 종류",
    "MAX_DISTANCE": "최대 주행거리",
    "SUBSIDY": "국고 지원금",
    "BRAND_NAME": "브랜드명",
    "IMG_URL": "대표 이미지 URL"
}

st.set_page_config(page_title="전기차 모델 비교", page_icon="🚗", layout="wide")
st.title("🔍 전기차 모델 성능 및 국고 지원금 비교")

theme_toggle = st.toggle("🌗 다크 모드 활성화", value=False)
if theme_toggle:
    st.markdown("""
    <style>
        .main, .block-container {
            background-color: #2E2E2E;
            color: white;
        }
        .stButton>button, .stSelectbox>div>div {
            color: white;
            background-color: #3E3E3E;
        }
    </style>
    """, unsafe_allow_html=True)

compare = st.toggle("✨ 두 모델 비교", value=False)

col1, col2 = st.columns(2)

def display_car_info(model, region, key_prefix=""):
    if not (model and region):
        return None, None, None

    model_info = requests.get(url + '/car-info', params={"car_name": model}).json()["resData"]
    header = model_info[0]
    values = model_info[1]
    result = {header[i]: values[i] for i in range(len(header))}

    with st.expander(f"🔎 {model} 상세 정보 보기"):
        st.image(result["IMG_URL"], caption=f"{model} 대표 이미지", use_container_width=True)
        for key, value in result.items():
            if key in ["CAR_CODE", "IMG_URL"]:
                continue

            display_key = korean_mapping.get(key, key)
            if key == "PRICE":
                try:
                    value = format(int(value), ",") + " 원"
                except Exception as e:
                    pass
            elif key == "MAX_DISTANCE":
                value = f"{value} km"
            elif key == "FUEL_EFFICIENCY":
                value = f"{value} km/h"
            
            st.write(f"**{display_key}:** {value}")

    headers = model_info[0]
    values = model_info[1]
    result_dict = {header.replace("_", ""): value for header, value in zip(headers, values)}
    
    sub_data = requests.post(url, params={"car_code": result_dict["CARCODE"], "sido": regions[region]}).json()["resData"]
    
    if sub_data:
        texts = [item["text"] for item in sub_data]
        selected_text = st.selectbox("**전기차 국고 지원금**", texts, key=f"sub_data_{key_prefix}", index=0)
    else:
        selected_text = None

    support = result["SUBSIDY"]
    return model_info, support, header

with col1:
    st.subheader("🚗 첫 번째 자동차 선택")
    selected_company1 = st.selectbox("**회사**", list(data.keys()), key="company1")
    selected_model1 = st.selectbox("**모델**", data[selected_company1], key="model1")
    selected_region1 = st.selectbox("**거주 지역**", list(regions.keys()), key="region1")
    
    if selected_model1 and selected_region1:
        model_info1, support1, header1 = display_car_info(selected_model1, selected_region1, key_prefix="left")

if compare:
    with col2:
        st.subheader("🚙 두 번째 자동차 선택")
        selected_company2 = st.selectbox("**비교 전기차 회사**", list(data.keys()), key="company2")
        selected_model2 = st.selectbox("**비교 전기차 모델**", data[selected_company2], key="model2")
        selected_region2 = st.selectbox("**거주 지역**", list(regions.keys()), key="region2")
        
        if selected_model2 and selected_region2:
            model_info2, support2, header2 = display_car_info(selected_model2, selected_region2, key_prefix="right")

st.markdown("""
---
### 💬 **추가 정보**
✅ 비교하고 싶은 모델을 선택해 주세요.  
⚡ 전기차 모델의 경우 연비 대신 전기차로 표시됩니다.  
💡 국고 지원금 정보는 선택한 지역에 따라 달라질 수 있습니다.  
🌐 언어 지원 기능 추가 예정입니다.
""")
