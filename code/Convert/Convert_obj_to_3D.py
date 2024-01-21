import numpy as np
from xml.etree.ElementTree import Element, SubElement, ElementTree
from glob import glob

coord = []
convert_coord = {}
num = 1
obj_cnt = 0
for obj_file in glob('C:/Users/MIngsu/Desktop/*.obj'):
    obj_cnt += 1
    with open(f'{obj_file}', 'r') as f:
        for idx, i in enumerate(f):
            i = i.split('\n')[0].split(' ')
            if i[0] =='v' and ((idx+1)%8) ==0:
                # print([float(i[2]), float(i[1]), float(i[3])])
                # print('{}_nd'.format(num))
                coord.append([float(i[2]), float(i[1]), float(i[3])])
                convert_coord['{}_nd'.format(num)] = coord
                coord = []
                num += 1
            elif idx+1 % 8 != 0 or idx==0:
                coord.append([float(i[2]), float(i[1]), float(i[3])])

print(convert_coord.keys())
xml_file = open('C:/Users/MIngsu/Desktop/tracklet_labels_test.xml', 'w',encoding='utf-8')

xml_file.write(f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<!DOCTYPE boost_serialization>
<boost_serialization version="9" signature="serialization::archive">
<tracklets version="0" tracking_level="0" class_id="0">
  <count>{len(convert_coord.keys())}</count>
  <item_version>1</item_version>''')

for idx, val in enumerate(convert_coord):
    if idx==0 :
        xml_file.write(f'''<item version="1" tracking_level="0" class_id="1">
        <objectType>car</objectType>
        <h>{max(convert_coord[val][0][1], convert_coord[val][2][1]) - min(convert_coord[val][0][1], convert_coord[val][2][1])}</h>
        <w>{max(convert_coord[val][0][0], convert_coord[val][4][0]) - min(convert_coord[val][0][0], convert_coord[val][4][0])}</w>
        <l>{max(convert_coord[val][0][2], convert_coord[val][1][2]) - min(convert_coord[val][0][2], convert_coord[val][1][2])}</l>
        <first_frame>{obj_cnt}</first_frame>
        <poses version="0" tracking_level="0" class_id="2">
        <count>1</count>
        <item_version>0</item_version>
        <item version="1" tracking_level="0" class_id="3">
        <tx>{(convert_coord[val][0][0]+convert_coord[val][4][0])/2}</tx>
        <ty>{-(convert_coord[val][0][1]+convert_coord[val][2][1])/2}</ty>
        <tz>{(convert_coord[val][0][2]+convert_coord[val][1][2])/2}</tz>
        <rx>0</rx>
        <ry>0</ry>
        <rz>0</rz>
        <state>2</state>
        <occlusion>0</occlusion>
        <occlusion_kf>0</occlusion_kf>
        <truncation>0</truncation>
        <amt_occlusion>-1</amt_occlusion>
        <amt_border_l>-1</amt_border_l>
        <amt_border_r>-1</amt_border_r>
        <amt_occlusion_kf>-1</amt_occlusion_kf>
        <amt_border_kf>-1</amt_border_kf>
        </item>
        </poses>
        <finished>1</finished>
        </item>''')
    else:
        xml_file.write(f'''<item>
    <objectType>car</objectType>
    <h>{max(convert_coord[val][0][1], convert_coord[val][2][1]) - min(convert_coord[val][0][1], convert_coord[val][2][1])}</h>
    <w>{max(convert_coord[val][0][0], convert_coord[val][4][0]) - min(convert_coord[val][0][0], convert_coord[val][4][0])}</w>
    <l>{max(convert_coord[val][0][2], convert_coord[val][1][2]) - min(convert_coord[val][0][2], convert_coord[val][1][2])}</l>
    <first_frame>0</first_frame>
    <poses>
      <count>1</count>
      <item_version>0</item_version>
      <item>
        <tx>{(convert_coord[val][0][0]+convert_coord[val][4][0])/2}</tx>
        <ty>{-(convert_coord[val][0][1]+convert_coord[val][2][1])/2}</ty>
        <tz>{(convert_coord[val][0][2]+convert_coord[val][1][2])/2}</tz>
        <rx>0</rx>
        <ry>0</ry>
        <rz>0</rz>
        <state>2</state>
        <occlusion>0</occlusion>
        <occlusion_kf>0</occlusion_kf>
        <truncation>0</truncation>
        <amt_occlusion>-1</amt_occlusion>
        <amt_border_l>-1</amt_border_l>
        <amt_border_r>-1</amt_border_r>
        <amt_occlusion_kf>-1</amt_occlusion_kf>
        <amt_border_kf>-1</amt_border_kf>
      </item>
    </poses>
    <finished>1</finished>
  </item> ''')

xml_file.write('''</tracklets>
</boost_serialization>''')
xml_file.close()
