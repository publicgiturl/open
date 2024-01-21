import numpy as np
from math import *
import json
import cv2

class Calibration():
    def read_calib(self, json_file):
        #json_list = ['front', 'left_front', 'left_rear', 'right_front', 'right_rear']
        with open(json_file) as j_file:
            json_data = json.load(j_file)
            extr = json_data[json_data['camera'].keys()[0]]['Extrinsic']
            intr = json_data[json_data['camera'].keys()[0]]['Intrinsic']

        return extr, intr

    def read_label(self, json_file, calib_file):
        cls_name = []
        xyz = []
        rotation = []
        scale_xyz = []

        extr, intr = self.read_calib(calib_file)


        with open(json_file) as j_file:
            json_data = json.load(j_file)

            cat_list = []
            for ann in json_data:
                cls_name.append(ann['obj_type'])
                xyz.append([ann['psr']['position']['x'], ann['psr']['position']['y'], ann['psr']['position']['z']])
                rotation.append([ann['psr']['rotation']['x'], ann['psr']['rotation']['y'], ann['psr']['rotation']['z']])
                scale_xyz.append([ann['psr']['scale']['x'], ann['psr']['scale']['y'], ann['psr']['scale']['z']])

                x, y = self.calculate_rt(extr, intr, xyz)

                cat_list.append(dict(
                    cls_name = cls_name,
                    x = x,
                    y = y
                ))

    def calculate_rt(self, extr, intr, xyz : list):
        extr_x, extr_y, extr_z = extr['Rx'], extr['Ry'], extr['Rz']
        intr_cx, intr_cy = intr['Cx'], intr['Cy']
        intr_fx, intr_fy = intr['Fx'], intr['Fy']

        k1 = intr['Distortion']['Param0']
        k2 = intr['Distortion']['Param1']
        p1 = intr['Distortion']['Param2']
        p2 = intr['Distortion']['Param3']

        c1 = cos(extr_x*np.pi/180)
        c2 = cos(extr_y*np.pi/180)
        c3 = cos(extr_z*np.pi/180)

        s1 = sin(extr_x*np.pi/180)
        s2 = sin(extr_y*np.pi/180)
        s3 = sin(extr_z*np.pi/180)

        R = np.array([[c2 * s3, -s2, c2 * c3], [-(c1 * c3) + (s1 * s2 * s3), (s1 * c2), (c1 * s3) + (s1 * s2 * c3)],
                      [-(s1 * c3) - (c1 * s2 * s3), (-c1 * c2), (s1 * s3) - (c1 * s2 * c3)]]).T
        T = np.array([extr['Tx'], extr['Ty'], extr['Tz']]).reshape(1, 3).T

        Tcw = np.dot(R,-T)



        calculate = np.hstack((R, Tcw))
        # print('TCW : ', calculate)
        xyz = np.array(xyz).reshape(4,1)
        cal_xyz = np.dot(calculate, xyz)

        xc = cal_xyz[0] / cal_xyz[2]
        yc = cal_xyz[1] / cal_xyz[2]
        r_2 = (xc**2) + (yc**2)

        x_d = xc * (1 + (k1 * r_2) + (k2 * (r_2**2))) + ((2 * p1 * xc * yc) + p2 * (r_2 + (2 * (xc**2))))
        y_d = yc * (1 + (k1 * r_2) + (k2 * (r_2**2))) + ((2 * p2 * xc * yc) + p1 * (r_2 + (2 * (yc**2))))

        u = intr_cx + (intr_fx * x_d)
        v = intr_cy + (intr_fy * y_d)
        x, y = self.calculate_scale_front(u, v)

        return x, y

    def calculate_scale_rear(self, u, v):
        cal_u = 319 - (u * 320 / 1920)
        cal_v = v * 180 / 1080
        return cal_u, cal_v
    def calculate_scale_front(self, u, v):
        cal_u = u * 640 / 1920
        cal_v = v * 360 / 1080
        return cal_u, cal_v
    def calculate_scale_sparse(self, u, v):
        cal_u = u * 320 / 1920
        cal_v = v * 180 / 1080
        return cal_u, cal_v


