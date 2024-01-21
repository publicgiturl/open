import glob, os, csv, json
import pandas as pd
from openpyxl import Workbook
from openpyxl import load_workbook
import xml.etree.ElementTree as ET
from openpyxl import Workbook


main_path = 'Z:/키포인트/[163][키포인트]21.01.21 48.우마에서 근로자 떨어짐'
dir_path = main_path.replace(main_path.split('/')[-1], '')
os.chdir(main_path)

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)
 
createFolder(dir_path+'카운트')

for (path, dir, files) in os.walk(main_path):
        error_json = {}
        for file_name in files:
            if file_name.endswith('.json'):
                try:
                    with open(os.path.join(path, file_name), encoding='utf-8') as json_file:
                        error_json[os.path.join(path, file_name)] = ''
                        json_data = json.load(json_file)
                        annotation = json_data['annotations']
                        com_count = 0

                        if json_data['image']['copyrighter'] != '미디어그룹사람과숲(컨)':
                            error_json[os.path.join(path, file_name)] = error_json[os.path.join(path, file_name)] + 'Copyrighter 에러'
                            com_count += 1
                        if len(json_data['image']['date']) != 8:
                            if com_count != 0:
                                error_json[os.path.join(path, file_name)] = error_json[os.path.join(path, file_name)] + ', ' + 'date 에러'
                            else:
                                error_json[os.path.join(path, file_name)] = error_json[os.path.join(path, file_name)] + 'date 에러'
                                com_count += 1
                        if json_data['image']['path'] == 'NULL':
                            if com_count != 0:
                                error_json[os.path.join(path, file_name)] = error_json[os.path.join(path, file_name)] + ', ' + 'path 에러'
                            else:
                                error_json[os.path.join(path, file_name)] = error_json[os.path.join(path, file_name)] + 'path 에러'
                                com_count += 1
                        if json_data['image']['filename'][0] != 'S' or json_data['image']['filename'][3] != 'O' and json_data['image']['filename'][3] != 'N':
                            if com_count != 0:
                                error_json[os.path.join(path, file_name)] = error_json[os.path.join(path, file_name)] + ', ' + 'filename 에러'
                            else:
                                error_json[os.path.join(path, file_name)] = error_json[os.path.join(path, file_name)] + 'filename 에러'
                                com_count += 1
                        if len(annotation) == 0:
                            if com_count != 0:
                                error_json[os.path.join(path, file_name)] = error_json[os.path.join(path, file_name)] + ', ' + 'annotation 누락'
                            else:
                                error_json[os.path.join(path, file_name)] = error_json[os.path.join(path, file_name)] + 'annotation 누락'
                                com_count += 1
                        else:
                            for i in range(len(annotation)):
                                if 'data ID' not in annotation[i] or 'middle classification' not in annotation[i] or 'flags' not in annotation[i] or 'class' not in annotation[i]:
                                    if com_count != 0:
                                        error_json[os.path.join(path, file_name)] = error_json[os.path.join(path, file_name)] + ', ' + 'annotation 에러'
                                        break
                                    else:
                                        error_json[os.path.join(path, file_name)] = error_json[os.path.join(path, file_name)] + 'annotation 에러'
                                        com_count += 1
                                        break
                                else:
                                    if len(annotation[i]['data ID']) != 2:
                                        if com_count != 0:
                                            error_json[os.path.join(path, file_name)] = error_json[os.path.join(path, file_name)] + ', ' + 'annotation 에러'
                                            break
                                        else:
                                            error_json[os.path.join(path, file_name)] = error_json[os.path.join(path, file_name)] + 'annotation 에러'
                                            com_count += 1
                                            break
                                    if 'box' in annotation[i]:
                                        if len(annotation[i]['box']) != 4:
                                            if com_count != 0:
                                                error_json[os.path.join(path, file_name)] = error_json[os.path.join(path, file_name)] + ', ' + 'annotation 에러'
                                                break
                                            else:
                                                error_json[os.path.join(path, file_name)] = error_json[os.path.join(path, file_name)] + 'annotation 에러'
                                                com_count += 1
                                                break
                                    elif 'polygon' in annotation[i]:
                                        pass
                                    elif 'keypoints' in annotation[i]:
                                        pass
                                    else:
                                        if com_count != 0:
                                            error_json[os.path.join(path, file_name)] = error_json[os.path.join(path, file_name)] + ', ' + 'annotation 에러'
                                            break
                                        else:
                                            error_json[os.path.join(path, file_name)] = error_json[os.path.join(path, file_name)] + 'annotation 에러'
                                            com_count += 1
                                            break

                                    if annotation[i]['flags'] != {}:
                                        if len(annotation[i]['flags'].split(',')) < 2:
                                            if com_count != 0:
                                                error_json[os.path.join(path, file_name)] = error_json[os.path.join(path, file_name)] + ', ' + 'annotation 에러'
                                                break
                                            else:
                                                error_json[os.path.join(path, file_name)] = error_json[os.path.join(path, file_name)] + 'annotation 에러'
                                                com_count += 1
                                                break
                                    else:
                                        if com_count != 0:
                                            error_json[os.path.join(path, file_name)] = error_json[os.path.join(path, file_name)] + ', ' + 'annotation 에러'
                                            break
                                        else:
                                            error_json[os.path.join(path, file_name)] = error_json[os.path.join(path, file_name)] + 'annotation 에러'
                                            com_count += 1
                                            break
                except:
                    error_json[os.path.join(path, file_name)] = 'json 형식 에러'
                finally:
                    json_file.close()

        try:
            e = open(os.path.join(path, 'annotation_error.csv'), mode='wt', encoding='utf-8-sig')
            for key, value in error_json.items():
                if value != '':
                    e.write(str(key) + ' : ' + str(value) + '\n')
        finally:
            e.close()


