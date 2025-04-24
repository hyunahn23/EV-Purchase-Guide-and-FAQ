from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
import re  # 숫자 추출을 위한 정규표현식 사용

# 1. chrome 실행
driver = webdriver.Chrome()

# 2. 특정 URL 접근
url = 'https://auto.danawa.com/compare/?Codes=87279@86421@87959@92087@86423'
driver.get(url)
time.sleep(3)  # 페이지 로딩 대기


# 3. 모델 이름 추출
model_elements = driver.find_elements(By.XPATH, '//*[contains(@id, "Photo_")]/div[1]/a/span')
model_names = [model.text for model in model_elements]


# 4. 공통 데이터 추출 함수 (가격, 연비, 주행거리 포함)
def extract_data(base_xpath, total_items, remove_extra=False, default_msg="정보 없음", process_subsidy=False, process_price=False, process_efficiency=False, process_distance=False):
    data_list = []
    for i in range(1, total_items + 1):
        try:
            if "Sumy3_" in base_xpath or "Sumy5_" in base_xpath or "Incnt_" in base_xpath:
                # 차종, 연료 전체 텍스트 추출
                main_element = driver.find_element(By.XPATH, f'{base_xpath}{i}"]/div[1]/div[1]' if "Incnt_" in base_xpath else f'{base_xpath}{i}"]')
                main_text = main_element.text

                # 국고 보조금 숫자만 추출 후 변환
                if process_subsidy:
                    if "정보 없음" in main_text:
                        main_text = "0"
                    else:
                        amount = re.findall(r'\d+', main_text)
                        main_text = str(int(amount[0]) * 10000) if amount else "0"

            else:
                # 가격, 연비, 주행거리 등 기본 정보 처리
                main_element = driver.find_element(By.XPATH, f'{base_xpath}{i}"]/span[1]')
                main_text = main_element.text

                # 가격 숫자만 추출 (int형 변환)
                if process_price:
                    amount = re.sub(r'[^\d]', '', main_text)  # 숫자만 추출
                    main_text = int(amount) if amount else 0

                # 연비 (Efficiency)에서 '(복합)' 및 '㎞/kWh' 제거 후 숫자 추출
                if process_efficiency:
                    cleaned_text = re.sub(r'[^\d.]', '', main_text)  # 숫자와 '.'만 추출
                    main_text = float(cleaned_text) if cleaned_text else 0.0

                # 주행거리 (Distance)에서 '㎞' 제거
                if process_distance:
                    cleaned_text = re.sub(r'[^\d]', '', main_text)  # 숫자만 추출
                    main_text = int(cleaned_text) if cleaned_text else 0

                if remove_extra:
                    try:
                        extra_element = driver.find_element(By.XPATH, f'{base_xpath}{i}"]/span[2]/span')
                        extra_text = extra_element.text
                        main_text = main_text.replace(extra_text, '').strip()
                    except:
                        pass

            data_list.append(main_text)
        except:
            # 숫자형 데이터는 0, 그 외는 기본 텍스트
            if process_price or process_distance or process_efficiency or process_subsidy:
                data_list.append(0)
            else:
                data_list.append(default_msg)
    return data_list


# 5. 각 정보 추출 (필요한 데이터 변환 적용)
model_prices = extract_data('//*[@id="Sumy1_', len(model_names), remove_extra=True, process_price=True)  # 가격 int 처리
model_types = extract_data('//*[@id="Sumy3_', len(model_names), default_msg="차종 정보 없음")
model_fuels = extract_data('//*[@id="Sumy5_', len(model_names), default_msg="연료 정보 없음")
model_efficiencies = extract_data('//*[@id="Sumy6_', len(model_names), remove_extra=True, process_efficiency=True)  # 연비 숫자만
model_distances = extract_data('//*[@id="Sumy7_', len(model_names), remove_extra=True, process_distance=True)  # 주행거리 숫자만
model_subsidies = extract_data('//*[@id="Incnt_', len(model_names), default_msg="0", process_subsidy=True)  # 국고 보조금 숫자만


# 6. 추출된 데이터 출력
for idx, (name, price, car_type, fuel, efficiency, distance, subsidy) in enumerate(
    zip(model_names, model_prices, model_types, model_fuels, model_efficiencies, model_distances, model_subsidies), start=1):
    print(f"모델 {idx}: {name} , 가격: {price} , 차종: {car_type} , 연료: {fuel} , 연비: {efficiency} , 주행거리: {distance} , 국고 보조금: {subsidy}")


# 7. DataFrame 생성 및 CSV 저장
df = pd.DataFrame({
    'Model Name': model_names,
    'Price (KRW)': model_prices,
    'Car Type': model_types,
    'Fuel': model_fuels,
    'Efficiency (km/kWh)': model_efficiencies,
    'Distance (km)': model_distances,
    'Government Subsidy (KRW)': model_subsidies
})
df.to_csv("tesla.csv", index=False, encoding='utf-8-sig')
print("'tesla.csv' 파일로 저장 완료되었습니다.")


# 8. 드라이버 종료
driver.quit()
