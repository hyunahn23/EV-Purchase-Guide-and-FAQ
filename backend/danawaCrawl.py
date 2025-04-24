from selenium import webdriver
from selenium.webdriver.common.by import By
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from data_insert_module import db_insert_module




driver = webdriver.Chrome()

url = 'https://auto.danawa.com/compare/?Codes='

driver.get(url)
wait = WebDriverWait(driver,10)
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div.buttonAddComp")))

btnContainer = driver.find_element(By.CSS_SELECTOR,"div.buttonAddComp")

brand_list = {}


add_btn = btnContainer.find_element(By.CSS_SELECTOR,".button")
add_btn.click()
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,".brand__group")))    
brand_container = driver.find_elements(By.CSS_SELECTOR,".brand__group")


for brand in brand_container:
    brand_name_ct = brand.find_elements(By.CSS_SELECTOR,".brand__item")
    brand_list = brand_list | {
        b.text.strip(): {
            "brand_code": b.get_attribute("data-brand"),
            "items":[]
        }
        for b in brand_name_ct if b.text.strip()
    }

place =1

for brand in brand_list:
    # brand 값을 설정합니다.
    if brand =='현대' or brand=='기아' or brand=='테슬라':
        define_script = f'window.brand = {brand_list[brand]["brand_code"]};'
        driver.execute_script(define_script)
        
        
        fetch_script = f"""
        var callback = arguments[arguments.length - 1];
        fetch("https://auto.danawa.com/service/navigatorNewcar.php?Work=model&Type=compare&refer=compare&Brand={brand_list[brand]["brand_code"]}&box=1")
            .then(response => response.text())
            .then(text => callback(text))
            .catch(error => callback("Error: " + error));
        """
        # 비동기 스크립트를 사용해서 fetch의 반환값을 콜백으로 받아옴.
        result = driver.execute_async_script(fetch_script)
        pattern = re.compile(r"<a\s+href=\"[^\"]*getCompData\(\d+,\s*'([^']+)'\)[^\"]*\".*?<span\s+class=['\"]name['\"]>(.*?)</span>",re.DOTALL)


        matches = pattern.findall(result)
        item = [{"name": name.strip(), "car_sub_code": car_sub_code.strip()} for car_sub_code, name in matches]
        brand_list[brand]["items"] = item
        
        # 이후 openAutoTab을 통해 선택된 brand로 이동
        driver.execute_script("openAutoTab('model');")
        # 이전탭으로 이동
        driver.execute_script("openAutoTab('brand');")
driver.execute_script("javascript:$('#autodanawa_popup .close').click();")
data_index = 1
def extract_data(tr_id, td_id, attOption=None, default_msg=None, clsOption=None,imgOption=False):
    unit_element = driver.find_element(By.ID, tr_id)
    td_element = unit_element.find_element(By.ID, td_id)
    
    # attOption이 지정된 경우 해당 속성 값 반환
    if attOption:
        return td_element.get_attribute(attOption)
    if imgOption:
        return td_element.find_element(By.TAG_NAME,'img').get_attribute('src')
    # price_class가 지정되어 있다면 해당 클래스의 자식 요소를 찾음
    if clsOption:
        try:
            price_element = td_element.find_element(By.CSS_SELECTOR, clsOption)
            data = price_element.text
        except Exception:
            data = td_element.text
    else:
        data = td_element.text

    # 텍스트가 없으면 기본 메시지 반환
    if not data:
        return default_msg

    return data

def extract_numeric(text):
    # re.sub()를 사용하여 숫자(0-9)와 점(.)을 제외한 모든 문자를 빈 문자열로 치환합니다.
    if text is None:
        return ""
    cleaned = re.sub(r'[^0-9.]', '', text)
    return cleaned.strip()

def extract_sub(data):
    if data is None:
        return '0'
    pattern = re.compile(r"국고\s*보조금\s*([\d]+만)")
    match = pattern.search(data)
    
    if match:
        result = match.group(1)
        return result
    else:
        return '0'

new_list = []
for brand in brand_list:
    if brand =='현대' or brand=='기아' or brand=='테슬라':
        for item in brand_list[brand]["items"]:
            script = f'getCompData({data_index},"{item["car_sub_code"]}")'
            driver.execute_script(script)
            model_fuels = extract_data('unitSumy5',f'Sumy5_{data_index}', default_msg="연료 정보 없음")
            
            if ('배터리' in model_fuels or '전기' in model_fuels) and ('가솔린' not in model_fuels or '경유' not in model_fuels) :
                price = extract_data('unitSumy1',f'Sumy1_{data_index}',clsOption='.vals')
                car_code = extract_data('unitPhoto',f'Photo_{data_index}','code')
                subsidies = extract_data('unitIncnt',f'Incnt_{data_index}')
                fuels = extract_data('unitSumy5',f'Sumy5_{data_index}')
                efficiencies = extract_data('unitSumy6',f'Sumy6_{data_index}')
                distances = extract_data('unitSumy7',f'Sumy7_{data_index}')
                types = extract_data('unitSumy3',f'Sumy3_{data_index}')
                unit_element = driver.find_element(By.ID, 'unitPhoto')
                td_element = unit_element.find_element(By.ID, f'Photo_{data_index}')
                photo_element = td_element.find_element(By.CLASS_NAME,"photo")
                img_element = photo_element.find_element(By.TAG_NAME,'img')
                car_img_url = img_element.get_attribute('src')
                new_list.append(
                    {
                        "brand":brand,
                        "model_name":item["name"],
                        "car_code":car_code[-5:],
                        "price":int(price.replace(",","").replace(",", "")),
                        "subsidy": int(extract_sub(subsidies).replace('만','0000')),
                        "efficiencies": float(extract_numeric(efficiencies)) if extract_numeric(efficiencies) else 0.0,
                        "distances":int(extract_numeric(distances)) if extract_numeric(distances) else 0,
                        "types":types,
                        "fuels":fuels,
                        "img_url":car_img_url
                    })
            if data_index==5:
                data_index=1
                continue
            data_index+=1


replace_list = []
for item in new_list:
    insertData = (item["car_code"],item["model_name"],item["price"],item["types"],item["efficiencies"],item["fuels"],item["distances"],item["subsidy"],item["brand"],item["img_url"])
    replace_list.append(insertData)

db_insert_module("CAR",replace_list)
print('CAR COMPLETE')
    