remove_list = []

# annotation누락 찾기
with open(main_path+'/annotation_error.csv', 'r', encoding='utf-8') as f:
    Ann_list = [i for i in f]

for ann in Ann_list:
    if ' annotation 누락' in ann:
        remove_list.append(ann.split('\\')[-1].split(' :')[0])

for i in remove_list:
    os.remove('./'+i)

write_xl = Workbook()
write_ws = write_xl.active
write_ws.append(['폴더명', 'JSON', 'class', 'class_count', 'box', 'polygon', 'point'])
for (path, dir, files) in os.walk(main_path):
    firstRow = True
    for fileName in files:
        if fileName.endswith('.json'):
            firstJson = True
            with open(os.path.join(path, fileName), encoding='utf-8') as json_file:
                try:
                    jsonData = json.load(json_file)
                    annotations = jsonData['annotations']
                    classType = []
                    classTypeList = ['box', 'polygon', 'point']
                    classCountDict = {}
                    classTypeCountDict = {}

                    for i in range(len(annotations)):
                        classType.append(annotations[i]['class'])

                    for key in classType:
                        classCountDict[key] = classType.count(key)
                        classTypeCountDict[key] = {'box': 0, 'polygon': 0, 'point': 0}

                    for key in classCountDict:
                        for i in range(len(annotations)):
                            if annotations[i]['class'] == key:
                                for item in classTypeList:
                                    if item in annotations[i]:
                                        classTypeCountDict[key][item] += 1

                    for key in classCountDict:
                        if firstRow and firstJson:
                            write_ws.append([path, fileName, key, classCountDict[key],
                                                classTypeCountDict[key][classTypeList[0]],
                                                classTypeCountDict[key][classTypeList[1]],
                                                classTypeCountDict[key][classTypeList[2]]])
                            firstRow = False
                            firstJson = False
                        elif firstJson:
                            write_ws.append(["", fileName, key, classCountDict[key],
                                                classTypeCountDict[key][classTypeList[0]],
                                                classTypeCountDict[key][classTypeList[1]],
                                                classTypeCountDict[key][classTypeList[2]]])
                            firstJson = False
                        else:
                            write_ws.append(["", "", key, classCountDict[key],
                                                classTypeCountDict[key][classTypeList[0]],
                                                classTypeCountDict[key][classTypeList[1]],
                                                classTypeCountDict[key][classTypeList[2]]])
                except Exception as ex:
                    print(ex)
                    pass

write_xl.save(os.path.join(main_path, '../카운트/{}.xlsx'.format(main_path.split('/')[-1])))


jpg  = []
json = []
NG = []
no_jpg = []
# json파일 이름명 추출
### 주소만 변경 ###

# os.chdir(main_path)
for file in glob.glob("*.json"):
    json.append(file.split('.')[0])

# jpg파일 이름명 추출    
for file in glob.glob("*.jpg"):
    jpg.append(file.split('.')[0])

# Json은 있지만 이미지가 없는 파일 걸러내기
for v in jpg:
    if v not in json:
        NG.append(v+'.jpg')

# 이미지가 없는데 Json이 있는 파일 걸러내기
for v in json:
    if v not in jpg:
        no_jpg.append(v+'.json')

# # 매치 되지않은 jpg리스트 저장
with open('./omission_jpg.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(NG)

# 매치 되지않은 json리스트 저장
with open('./omission_json.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(no_jpg)

# 매치되지 않은 jpg 삭제
for i in NG:
    os.remove(i)

# 매치되지 않은 json 삭제
for i in no_jpg:
    os.remove(i)
print(main_path + '완료')