with open('D:/onss/Han/data/katech/katech/label/240_lidar.json') as j_file:
    json_data = json.load(j_file)
    rx, ry, rz = json_data[0]['psr']['rotation']['x'], json_data[0]['psr']['rotation']['y'], json_data[0]['psr']['rotation']['z']
    p_x, p_y, p_z = json_data[0]['psr']['position']['x'], json_data[0]['psr']['position']['y'], json_data[0]['psr']['position']['z']

    sx, sy, sz = json_data[0]['psr']['scale']['x'], json_data[0]['psr']['scale']['y'], json_data[0]['psr']['scale']['z']
    p1 = np.array([p_x, p_y, p_z]) + np.dot(np.array([[
        cos(rz), -sin(rz), 0],[
        sin(rz), cos(rz), 0],[
        0, 0, 1]]), np.array([-sx/2, sy/2, sz/2]))
    p2 = np.array([p_x, p_y, p_z]) + np.dot(np.array([[
        cos(rz), -sin(rz), 0], [
        sin(rz), cos(rz), 0], [
        0, 0, 1]]), np.array([-sx / 2, -sy / 2, sz / 2]))
    p3 = np.array([p_x, p_y, p_z]) + np.dot(np.array([[
        cos(rz), -sin(rz), 0], [
        sin(rz), cos(rz), 0], [
        0, 0, 1]]), np.array([sx / 2, sy / 2, sz / 2]))
    p4 = np.array([p_x, p_y, p_z]) + np.dot(np.array([[
        cos(rz), -sin(rz), 0], [
        sin(rz), cos(rz), 0], [
        0, 0, 1]]), np.array([sx / 2, -sy / 2, sz / 2]))
    p5 = np.array([p_x, p_y, p_z]) + np.dot(np.array([[
        cos(rz), -sin(rz), 0], [
        sin(rz), cos(rz), 0], [
        0, 0, 1]]), np.array([-sx / 2, sy / 2, -sz / 2]))
    p6 = np.array([p_x, p_y, p_z]) + np.dot(np.array([[
        cos(rz), -sin(rz), 0], [
        sin(rz), cos(rz), 0], [
        0, 0, 1]]), np.array([-sx / 2, -sy / 2, -sz / 2]))
    p7 = np.array([p_x, p_y, p_z]) + np.dot(np.array([[
        cos(rz), -sin(rz), 0], [
        sin(rz), cos(rz), 0], [
        0, 0, 1]]), np.array([sx / 2, sy / 2, -sz / 2]))
    p8 = np.array([p_x, p_y, p_z]) + np.dot(np.array([[
        cos(rz), -sin(rz), 0], [
        sin(rz), cos(rz), 0], [
        0, 0, 1]]), np.array([sx / 2, -sy / 2, -sz / 2]))
    for i in [p1,p2,p3,p4,p5,p6,p7,p8]:
        print(i)

img = cv2.imread('D:/onss/Han/data/katech/katech/camera/front/240_front.jpg')
with open('D:/onss/Han/data/katech/katech/calib/front.json') as j_file:
    json_data = json.load(j_file)
    extr = json_data['camera']['front']['Extrinsic']
    intr = json_data['camera']['front']['Intrinsic']

    calib = Calibration()
    x_coord = []
    y_coord = []
    for i in [p1,p2,p3,p4,p5,p6,p7,p8]:
        x,y = calib.calculate_rt(extr, intr, np.append(i,1).tolist())
        x_coord.append(x)
        y_coord.append(y)
        cv2.circle(img, (int(x), int(y)), 2, (255, 0, 0), 3, cv2.LINE_AA)
cv2.rectangle(img, (int(min(x_coord)), int(min(y_coord))), (int(max(x_coord)), int(max(y_coord))), (255,0,0), 2)
cv2.imshow('img', img)
cv2.waitKey(0)
# x_pos, y_pos, width, height = cv2.selectROI('location',img,False)
# print('x_position, y_position : ', x_pos, y_pos)
# print('width, height : ',width,height)
# cv2.destroyAllWindows()
# img_size = [1920, 1080]

