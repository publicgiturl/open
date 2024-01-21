import cv2
from glob import glob
from tqdm import tqdm
import numpy as np
import os

# path 설정
video_path = 'E:/sample/*.avi'


# # 1/n 프레임 수 확인
# frames_step = total_frames//10

#for frame identity
for i, video in enumerate(glob(video_path)):
    print('{}번째 파일 시작'.format(i+1))
    # set video file path of input video with name and extension
    vid = cv2.VideoCapture(video)
    out_put_path = 'E:/sample/result/{}'.format(video.split('\\')[-1].split('.avi')[0])
    # 전체 프레임 수 확인
    total_frames = vid.get(cv2.CAP_PROP_FRAME_COUNT)
    index = 1

    if not os.path.exists(out_put_path):
        os.makedirs(out_put_path)

    while(True):
        # Extract images
        ret, frame = vid.read()
        # end of frames, 마지막 frame은 제외
        if not ret or index==3601:
            break
        # Saves images
        name = os.path.join(out_put_path, video.split('\\')[-1].split('.avi')[0] + '_' + str(index) + '.jpg')
        # print ('Creating...' + name)
        cv2.imwrite(name, frame)

        # next frame
        index += 1
    print('{0}번째 파일 완료'.format(i+1))