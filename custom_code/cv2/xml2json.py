import cv2
import json
import xmltodict

xml_path = '/data2/2021/차량외관/2D_165_set_f(앞)_r(뒤)/task_p1-001r-2021_10_15_07_28_21-pascal voc 1.1/Annotations/1630546831.687456885.xml'
img_path = '/data2/2021/차량외관/2D_165_set_f(앞)_r(뒤)/task_p1-001r-2021_10_15_07_28_21-pascal voc 1.1/JPEGImages/1630546831.687456885.jpg'
json_path = '/data2/2021/차량외관/2D_165_set_f(앞)_r(뒤)/task_p1-001r-2021_10_15_07_28_21-pascal voc 1.1/Annotations/1630546831.687456885.json'


with open(xml_path, 'r') as f:
    xmlString = f.read()

print("xml input (xml_to_json.xml):")
print(xmlString)

jsonString = json.dumps(xmltodict.parse(xmlString), indent=4)

print("\nJSON output(output.json):")
print(jsonString)

with open(xml_path.replace('.xml','.json'), 'w') as f:
    f.write(jsonString)

img = cv2.imread(img_path)

with open(json_path) as json_file:
    json_data = json.load(json_file)

    for ann in json_data['annotation']['object']:
        xmin = int(float(ann['bndbox']['xmin']))
        ymin = int(float(ann['bndbox']['ymin']))
        xmax = int(float(ann['bndbox']['xmax']))
        ymax = int(float(ann['bndbox']['ymax']))

        print(xmin, ymin, xmax, ymax)
        cv2.rectangle(img, (xmin, ymin), (xmax,ymax), (255,255,0), 2)

    cv2.imshow('img',img)
    cv2.waitKey(0)