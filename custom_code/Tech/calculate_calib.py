import numpy as np
from math import *
import json

with open('/data2/data/katech/label/240_lidar.json') as j_file:
    json_data = json.load(j_file)
    x,y,z = json_data[0]['psr']['position']['x'], json_data[0]['psr']['position']['y'], json_data[0]['psr']['position']['z']
    sx,sy,sz = json_data[0]['rotation']['scale']['x'], json_data[0]['rotation']['scale']['y'], json_data[0]['rotation']['scale']['z']

xyz_3d = np.array([x,y,z,1], dtype=np.float).reshape(4,1)
scale_3d = np.array([sx,sy,sz,1], dtype=np.float).reshape(4,1)

with open('/data2/data/katech/calib/rightrear.json') as j_file:
    json_data = json.load(j_file)
    extr = json_data['camera']['right_rear']['Extrinsic']
    intr = json_data['camera']['right_rear']['Intrinsic']
    cx = json_data['camera']['right_rear']['Intrinsic']['Cx']
    cy = json_data['camera']['right_rear']['Intrinsic']['Cy']

    fx = json_data['camera']['right_rear']['Intrinsic']['Fx']
    fy = json_data['camera']['right_rear']['Intrinsic']['Fy']

    k1 = json_data['camera']['right_rear']['Intrinsic']['Distortion']['Param0']
    k2 = json_data['camera']['right_rear']['Intrinsic']['Distortion']['Param1']
    p1 = json_data['camera']['right_rear']['Intrinsic']['Distortion']['Param2']
    p2 = json_data['camera']['right_rear']['Intrinsic']['Distortion']['Param3']
    # p4 = json_data['camera']['right_rear']['Intrinsic']['Distortion']['Param4']
    # p5 = json_data['camera']['right_rear']['Intrinsic']['Distortion']['Param5']

    # calibration
    c1 = cos(extr['Rx'])
    c2 = cos(extr['Ry'])
    c3 = cos(extr['Rz'])

    s1 = sin(extr['Rx'])
    s2 = sin(extr['Ry'])
    s3 = sin(extr['Rz'])

    R = np.array([[c2*s3, -s2, c2*c3], [-(c1*c3)+(s1*s2*s3), s1*c2, (c1*s3)+(s1*s2*c3)],[-(s1*c3)-(c1*s2*s3), -c1*c2, (s1*s3)-(c1*s2*c3)]], dtype=np.float)
    T = np.array([extr['Tx'], extr['Ty'],extr['Tz']], dtype=np.float).reshape(1,3).T

calculate = np.hstack((R,T))

camrea_xyz = np.dot(calculate, xyz_3d)
scale_xyz = np.dot(calculate, scale_3d)

xc = np.float(camrea_xyz[0] / camrea_xyz[-1])
yc = np.float(camrea_xyz[1] / camrea_xyz[-1])
r_2 = np.float(sqrt(xc) + sqrt(yc))

x_d = xc*(1 + (k1 * r_2) + (k2 * sqrt(r_2))) + ((2 * p1 * xc * yc) + p2*(r_2 + (2 * sqrt(xc))))
y_d = yc*(1 + (k1 * r_2) + (k2 * sqrt(r_2))) + ((2 * p2 * x * yc) + p1*(r_2 + (2 * sqrt(yc))))

u = cx + fx * x_d
v = cy + fy * y_d

new_u = 319-(u*320/1920)
new_v = v*180/1080

print(new_u, new_v)

xc = np.float(scale_xyz[0] / scale_xyz[-1])
yc = np.float(scale_xyz[1] / scale_xyz[-1])

r_2 = (xc*xc) + (yc*yc)

x_d = xc*(1 + (k1 * r_2) + (k2 * sqrt(r_2))) + ((2 * p1 * xc * yc) + p2*(r_2 + (2 * (xc*xc))))
y_d = yc*(1 + (k1 * r_2) + (k2 * sqrt(r_2))) + ((2 * p2 * x * yc) + p1*(r_2 + (2 * (yc*yc))))

u = cx + fx * x_d
v = cy + fy * y_d

new_u = 319-(u*320/1920)
new_v = v*180/1080
print(new_u,new_v)

class Calibration():
    
    def world2carmera(self, R, T, x, y, z):
        calculate = np.hstack((R, T))
        cal_xyz = np.dot(calculate, xyz_3d)

        return cal_xyz

    def convert_3D22D(self, xyz, fx, fy, cx, cy):
        xc = np.float(xyz[0] / xyz[-1])
        yc = np.float(xyz[1] / xyz[-1])
        r_2 = np.float(sqrt(xc) + sqrt(yc))

        x_d = xc * (1 + (k1 * r_2) + (k2 * sqrt(r_2))) + ((2 * p1 * xc * yc) + p2 * (r_2 + (2 * sqrt(xc))))
        y_d = yc * (1 + (k1 * r_2) + (k2 * sqrt(r_2))) + ((2 * p2 * x * yc) + p1 * (r_2 + (2 * sqrt(yc))))

        u = cx + fx * x_d
        v = cy + fy * y_d

        x, y = self.calculate_scale_rear(u,v)

        return x, y

    def calculate_scale_rear(self, u, v):
        cal_u = 319 - (u * 320 / 1920)
        cal_v = v * 180 / 1080
        return cal_u, cal_v
    # import cv2
#
# img = cv2.imread('/data2/data/katech/camera/rightrear/240_rightrear.jpg')
# # cv2.line(img, (int(121.3216610089392), int(72)), (0,0),(255,0,0))
# cv2.rectangle(img, (int(121.3216610089392), int(60)), (int(319), int(179)), (255,0,0), 2)
# cv2.imshow('img',img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
