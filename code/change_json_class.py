# -*- coding: UTF-8 -*-
import os
import json
from parser import expr

try:
    configFile = r"./config.json"
    with open(configFile, 'rt', encoding='utf-8') as f:
        config = json.load(f)
finally:
    f.close()

beforePath = config['BEFORE_JSON_PATH']
afterPath = config['AFTER_JSON_PATH']

#  폴더 생성
if not (os.path.isdir(afterPath + "/A")):
    os.makedirs(afterPath + "/A")
if not (os.path.isdir(afterPath + "/B")):
    os.makedirs(afterPath + "/B")
if not (os.path.isdir(afterPath + "/C")):
    os.makedirs(afterPath + "/C")
if not (os.path.isdir(afterPath + "/D")):
    os.makedirs(afterPath + "/D")

#  리스트 생성
class_a = []
class_b = []
class_c = []
class_d = []

for (path, dir, files) in os.walk(beforePath):  # for (path,dir,files) in os.walk(beforepath) beforepath에 있는 디렉토리 탐색
    for fileName in files:  # 디렉토리 탐색 중 파일을 검색
        if fileName.endswith('.json'):  # .json 확장자를 탐색
            try:
                with open(os.path.join(path, fileName),encoding='utf-8') as json_file:  # 파일 열기
                    jsonData = json.load(json_file)  # 디스크에 있는 포맷 데이터를 파이썬으로 읽어 오기
                    jsonimge = jsonData["image"]  # json이미지 key추출

                    for jsonanno in jsonData["annotations"]:
                        if jsonanno["middle classification"] == "01":
                            class_a.append(jsonanno)
                        if jsonanno["middle classification"] == "02":
                            class_b.append(jsonanno)
                        if jsonanno["middle classification"] == "03":
                            class_c.append(jsonanno)
                        if jsonanno["middle classification"] == "04":
                            class_c.append(jsonanno)
                        if jsonanno["middle classification"] == "05":
                            class_c.append(jsonanno)
                        if jsonanno["middle classification"] == "06":
                            class_c.append(jsonanno)
                        if jsonanno["middle classification"] == "07":
                            class_d.append(jsonanno)

                    # 딕셔너리 생성
                    class_adic = {"image": jsonimge, "annotations": class_a}
                    class_bdic = {"image": jsonimge, "annotations": class_b}
                    class_cdic = {"image": jsonimge, "annotations": class_c}
                    class_ddic = {"image": jsonimge, "annotations": class_d}

                    # 값이 존재할 경우 json데이터 저장
                    if class_adic["annotations"]:
                        with open(os.path.join(afterPath + "/A", fileName), 'w', encoding='utf-8') as json_change:
                            json.dump(class_adic, json_change, indent=4)
                    if class_bdic["annotations"]:
                        with open(os.path.join(afterPath + "/B", fileName), 'w', encoding='utf-8') as json_change:
                            json.dump(class_bdic, json_change, indent=4)
                    if class_cdic["annotations"]:
                        with open(os.path.join(afterPath + "/C", fileName), 'w', encoding='utf-8') as json_change:
                            json.dump(class_cdic, json_change, indent=4)
                    if class_ddic["annotations"]:
                        with open(os.path.join(afterPath + "/D", fileName), 'w', encoding='utf-8') as json_change:
                            json.dump(class_ddic, json_change, indent=4)

                    #  리스트 초기화
                    class_a.clear()
                    class_b.clear()
                    class_c.clear()
                    class_d.clear()

            finally:
                json_file.close()
