# import numpy as np
# import cv2
#
# hdr_path = "D:/test.hdr"
# raw_path = "D:/test.raw"
# # # hdr 파일을 읽어옴
# # img = cv2.imread(, cv2.IMREAD_ANYDEPTH | cv2.IMREAD_COLOR)
# hdr = cv2.imread(hdr_path, cv2.IMREAD_ANYDEPTH | cv2.IMREAD_COLOR)
#
# print(hdr)
# # # RGB 색상 공간에서 linear한 데이터를 gamma 보정을 적용하여 sRGB 색상 공간으로 변환
# # img_srgb = cv2.cvtColor(hdr, cv2.COLOR_RGB2BGR)
# # img_srgb = cv2.cvtColor(img_srgb, cv2.COLOR_BGR2RGB)
# # img_srgb = cv2.pow(img_srgb, 1.0 / 2.2)
# # img_srgb = cv2.normalize(img_srgb, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8UC3)
# #
# # # 이미지 출력
# # cv2.imshow('image', img_srgb)
# # cv2.waitKey(0)
# # cv2.destroyAllWindows()
#
#
# # raw 파일 읽어오기
# with open(raw_path, "rb") as f:
#     raw_data = np.frombuffer(f.read(), np.uint16)
#     # raw_data = np.reshape(raw_data, (hdr.shape[0], hdr.shape[1]))
# print(raw_data)
# import matplotlib.pyplot as plt
# from PIL import Image
# import cv2
#
# # img = cv2.imread('D:/REFLECTANCE_jeju_2023-05-07_005.tif', cv2.IMREAD_UNCHANGED)
# # print(img)
# # cv2.imshow('image', img)
# # cv2.waitKey(0)
# # cv2.destroyAllWindows()
# raw_file = open('D:/test.raw','rb')
# data = raw_file.read()
#
# img = Image.frombytes('L', (1920,1080),data)
# print(img)
# plt.imshow(img, cmap='Accent')
# plt.show()
# # print(data)
# raw_file.close()
import numpy as np

import cv2
import json
from PIL import ImageFont, ImageDraw, Image
from glob import glob

def getbbox(points):
    polygons = np.array(points)
    x,y = polygons[:,0], polygons[:,1]
    bbox = [round(x.min(),2),round(y.min(),2), round(x.max()-x.min(),2),round(y.max()-y.min(),2)]
    area = 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))
    return bbox, area

def get_seg(points):
    x = []
    y = []
    for seg_idx, seg in enumerate(points):
        if seg_idx % 2 == 0:
            x.append(seg)
        else:
            y.append(seg)
    seg = np.array([(x, y) for x, y in zip(x, y)], np.int)
    return seg

# 랜덤한 색상 생성 함수
def generate_random_color():
    r = np.random.randint(0, 255)
    g = np.random.randint(0, 255)
    b = np.random.randint(0, 255)
    return (r, g, b)

# 각 객체에 랜덤한 색상 부여
object_colors = [generate_random_color() for _ in range(17)]

font = ImageFont.truetype("C:/Windows/Fonts/H2GTRM.TTF", 20)

cls_dict = {idx:rgb for idx, rgb in enumerate(object_colors)}

for j_file in glob('D:/aaa/*.json'):
    img_file = j_file.replace('.json','.png')
    img = cv2.imread(img_file)

    with open(j_file, encoding='utf-8') as json_file:
        json_data = json.load(json_file)
        cls_list = list(set([cls['class'] for cls in json_data['annotations']]))

        for ann in json_data['annotations']:
            if ann['label_type']=='bbox':
                x,y,w,h = [int(coord) for coord in ann['coordinates']]
                cv2.rectangle(img,(x,y),(x+w,y+h), cls_dict[cls_list.index(ann['class'])], 2)
                text_size = cv2.getTextSize(ann['class'], cv2.FONT_HERSHEY_SIMPLEX, 2, 1)[0]
                label_x = x
                label_y = y + text_size[1]

            elif ann['label_type']=='segmentation':
                seg = get_seg(ann['coordinates'])
                box, area = getbbox(seg)

                top_point = min(seg, key=lambda p: p[1])
                cv2.polylines(img, [seg], True, cls_dict[cls_list.index(ann['class'])], 2)
                text_size = cv2.getTextSize(ann['class'], cv2.FONT_HERSHEY_SIMPLEX, 1, 1)[0]

                label_x = top_point[0]
                label_y = top_point[1] + text_size[1]


            pil_img = Image.fromarray(img)
            draw = ImageDraw.Draw(pil_img)
            draw.text((label_x, label_y), ann['class'], cls_dict[cls_list.index(ann['class'])], font)
            img=np.array(pil_img)



    # cv2.imshow('img',img)
    # cv2.waitKey(0)
    file_name =img_file.split("\\")[-1]
    cv2.imwrite(f'D:/aaa_1/{file_name}', img)
# cv2.destroyAllWindows()
    # break