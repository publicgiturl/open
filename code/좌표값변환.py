import json

import numpy as np
import cv2

# def project_3d_to_2d(intrinsic_matrix, extrinsic_matrix, point_3d):
#     # Intrinsic Matrix
#     intrinsic_matrix = np.array(intrinsic_matrix).reshape(4, 4)
#
#     # Extrinsic Matrix
#     extrinsic_matrix = np.array(extrinsic_matrix).reshape(4, 4)
#
#     # 3D point (x, y, z, 1)
#     point_3d = np.array([point_3d['x'], point_3d['y'], point_3d['z'], 1])
#
#     # 3D to 2D projection
#     projection_matrix = np.dot(intrinsic_matrix, extrinsic_matrix)
#     point_2d = np.dot(projection_matrix, point_3d)
#
#     # Normalize 2D coordinates
#     x_2d = point_2d[0] / point_2d[2]
#     y_2d = point_2d[1] / point_2d[2]
#
#     # Scale to image size (640x480)
#     width, height = 640, 480
#     x_scaled = int((x_2d + 1) * width / 2)
#     y_scaled = int((1 - y_2d) * height / 2)
#
#     return x_scaled, y_scaled
#
# def extract_object_info(label_info):
#     object_info = {
#         "name": label_info[0],
#         "x": float(label_info[3]),
#         "y": float(label_info[4]),
#         "z": float(label_info[5]),
#         "width": float(label_info[6]) - float(label_info[3]),
#         "height": float(label_info[8]) - float(label_info[7])
#     }
#     return object_info
#
# def convert_to_2d_bbox(data):
#     x_min, y_min, x_max, y_max = data['x'], data['y'], data['x'] + data['width'], data['y'] + data['height']
#     return {
#         "name": data['name'],
#         "x": x_min,
#         "y": y_min,
#         "width": x_max - x_min,
#         "height": y_max - y_min
#     }
#

with open('/data2/자율주행/train/test5_10segs_weather_0_spawn_1_roadTexture_1_P_None_C_None_B_None_WC_None/19-10-2018_12-47-37/Information/000101.json') as json_file:
    json_data = json.load(json_file)

    intrinsic = json_data['intrinsic']['matrix']
    extrinsic = json_data['extrinsic']['matrix']
#     coord_list = []
#     # for coord in json_data['bounds']:
#     #     coord_list.append(coord['Center'])
#
# def check_minus(x):
#     if x <0:
#         return 0
#     else:
#         return int(x)
#
from tqdm import tqdm
from glob import glob

for sample_file in tqdm(glob('/data2/자율주행/test/test5_14segs_weather_0_spawn_0_roadTexture_1_P_None_C_None_B_None_WC_None/24-10-2018_20-16-55/labels_kitti/*.txt')):
    with open(sample_file) as txt_file:
        img_file = sample_file.replace('labels_kitti','RGB').replace('.txt','.png')
        img = cv2.imread(img_file)
        for ann in txt_file:
            parts = ann.strip().split(' ')
            label = parts[0]
            x_min, y_min, x_max, y_max = [int(coord) for coord in map(float, parts[4:8])]
            cv2.rectangle(img, (x_min,y_min), (x_max, y_max), (255,0,0), 2)
#         # x_2d, y_2d = project_3d_to_2d(intrinsic, extrinsic, [float(coord) for coord in ann.split()[1:]])
#         # print(x_2d, y_2d)
#         label_info = extract_object_info(ann.split())
#         # x_2d, y_2d = project_3d_to_2d(intrinsic, extrinsic, label_info)
#         aa = convert_to_2d_bbox(label_info)
#         x1, y1, x2, y2 = check_minus(aa['x']), check_minus(aa['y']), check_minus(aa['x']+aa['width']), check_minus(aa['y']+aa['height'])
#         print(x1,y1,x2,y2)
#         cv2.rectangle(img, (x1,y2), (x2,y1), (255,0,0), 2)
# #
# cv2.imwrite('/data/test.png', img)
    cv2.imshow('img',img)
    cv2.waitKey(0)
#
#
# # # 3D 좌표를 2D 이미지 좌표로 변환
# # x_2d, y_2d = project_3d_to_2d(intrinsic, extrinsic, point_3d)
# #
# # for ann in coord_list:
# #     x, y = project_3d_to_2d(intrinsic, extrinsic, ann)
# # print("2D 이미지 좌표 (x, y):", x_2d, y_2d)

