import cv2
import numpy as np

# # 입력 이미지 파일 경로
image_path = '/data2/자율주행/train/test5_12segs_weather_0_spawn_0_roadTexture_2_P_20_C_None_B_20_WC_100/24-10-2018_13-03-55/SemSeg/000101.png'
ori_image = '/data2/자율주행/train/test5_12segs_weather_0_spawn_0_roadTexture_2_P_20_C_None_B_20_WC_100/24-10-2018_13-03-55/RGB/000101.png'

img = cv2.imread(image_path)

unique_colors = np.unique(img.reshape(-1, img.shape[2]), axis=0)

ori_img = cv2.imread(ori_image)

for target_color in unique_colors:
	if np.array_equal(target_color, np.array([0, 0, 0])) or np.array_equal(target_color, np.array([255, 255, 255])):
		continue

	mask = cv2.inRange(img, np.array(target_color), np.array(target_color))

	contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	for contour in contours:
		contour = np.squeeze(contour, axis=1)
		xmin, ymin, xmax, ymax = np.min(contour[:,0]), np.min(contour[:,1]),np.max(contour[:,0]),np.max(contour[:,1])
		if (xmax-xmin)*(ymax-ymin)<20*20:
			continue
		cv2.rectangle(ori_img, (xmin,ymin), (xmax, ymax), (0,0,255), 2)
		# cv2.polylines(ori_img, [contour], isClosed=True, color=(0, 0, 255), thickness=2)
		# cv2.drawContours(ori_img, [contour], -1, (0, 0, 255), 2)

# cv2.imwrite('test_2.jpg', ori_img)
cv2.imshow('img', ori_img)
cv2.waitKey(0)