## 데이터 복사 ##
from tqdm import tqdm
import shutil,os
from glob import glob
import json

# path = "C:/Users/human/Desktop/Workplace/Plan/*품질*"
#
# file_list = glob.glob(path, recursive=True)
# file_name = [os.path.basename(name) for name in file_list]
#
# test = 'C:/Users/human/Desktop/test/'
#
# for file in glob.glob('C:/Users/human/Desktop/Workplace/Plan/*품질*'):
#     print(file)
#     shutil.copy(file, test)


main_path = 'H:/Data/03_Landmark/label'
cls_dict = dict()
mid_dict = dict()

for j_file in tqdm(glob(main_path+'/**/*.json', recursive=True)):
    with open(os.path.join(main_path, j_file), encoding='utf-8-sig') as json_file:
        j_data = json.load(json_file)
        # print(j_data)
        for ann in j_data['regions']:
            if ann['class']=='castle gate':
                print(j_file)
                break

#         try:
#             for ann in j_data['regions']:
#                 if ann['class'] not in cls_dict.keys():
#                     cls_dict[ann['class']] = 1
#                 else :
#                     cls_dict[ann['class']] += 1
#
#                 if ann['tags'][5] not in mid_dict.keys():
#                     mid_dict[ann['tags'][5]] = 1
#                 else:
#                     mid_dict[ann['tags'][5]] +=1
#         except Exception as e:
#             print(j_file)
#             pass
# print(cls_dict)
# print('-'*50)
# print(mid_dict)

# import struct
# import numpy as np
# with open("G:/Request_data/data/TS/kitti/training/velodyne/000000.bin","rb") as f:
#     # data = f.read()
#
#     rectype = np.dtype(np.int32)
#     bdata=np.fromfile(f, dtype=rectype)
#
# print(bdata)
# for idx, i in enumerate(bdata):
#     if i==3:
#         print(i)

# import tensorflow as tf

# import json
#
# import numpy as np
#
# PATH = 'G:/다운로드/segment-10072231702153043603_5725_000_5745_000_with_camera_labels.tfrecord'


# import tensorflow.compat.v1 as tf
# tf.disable_v2_behavior()
# from PIL import Image
# import io
# import sys
#
# #tfrecord_filename = 'example_cat.tfrecord'
#
# def readRecord(filename_queue):
#     reader = tf.TFRecordReader()
#     _,serialized_example = reader.read(filename_queue)
#
#     #'''
#     keys_to_features = {
#         'image/height': tf.FixedLenFeature((), tf.int64, 1),
#         'image/width': tf.FixedLenFeature((), tf.int64, 1),
#         'image/colorspace': tf.FixedLenFeature((), tf.string, default_value=''),
#         'image/channels': tf.FixedLenFeature((), tf.int64, 1),
#         'image/class/label': tf.FixedLenFeature((), tf.int64, 1),
#         'image/class/text': tf.FixedLenFeature((), tf.string, default_value=''),
#         'image/format': tf.FixedLenFeature((), tf.string, default_value='JPEG'),
#         'image/filename': tf.FixedLenFeature((), tf.string, default_value=''),
#         'image/encoded': tf.FixedLenFeature((), tf.string, default_value=''),
#     }
#
#     features = tf.parse_single_example(serialized_example,features= keys_to_features)
#
#     height = tf.cast(features['image/height'],tf.int64)
#     width = tf.cast(features['image/width'],tf.int64)
#     colorspace = tf.cast(features['image/colorspace'], tf.string)
#     channels = tf.cast(features['image/channels'], tf.int64)
#     label = tf.cast(features['image/class/label'], tf.int64)
#     text = tf.cast(features['image/class/text'], tf.string)
#     format = tf.cast(features['image/format'],tf.string)
#     filename = tf.cast(features['image/filename'],tf.string)
#     encoded = tf.cast(features['image/encoded'],tf.string)
#
#
#     return height,width,colorspace,channels,label,text,format,filename,encoded
#
# def main():
#     if len(sys.argv) != 2:
#         print("Usage : python3 tfrecord_reader.py <tfrecord_file_name>")
#     else:
#         tfrecord_filename = sys.argv[1]
#         filename_queue = tf.train.string_input_producer([tfrecord_filename])
#         height,width,colorspace,channels,label,text,format,filename,encoded = readRecord(filename_queue)
#
#         init_op = tf.global_variables_initializer()
#
#         with tf.Session() as sess:
#             sess.run(init_op)
#
#             coord = tf.train.Coordinator()
#             threads = tf.train.start_queue_runners(coord=coord)
#
#             vheight,vwidth,vcolorspace,vchannels,vlabel,vtext,vformat,vfilename,vencoded = \
#             sess.run([height,width,colorspace,channels,label,text,format,filename,encoded])
#             print("vheight : %d" %vheight)
#             print("vwidth : %d" %vwidth)
#             print("vcolorspace : %s" %vcolorspace)
#             print("vchannels : %d" %vchannels)
#             print("vlabel : %d" %vlabel)
#             print("vtext : %s" %vtext)
#             print("vformat : %s" %vformat)
#             print("vfilename : %s" %vfilename)
#             image = Image.open(io.BytesIO(vencoded))
#             image.show()
#
#             coord.request_stop()
#             coord.join(threads)
#
# if __name__ == "__main__":
#     main()