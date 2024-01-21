# import cv2
# import mediapipe as mp
# import numpy as np
# mp_drawing = mp.solutions.drawing_utils
# mp_pose = mp.solutions.pose
#
# cap = cv2.VideoCapture(1)
#
# # cap = cv2.VideoCapture('dance.mp4')  # 영상파일
#
# # Curl counter variables
# counter = 0
# stage = None
#
# ## Setup mediapipe instance
# with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
#     while cap.isOpened():
#         ret, frame = cap.read()
#
#         # Recolor image to RGB
#         image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         image.flags.writeable = False
#
#         # Make detection
#         results = pose.process(image)
#
#         # Recolor back to BGR
#         image.flags.writeable = True
#         image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
#
#         # Extract landmarks
#         try:
#             landmarks = results.pose_landmarks.landmark
#
#             # Get coordinates
#             # shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
#             nose = [landmarks[mp_pose.PoseLandmark.NOSE.value].x, landmarks[mp_pose.PoseLandmark.NOSE.value].y]
#             # elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
#             # wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
#
#             # Calculate angle
#             # angle = calculate_angle(shoulder, elbow, wrist)
#             angle = calculate_angle(nose)
#             print(nose)
#             # Visualize angle
#             cv2.putText(image, str(NOSE),
#                         tuple(np.multiply(elbow, [640, 480]).astype(int)),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
#                         )
#
#             # Curl counter logic
#             if angle > 100:
#                 stage = True
#             if angle < 150 and stage == True:
#                 stage = "Falling"
#                 counter += 1
#                 print(counter)
#
#         except:
#             pass
#
#         # Render curl counter
#         # Setup status box
#         cv2.rectangle(image, (0, 0), (225, 73), (245, 117, 16), -1)
#
#         # Rep data
#         cv2.putText(image, 'REPS', (15, 12),
#                     cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
#         cv2.putText(image, str(counter),
#                     (10, 60),
#                     cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)
#
#         # Stage data
#         cv2.putText(image, 'STAGE', (65, 12),
#                     cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
#         cv2.putText(image, stage,
#                     (60, 60),
#                     cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)
#
#         # Render detections
#         mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
#                                   mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
#                                   mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
#                                   )
#
#         cv2.imshow('Mediapipe Feed', image)
#
#         if cv2.waitKey(10) & 0xFF == ord('q'):
#             break
#
#     cap.release()
#     cv2.destroyAllWindows()

import json
import os
from glob import glob
from tqdm import tqdm
import shutil
import cv2

# img = cv2.imread('H:/Data/07_warehouse/images/L-211007_G07_B_UA-01_0219.jpg')
# cv2.imshow('img',img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
#
# with open('H:/Data/07_warehouse/label/L-211007_G07_B_UA-01_0219.json') as json_file:
#     json_data = json.load(json_file)
#     print(json_data)

num = 0

for i in tqdm(glob('H:/Data/07_warehouse/images/*.jpg',recursive=True)):
    file_name = i.split('\\')[-1].replace('.jpg','.json')
    # shutil.copy(i, f'H:/Data/07_warehouse/images/{file_name}')
    if os.path.isfile(f'H:/Data/07_warehouse/label/{file_name}'):
        pass
    else:
        # num+=1
        os.remove(i)
        # print(file_name)
# print('not_match_img2json',num)

num = 0
for i in tqdm(glob('H:/Data/07_warehouse/label/*.json',recursive=True)):
    file_name = i.split('\\')[-1].replace('.json','.jpg')
    # shutil.copy(i, f'H:/Data/07_warehouse/images/{file_name}')
    if os.path.isfile(f'H:/Data/07_warehouse/images/{file_name}'):
        pass
    else:
        # num+=1
        os.remove(i)
        # print(file_name)
# print('not_match_json2img',num)

num = 0

for i in tqdm(glob('H:/Data/07_warehouse/images/*.jpg',recursive=True)):
    file_name = i.split('\\')[-1].replace('.jpg','.json')
    # shutil.copy(i, f'H:/Data/07_warehouse/images/{file_name}')
    if os.path.isfile(f'H:/Data/07_warehouse/label/{file_name}'):
        pass
    else:
        num+=1
        # os.remove(i)
        # print(file_name)
print('not_match_img2json',num)

num = 0
for i in tqdm(glob('H:/Data/07_warehouse/label/*.json',recursive=True)):
    file_name = i.split('\\')[-1].replace('.json','.jpg')
    # shutil.copy(i, f'H:/Data/07_warehouse/images/{file_name}')
    if os.path.isfile(f'H:/Data/07_warehouse/images/{file_name}'):
        pass
    else:
        num+=1
        # os.remove(i)
        # print(file_name)
print('not_match_json2img',num)