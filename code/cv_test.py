import cv2
import numpy as np
import json

# img = cv2.imread('E:/2021/TS/000011_front.png')
#
# with open('E:/2021/TS/COCO/3) 21.10.09/034_일출-일몰_흐림_지방도로_210902_01_/label/instances_default.json', encoding='utf-8') as f:
#     json_data = json.load(f)
#     obj_list =[]
#     obj_dict = {}
#     for i in json_data['annotations']:
#
#         if i['image_id']==471:
#             obj_dict[i['id']] = i['segmentation']
# for key,val in obj_dict.items():
#     # print(key)
#     print('val :',val)
#     aa=np.array(val,np.int32).flatten()
#     # print(aa)
#     x = aa.shape
#     bb = aa.reshape(x[0]//2,2)
#     print(bb[:,0])
#     print(bb[:,1])
#     cv2.polylines(img, [bb], True, (255, key+10, 0), 2)
#
# cv2.imshow('test',img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# from glob import glob
# from tqdm import tqdm
#
# for txt_file in tqdm(glob('G:/test/*.txt')):
#     with open(txt_file) as f:
#         img = cv2.imread(txt_file.replace('.txt', '.jpg'))
#         h, w = img.shape[:-1]
#
#         for i in f:
#             # print(i.split('\n')[0])
#             coord = i.split('\n')[0].split()
#
#             xmax = int(w * float(coord[1]))
#             xmin = int(w * float(coord[3]))
#             ymax = int(h * float(coord[2]))
#             ymin = int(h * float(coord[4]))
#
#             xmax = int(xmax-xmin/2)
#             ymax = int(ymax-ymin/2)
#
#             # print(xmax, ymax, xmin, ymin)
#             cv2.rectangle(img, (xmax,ymax), (xmin+xmax,ymin+ymax), (255,0,0),2)

        # cv2.imwrite(txt_file.replace('.txt','.jpg'), img)
