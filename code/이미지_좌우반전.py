from PIL import Image
import json, os, glob, re

main_path = 'F:/새 폴더/aa' # 파일위치
jpg_list = glob.glob('{}/*.jpg'.format(main_path))

for jpg_name in jpg_list:
    row_jpg = jpg_name.split('\\')[-1]
    if len(row_jpg) == 19:
        number = re.findall('\d{5}',row_jpg)[-1]
    elif len(row_jpg) == 18:
        number = re.findall('\d{5}',row_jpg)[-1]
        
    new_number= int(''.join(number)) + 100000
    json_name = re.sub('.jpg', '.json', jpg_name)

    if len(row_jpg) > 18:
        new_jpg = row_jpg.split('M')[0] +'M'+ re.sub('\d{5}', str(new_number),row_jpg.split('M')[-1])   # 반전된 jpg이름
    elif len(row_jpg) == 18:
        new_jpg = re.sub('\d{5}', str(new_number), row_jpg)
        
    new_json = new_jpg.replace('.jpg', '.json')   # 반전된 json이름
    re_path = jpg_name.split('\\')[0]+'_re'
    
    image1 = Image.open(jpg_name)   #이미지 불러오기
    FlipImage = image1.transpose(Image.FLIP_LEFT_RIGHT)   #이미지 좌우대칭
    
    if not (os.path.isdir(re_path)):   # _re폴더 생성
        os.makedirs(re_path)    
    FlipImage.save(os.path.join(re_path, new_jpg))
# 
    try:
        with open(json_name, encoding='utf-8') as json_file:
            json_data = json.load(json_file)
            json_data['image']['filename'] = new_jpg
            annotation = json_data['annotations']
            
            for i in range(len(annotation)):
                annotation[i]['box'][0] = 1920-annotation[i]['box'][0]
                annotation[i]['box'][2] = 1920-annotation[i]['box'][2]
               
        with open(os.path.join(re_path, new_json), 'w', encoding='utf-8') as json_change:
            json.dump(json_data, json_change, indent=2, ensure_ascii = False)
                            
    finally:
        json_file.close()