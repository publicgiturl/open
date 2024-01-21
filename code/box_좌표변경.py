import os
import shutil
import json

main_path = 'E:/fire/fire_df'
# main_path = 'E:/test/20210528_S3-'
before_path = main_path
after_path = main_path

def start():
    global count_box, count_polygon, count_fix, count_nfix
    try:
        with open(os.path.join(path, file_name),encoding='utf-8-sig') as json_file:
            json_data = json.load(json_file)
            annotation = json_data['annotations']

            if(len(annotation)!=2):
                print(file_name + ' count')
                count_box = count_box + 1
                return
            for i in range(len(annotation)):
                if 'polygon' in annotation[i]:
                    count_polygon = count_polygon+1
                    print(file_name + ' polygon')
                    return

            point_L = list()
            point_R = list()
            point_D = list()
            point_U = list()
            for i in range(len(annotation)):
                if(annotation[i]['box'][1]>annotation[i]['box'][3]): # Y좌표넣기
                    point_U.append(-annotation[i]['box'][3])
                    point_D.append(-annotation[i]['box'][1])
                else:
                    point_U.append(-annotation[i]['box'][1])
                    point_D.append(-annotation[i]['box'][3])
                if(annotation[i]['box'][0]<annotation[i]['box'][2]): # X좌표넣기
                    point_L.append(annotation[i]['box'][0])
                    point_R.append(annotation[i]['box'][2])
                else:
                    point_L.append(annotation[i]['box'][2])
                    point_R.append(annotation[i]['box'][0])


            mode = 0
            if(annotation[1]['class']=='04'): # 0번 04(불꽃)(A), 1번 01/02/03(연기)(B)
                mode = 1
                temp = point_U[0]
                point_U[0] = point_U[1]
                point_U[1] = temp

                temp = point_D[0]
                point_D[0] = point_D[1]
                point_D[1] = temp

                temp = point_L[0]
                point_L[0] = point_L[1]
                point_L[1] = temp

                temp = point_R[0]
                point_R[0] = point_R[1]
                point_R[1] = temp

            if(point_U[0]>point_D[1]): # A의 위쪽이 B의 아래쪽보다 위쪽
                if(point_R[1] < point_L[0] or point_L[1] > point_R[0]):
                    count_nfix = count_nfix +1
                    print(file_name + " 정상")
                else:
                    count_fix = count_fix + 1
                    print(file_name + " 좌표변경")
                    point_D[1] = point_U[0] # 좌표맞추기
            else:
                count_nfix = count_nfix +1
                print(file_name + " 정상")

            if(mode == 0):
                annotation[0]['box'][1] = -point_U[0]
                annotation[0]['box'][3] = -point_D[0]
                annotation[1]['box'][1] = -point_U[1]
                annotation[1]['box'][3] = -point_D[1]
            else:
                annotation[1]['box'][1] = -point_U[0]
                annotation[1]['box'][3] = -point_D[0]
                annotation[0]['box'][1] = -point_U[1]
                annotation[0]['box'][3] = -point_D[1]


        with open(os.path.join(after_path, file_name), 'w', encoding='utf-8') as json_change:
            json.dump(json_data, json_change, indent=2, ensure_ascii=False)

    finally:
        json_file.close()

count_box = 0
count_polygon = 0
count_fix = 0
count_nfix = 0

for (path, dir, files) in os.walk(before_path):
        for file_name in files:
            if file_name.endswith('.json'):
                start()


print("count_except :",end=' ');print(count_box)
print("polygon_except :",end=' ');print(count_polygon)
print("nfix :",end=' ');print(count_nfix)
print("fix :",end=' ');print(count_fix)
print("sum :",end=' ');print(count_fix+count_nfix+count_box+count_polygon)