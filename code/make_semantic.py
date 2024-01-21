# # import json
# # from glob import glob
# # from tqdm import tqdm
# # import numpy as np
# # import pymysql
# # import pandas as pd
# #
# #
# #
# # # Connect DB
# # conn = pymysql.connect(host = '192.168.100.53', user = 'haer', password = 'haer', db='onss_ai')
# # curs = conn.cursor()
# #
# # sql = "INSERT ignore INTO ai_image_tbl(IMG_NAME,IMG_PATH,IMG_WIDTH,IMG_HEIGHT,LOCATION) VALUES (%s,%s,%s,%s,%s);"
# # # sql2 = "INSERT INTO ai_annotation_tbl(IMG_NAME,OBJ_IDX,CLASS_CODE,ANNO_TYPE,BOX_X_MIN,BOX_Y_MIN,BOX_X_MAX,BOX_Y_MAX,POLY_XCNTS,POLY_YCNTS) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
# #
# # print("img tbl insert start")
# # img_dummy = []
# #
# # # dummy_list = pd.DataFrame(columns=['IMG_NAME','OBJ_IDX','CLASS_CODE','ANNO_TYPE','BOX_X_MIN','BOX_Y_MIN','BOX_X_MAX','BOX_Y_MAX','POLY_XCNTS','POLY_YCNTS'])
# # txt_list = []
# # with open('F:/2022/img_list.txt') as txt_file:
# #     for i in txt_file:
# #         j_name = i.split('\n')[0]
# #         txt_list.append(f"H:/Data/04_Industrial_safety/fire/label/{j_name}")
# #
# # for idx, j_file in enumerate(tqdm(txt_list)):
# #     with open(j_file, encoding='utf-8-sig') as json_file:
# #         json_data = json.load(json_file)
# #
# #         img_name = json_data["image"]["filename"]
# #         img_path = '04_Industrial_safety/fire/image'
# #
# #         if json_data["image"]["filename"] != j_file.split('/')[-1].replace('.json','.jpg'):
# #             print(f'파일이름 다르다 : {j_file}')
# #             continue
# #
# #         width, height = json_data["image"]["resolution"][0], json_data["image"]["resolution"][1]
# #         if json_data['image']['location'] == '01':
# #             location = '경기도 용인시 기흥구 지삼로331'
# #         elif json_data['image']['location'] == '02':
# #             location = '경기용인기흥구청덕동'
# #         elif json_data['image']['location'] == '03':
# #             location = '화성시 양감면 정문송산로93번길 10-59'
# #         elif json_data['image']['location'] == '04':
# #             location = '광주시 오포읍 고산리 242-6 1동'
# #         elif json_data['image']['location'] == '05':
# #             location = '용인시 기흥구 강남로 12 스카이프라자 704-2'
# #         elif json_data['image']['location'] == '06':
# #             location = '청주시 서원구 창직로 114'
# #         elif json_data['image']['location'] == '07':
# #             location = '전주시 덕진구 원만성로 21'
# #         elif json_data['image']['location'] == '08':
# #             location = '경기도가평군청평면대성리56-4'
# #         elif json_data['image']['location'] == '09':
# #             location = '충북 충주시 동량면 하천리'
# #         elif json_data['image']['location'] == '10':
# #             location = '용인시 기흥구 죽전로10 장은프라자'
# #         elif json_data['image']['location'] == '11':
# #             location = '화성시 정남면 수면리 133-1'
# #         elif json_data['image']['location'] == '12':
# #             location = '경기도 용인시 기흥구 청덕동 214-2'
# #         elif json_data['image']['location'] == '13':
# #             location = '화성시 양감면 정문송산로93번길 10-59'
# #         elif json_data['image']['location'] == '14':
# #             location = '경기도 용인시 기흥구 청명산로 41번지'
# #         elif json_data['image']['location'] == '15':
# #             location = '충남 부여군 내산면 금지리 산43'
# #         elif json_data['image']['location'] == '16':
# #             location = '화성시 양감면 정문송산로93번길 10-59'
# #         elif json_data['image']['location'] == '17':
# #             location = '경기화성송동727'
# #         elif json_data['image']['location'] == '18':
# #             location = '라오스, 비엔티엔'
# #
# #         img_dummy.append([img_name, img_path, width, height, location])
# #
# #
# # #     if idx % 100000 ==0:
# # #         dummy_list.to_csv(path_or_buf=f'F:/2022/fire_db_{idx}.csv', mode='w', index=False,encoding='utf-8-sig')
# # #
# # #         del dummy_list
# # #         dummy_list = pd.DataFrame(
# # #             columns=['IMG_NAME', 'OBJ_IDX', 'CLASS_CODE', 'ANNO_TYPE', 'BOX_X_MIN', 'BOX_Y_MIN', 'BOX_X_MAX',
# # #                      'BOX_Y_MAX', 'POLY_XCNTS', 'POLY_YCNTS'])
# # #
# # # dummy_list.to_csv(path_or_buf=f'F:/2022/fire_db_{idx}.csv', mode='w', index=False,encoding='utf-8-sig')
# #     # if 'polygon' in ann.keys():
# #     #     print(dummy_list)
# #
# #
# # #         try :
# # #             # if len(img_dummy) % 2000 == 0:
# # curs.executemany(sql, img_dummy)
# # conn.commit()
# # #                 # del img_dummy
# # #             img_dummy = []
# # #
# # #             # curs.executemany(sql2, dummy_list)
# # #             # conn.commit()
# # #
# #         # except Exception as e:
# #         #         conn.commit()
# #         #         # conn.close()
# #         #         # json_file.close()
# #         #         print(f'인서트 에러 : {e}')
# #         #         print(f'인서트 파일에러 : {j_file}')
# #         #         pass
# # #     del dummy_list
# # #     dummy_list = []
# # conn.close()
# # print("annotation tbl insert finish")
# #
# # # import pandas as pd
# # #
# # # df= pd.read_csv('F:/2022/fire_db_1730253.csv', encoding='utf-8')
# # # df_list = []
# # # for i in df['IMG_NAME']:
# # #     df_list.append(i.replace('.jpg','.json'))
# # # df_list = set(df_list)
# # # with open('F:/2022/img_list.txt', 'w', encoding='utf-8') as f:
# # #     for i in df_list:
# # #         f.write(i+'\n')
# #!/usr/bin/env python
#
# from __future__ import print_function
#
# import argparse
# import glob
# import os
# import os.path as osp
# import sys
#
# import imgviz
# import numpy as np
#
# import labelme
#
#
# def main():
#     parser = argparse.ArgumentParser(
#         formatter_class=argparse.ArgumentDefaultsHelpFormatter
#     )
#     parser.add_argument("--input_dir", default='F:/2022/code',help="input annotated directory")
#     parser.add_argument("--output_dir", default='F:/2022/code/results',help="output dataset directory")
#     parser.add_argument("--labels", default='labels.txt',help="labels file")
#     parser.add_argument(
#         "--noviz", help="no visualization", action="store_true"
#     )
#     args = parser.parse_args()
#
#     if osp.exists(args.output_dir):
#         print("Output directory already exists:", args.output_dir)
#         os.makedirs(args.output_dir, exist_ok=True)
#     os.makedirs(osp.join(args.output_dir, "JPEGImages"), exist_ok=True)
#     os.makedirs(osp.join(args.output_dir, "SegmentationClass"),exist_ok=True)
#     os.makedirs(osp.join(args.output_dir, "SegmentationClassPNG"),exist_ok=True)
#     if not args.noviz:
#         os.makedirs(
#             osp.join(args.output_dir, "SegmentationClassVisualization"), exist_ok=True
#         )
#     print("Creating dataset:", args.output_dir)
#
#     class_names = []
#     class_name_to_id = {}
#     for i, line in enumerate(open(args.labels).readlines()):
#         class_id = i - 1  # starts with -1
#         class_name = line.strip()
#         class_name_to_id[class_name] = class_id
#         if class_id == -1:
#             assert class_name == "__ignore__"
#             continue
#         elif class_id == 0:
#             assert class_name == "_background_"
#         class_names.append(class_name)
#     class_names = tuple(class_names)
#     print("class_names:", class_names)
#     out_class_names_file = osp.join(args.output_dir, "class_names.txt")
#     with open(out_class_names_file, "w") as f:
#         f.writelines("\n".join(class_names))
#     print("Saved class_names:", out_class_names_file)
#
#     for filename in glob.glob(osp.join(args.input_dir, "*.json")):
#         print("Generating dataset from:", filename)
#
#         label_file = labelme.LabelFile(filename=filename)
#         base = osp.splitext(osp.basename(filename))[0]
#         out_img_file = osp.join(args.output_dir, "JPEGImages", base + ".jpg")
#         out_lbl_file = osp.join(
#             args.output_dir, "SegmentationClass", base + ".npy"
#         )
#         out_png_file = osp.join(
#             args.output_dir, "SegmentationClassPNG", base + ".png"
#         )
#         if not args.noviz:
#             out_viz_file = osp.join(
#                 args.output_dir,
#                 "SegmentationClassVisualization",
#                 base + ".jpg",
#             )
#
#         with open(out_img_file, "wb") as f:
#             f.write(label_file.imageData)
#         img = labelme.utils.img_data_to_arr(label_file.imageData)
#
#         lbl, _ = labelme.utils.shapes_to_label(
#             img_shape=img.shape,
#             shapes=label_file.shapes,
#             label_name_to_value=class_name_to_id,
#         )
#         labelme.utils.lblsave(out_png_file, lbl)
#
#         np.save(out_lbl_file, lbl)
#
#         if not args.noviz:
#             viz = imgviz.label2rgb(
#                 lbl,
#                 imgviz.rgb2gray(img),
#                 font_size=15,
#                 label_names=class_names,
#                 loc="rb",
#             )
#             imgviz.io.imsave(out_viz_file, viz)
#
#
# if __name__ == "__main__":
#     main()


import cv2
import json
import os
from glob import glob

# img = cv2.imread('H:/Data/04_Industrial_safety/air/image/S1-N06161M04633.jpg')
# print(img)
# cv2.imshow('img',img)
# cv2.waitkey()
num = 0
for i in glob('D:/download/aa/*.json'):
    file_name = i.split("\\")[-1].replace('.json','.jpg')
    if not os.path.isfile(os.path.join('H:/Data/04_Industrial_safety/air/image',file_name)):
        # print(file_name)
        num+=1

print(num)
