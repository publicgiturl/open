from mmdet.apis import (async_inference_detector, inference_detector,
                        init_detector, show_result_pyplot, single_gpu_test)
import cv2
import rasterio
import os.path as osp
import os
from rasterio import features
import shapely
from tqdm import tqdm
from glob import glob
from shapely.geometry import Point, Polygon, mapping
import numpy as np
import json

# labels_to_names_seq = {0: 'pedestrian', 1: 'vehicle', 2: 'sidewalk', 3: 'road', 4: 'traffic light', 5: 'rider',
#                        6: 'motorcycle', 7: 'mountain', 8: 'bulding', 9: 'bicycle', 10: 'sky', 11:'traffic sign'} #'traffic sign',
#                        #12: 'undefined object/area'}
labels_to_names_seq = {0: 'pedestrian', 1: 'vehicle', 2: 'sidewalk', 3: 'road', 4: 'traffic light', 5: 'rider',
                       6: 'motorcycle', 7: 'mountain', 8: 'bulding', 9: 'bicycle', 10: 'sky', 11: 'traffic sign',
                       12: 'undefined object/area'}

model_ckpt = init_detector('/data/TS/logs/yolact_ts_r101.py',
                           '/data/TS/logs/latest.pth', device='cuda:0')

# '/data/ai_dataSet/Model/mmdetection/configs/yolact_ts_r101.py'
#'/data/ai_dataSet/Model/mmdetection/TS/logs/latest.pth'
# model_ckpt = init_detector('/data/ai_dataSet/Model/mmdetection/TS/logs/yolact_ts_r101.py',
#                            '/data/ai_dataSet/Model/mmdetection/TS/logs/latest.pth', device=0)

def modify_coord(points):
    points = np.array(points)
    # re_point = np.sort(points.reshape(points.shape[1]//2,2),axis=0)
    re_point = points.reshape(points.shape[1]//2,2)

    x_list = re_point[:, 0]
    y_list = re_point[:, 1]

    modify_coord = []
    if re_point.shape[0]<10:
        for idx, coord in enumerate((zip(x_list, y_list))):
            modify_coord.append(coord)
    if re_point.shape[0]<100:
        for idx, coord in enumerate((zip(x_list, y_list))):
            if idx%3==0:
                modify_coord.append(coord)
    elif re_point.shape[0]<500:
        for idx, coord in enumerate((zip(x_list, y_list))):
            if idx % 5 == 0:
                modify_coord.append(coord)
    elif re_point.shape[0]<1000:
        for idx, coord in enumerate((zip(x_list, y_list))):
            if idx % 8 == 0:
                modify_coord.append(coord)
    elif re_point.shape[0] < 2000:
        for idx, coord in enumerate((zip(x_list, y_list))):
            if idx % 10 == 0:
                modify_coord.append(coord)
    # for idx, coord in enumerate((zip(x_list, y_list))):
    #     if idx == 0:
    #         modify_coord.append(coord)
    #     else:
            # if (modify_coord[-1][0] != coord[0] and modify_coord[-1][1] != coord[1]) or \
            # if (modify_coord[-1][0] != coord[0] and abs(modify_coord[-1][0] - coord[0]) > 0.5) or \
            #         (modify_coord[-1][1] != coord[1] and abs(modify_coord[-1][1] - coord[1]) > 0.5):
            # if modify_coord[-1][0] != coord[0] and modify_coord[-1][1] != coord[1]:
                    # (modify_coord[-1][0] != coord[0] and abs(modify_coord[-1][1] - coord[1]) > 3):
            # modify_coord.append(coord)
    # if len(modify_coord) <4 :
    #     return 0
    # else:
    modify_coord = [list(np.asarray(modify_coord).flatten())]
    return modify_coord

def mask_to_polygons_layer(mask):
    all_polygons = []
    for shape, value in features.shapes(mask.astype(np.int16), mask=(mask > 0),
                                        transform=rasterio.Affine(1.0, 0, 0, 0, 1.0, 0)):
        return shapely.geometry.shape(shape)
        all_polygons.append(shapely.geometry.shape(shape))

    all_polygons = shapely.geometry.MultiPolygon(all_polygons)
    if not all_polygons.is_valid:
        all_polygons = all_polygons.buffer(0)
        if all_polygons.type == 'Polygon':
            all_polygons = shapely.geometry.MultiPolygon([all_polygons])
    return all_polygons


def change_class(class_path):
    with open(class_path, encoding='utf-8') as f:
        cls_dict = []
        for idx, cls in enumerate(f):
            cls_dict.append(dict(id=idx + 1, name=cls.split('\n')[0]))
    return cls_dict


obj = 1
for root, dirs, files in os.walk('/home/user/Downloads/030_일출일몰_비_일반도로_211005_01/test'):
    img_list = []
    annotations = []  # total list infomation

    for idx, img in enumerate(tqdm(sorted(files), desc='Files :')):
        if img.endswith(('.jpg', 'png')):
            img_path = osp.join(root, img)
            height, width = cv2.imread(img_path).shape[:2]
            img_list.append({'id': idx+1, 'image': img.split('/')[-1], 'width': width, 'height': height})
            result = inference_detector(model_ckpt, cv2.imread(img_path))
            box, seg = result[0], result[1]

            for result_ind, bbox_result in enumerate(box):
                if len(bbox_result) == 0:
                    continue
                mask_array_list = seg[result_ind]

                try:
                    for i in range(len(bbox_result)):
                        # print(len(bbox_result))
                        detailInfo = {}  # 1 class value infomation
                        if bbox_result[i, 4] > 0.3:
                            polygons = mask_to_polygons_layer(mask_array_list[i])
                            area = polygons.area

                            if polygons.type=='GeometryCollection':
                                pass
                            else:
                                polygons = [list(np.array(polygons.exterior.coords).flatten())]
                                left = int(bbox_result[i, 0])
                                top = int(bbox_result[i, 1])
                                right = int(bbox_result[i, 2])
                                bottom = int(bbox_result[i, 3])
                                caption = "{}: {:.4f}".format(labels_to_names_seq[result_ind], bbox_result[i, 4])

                                detailInfo['id'] = obj
                                detailInfo['image_id'] = idx+1
                                detailInfo['category_id'] = result_ind+1
                                detailInfo['segmentation'] = modify_coord(polygons)
                                detailInfo['area'] = area
                                detailInfo['bbox'] = [left, top, right, bottom]
                                detailInfo["iscrowd"] = 0
                                annotations.append(detailInfo)

                                obj += 1

                except Exception as e:
                    print('\nerror :',e)
                    print(img)
                    pass
        else:
            continue


    coco_format_json = dict(
        images=img_list,
        annotations=annotations,
        categories=change_class('/data/ts_class.names')
        )

    if files and ('.jpg' in files[0] or '.png' in files[0]):
        new_path = osp.join(root, files[0])
        if not osp.exists('{}_label'.format(osp.join('/'.join(new_path.split('/')[:-1])))):
            os.mkdir('{}_label'.format(osp.join('/'.join(new_path.split('/')[:-1]))))
        print('make_json')
        with open('{}_label/segmentation.json'.format(osp.join('/'.join(new_path.split('/')[:-1]))), 'w', encoding='utf-8') as json_file:
            json.dump(coco_format_json, json_file, ensure_ascii=False, indent=2)

print('done')
