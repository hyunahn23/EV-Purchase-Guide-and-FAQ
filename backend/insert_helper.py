from data_insert_module import db_insert_module,db_insert_ignore_module,db_replace_module
import os
import ast
import json

def ev_data_insert():
    data_list = []
    seen_charge_names = set()  # 중복 확인을 위한 집합(Set)

    with open('temp.txt', 'r', encoding='utf-8') as file:
        for line in file:
            # 줄 끝의 쉼표와 개행 문자 제거 후 공백 제거
            line = line.rstrip(',\n').strip()
            if line:
                try:
                    # 문자열을 안전하게 튜플로 변환
                    tup = ast.literal_eval(line)
                    # 튜플을 리스트로 변환 (수정 가능하게)
                    tup_list = list(tup)
                    
                    # 충전소 이름(인덱스 5) 중복 검사
                    charge_name = tup_list[5]
                    if charge_name in seen_charge_names:
                        continue  # 중복이면 추가하지 않음
                    
                    seen_charge_names.add(charge_name)  # 새로운 충전소 이름 저장
                    
                    # 세 번째 인덱스의 문자열을 JSON 형식으로 변환
                    raw_str = tup_list[2]
                    items = raw_str.split(',')
                    json_dict = {}
                    for item in items:
                        if ':' in item:
                            key, value = item.split(':', 1)
                            key = key.strip()
                            value = value.strip()
                            json_dict[key] = value
                    
                    # dict를 JSON 문자열로 변환 (ensure_ascii=False 로 한글 유지)
                    json_str = json.dumps(json_dict, ensure_ascii=False)
                    tup_list[2] = json_str

                    # 다시 튜플로 변환하여 리스트에 저장
                    data_list.append(tuple(tup_list))
                except Exception as e:
                    print(f"Error parsing line: {line}\n{e}")
        return data_list


test_data = ev_data_insert()


# db_replace_module('CHARGE',test_data)

