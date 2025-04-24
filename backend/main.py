from fastapi import FastAPI,Query
import re
import subprocess
import json
from data_search import equal_serach,search_all,custom_equal_serach,like_serach
app = FastAPI()


@app.post("/api")
async def get_car_subsidy_info(car_code: str = Query(None), sido: str = Query(None)):
    url = f"https://auto.danawa.com/service/ajax_estimate_EVSigungu.php?trims={car_code}&sido={sido}&option="
    headers = "-H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'"
    curl_cmd = f"curl -k {headers} '{url}'"
    pattern = r"<option[^>]*\svalue=['\"](.*?)['\"][^>]*\sdata-price=['\"](.*?)['\"][^>]*\sdata-remaincount=['\"](.*?)['\"][^>]*>(.*?)</option>"
    result = subprocess.run(curl_cmd, shell=True, capture_output=True, text=True)

    matches = re.findall(pattern, result.stdout, re.DOTALL)

    result = []
    for value, data_price, data_remaincount, text in matches:
        result.append({
            "value": value,
            "data_price": data_price,
            "data_remaincount": data_remaincount,
            "text": text.strip()
        })
    return {"code":200,"resData":result}
@app.get("/api/car-info")
async def get_car_info(car_name: str = Query(None)):
    res_data = equal_serach('CAR','MODEL_NAME',car_name)
    return {"code":200,"resData":res_data}

@app.get("/api/chargeStatistics")
async def get_charge_Statistics():
    res_data = search_all('CHARGE_STATISTICS')
    return {"code":200,"resData":res_data}

@app.get('/api/region-info')
async def get_region_info():
    res_data = search_all('REGION')
    result = {}
    for row in res_data[1:]:
        # key는 1번 인덱스(지역명), value는 0번 인덱스(지역 코드)
        key = row[1]
        value = row[0]
        result[key] = value

    return {"code":200,"resData":result}

@app.get('/api/charge-search')
async def get_region_info(address: str = Query(None)):
    res_data = equal_serach('CHARGE','REGOIN_CODE',address)
    # for row in res_data[1:]:
    #     # key는 1번 인덱스(지역명), value는 0번 인덱스(지역 코드)
    #     key = row[1]
    #     value = row[0]
    #     result[key] = value

    return {"code":200,"resData":res_data}

@app.get('/api/region-info')
async def get_region_info():
    res_data = search_all('REGION')
    result = {}
    for row in res_data[1:]:
        # key는 1번 인덱스(지역명), value는 0번 인덱스(지역 코드)
        key = row[1]
        value = row[0]
        result[key] = value

    return {"code":200,"resData":result}

@app.get('/api/brand-info')
async def get_brand_info_all():
    hyeon_data = custom_equal_serach('CAR','MODEL_NAME,BRAND_NAME','BRAND_NAME','현대')
    hyeonkiakia_data = custom_equal_serach('CAR','MODEL_NAME,BRAND_NAME','BRAND_NAME','기아')
    tesla_data = custom_equal_serach('CAR','MODEL_NAME,BRAND_NAME','BRAND_NAME','테슬라')
    all_data = hyeon_data + hyeonkiakia_data + tesla_data
    data = {}
    for row in all_data:
    
        if row[0] == ['MODEL_NAME', 'BRAND_NAME'] :
            continue

        model, brand = row
        if model == 'MODEL_NAME':
            continue
        if brand not in data:
            data[brand] = []
        # 모델명을 리스트에 추가합니다.
        data[brand].append(model)
    return {"code":200,"resData":data}