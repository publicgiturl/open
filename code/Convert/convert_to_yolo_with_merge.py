import cv2
from merge_data import *

# src = '/data/vehicle_exterior'
# label_dst = '/data/vehicle_exterior/labels'
# image_dst = '/data/vehicle_exterior/images'
# class_path = '/data/ai_dataSet/Model/ScaledYOLOv4/vehicle_exterior.names'

# j_train, j_val, j_test = split_train_val_test(src, image_dst, label_dst)

# 전체 json폴더 내에 있는 json파일 불러와서 convert
def converting(json_path, class_path):
    box_class = class_dict(class_path)
    for j_file in tqdm(glob(f'{json_path}/*.json'), desc=f'{json_path.split("/")[-1]}/convert_json'):
        img = cv2.imread(j_file.replace('jsons','images').replace('.json','.jpg'))

        with open(j_file, encoding='utf-8') as json_file:
            class_name = box_class[j_file.split('/')[-1][14:17]]
            json_data = json.load(json_file)
            width,height = img.shape[1], img.shape[0]

            img_name = j_file.replace('jsons','images').replace('.json','.jpg').split('/')[-1]
            # convert된 yolo_data_set저장 경로
            yolo_set = open(f"{j_file.replace('jsons', 'labels').replace('.json','.txt')}", 'w', encoding='utf-8')

            # annotations 값 추출
            # annotations = json_data['Learning data info.']['annotation']

            if 'bbox' in json_data['Learning data Info'].keys():
                bbox = json_data['Learning data Info']['bbox']
                x_min, y_min, x_max, y_max = bbox['tl']['x'], bbox['tl']['y'], bbox['br']['x'], bbox['br']['y']
            dw = 1. / width
            dh = 1. / height
            x = float(x_min + x_max) / 2
            y = float(y_min + y_max) / 2
            w = float(x_max - x_min)
            h = float(y_max - y_min)

            x = round(x * dw, 6)
            w = round(w * dw, 6)
            y = round(y * dh, 6)  # 6자리 표시
            h = round(h * dh, 6)

            file_path = f"{class_name} {x} {y} {w} {h}"

            # file_path = j_file.replace('.json', '.jpg').replace('\\','/')
            # file_path = ''

            # annotations된 객체들 반복

            # for ann in annotations:
            #     if ann['type'] == 'box':
            #     #  if 'box' in ann.keys():
            #         # yolo형식에 맞게 자료 변환
            #         if ann['coord'][0]+ann['coord'][2] >=1920 or ann['coord'][1]+ann['coord'][3]>=1080 or ann['coord'][0]<0 or ann['coord'][1]<0 or ann['coord'][2]<0 or ann['coord'][3]<0:
            #             continue
            #
            #         x = ann['coord'][0]
            #         y = ann['coord'][1]
            #         w = ann['coord'][2]
            #         h = ann['coord'][3]
            #
            #         dw = 1. / width
            #         dh = 1. / height
            #
                    # x = float(x+w+x)/2
                    # y = float(y+h+y)/2
                    # w = float(w)
                    # h = float(h)
                    #
                    # x = round(x * dw, 6)
                    # w = round(w * dw, 6)
                    # y = round(y * dh, 6)  # 6자리 표시
                    # h = round(h * dh, 6)
            #
            #         obj = (str(box_class[ann['class_id']]) + ' '
            #                   + str(x) + ' '
            #                   + str(y) + ' '
            #                   + str(w) + ' '
            #                   + str(h)
            #                 )

                    # path값 설정
                    # file_path += obj+'\n'

            yolo_set.write(file_path)
            yolo_set.close()
        with open(f"{json_path.split('jsons')[0]}/{json_path.split('/')[4]}.txt", 'a', encoding='utf-8') as f:
            f.write(json_path.replace('jsons','images').replace('.json','.jpg'))
"""
    최종실행 방법 : 해당파일 내에 convert_Warehouse2YOLO('json파일들이 들어있는 경로', 'yolo_set을 저장할 경로 및 파일명', '클래스들이 저장되어 있는 파일명(.txt, .name)')
                  명령어로 실행                  
"""

# converting(j_train, class_path)
# converting(j_val, class_path)
# converting(j_test, class_path)
converting('/disk1/yolo/val', '/disk1/yolo/val.txt', '/disk1/yolo/warehouse_bbox.txt')
# converting('/disk1/yolo/test', '/disk1/yolo/test.txt', '/disk1/yolo/warehouse_bbox.txt')
f =  open('/data/vehicle_exterior/train/train.txt', 'w')
for i in glob('/data/vehicle_exterior/train/images/*.jpg'):
    f.write(i+'\n')
f.close()
