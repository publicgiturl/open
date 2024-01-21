import os, glob, shutil


# json파일 이름명 추출
### 주소만 변경 ###
re_list = ['20191026_re', ]
for i in re_list:
    jpg  = []
    json = []
    NG = []
    no_jpg = []
    main_path = 'Z:/추가작업/{}'.format(i)

    os.chdir(main_path)
    for file in glob.glob("*.json"):
        json.append(file.split('.')[0])

    # jpg파일 이름명 추출    
    for file in glob.glob("*.jpg"):
        jpg.append(file.split('.')[0])

    # Jpg만 있는 파일 삭제
    for v in jpg:
        if v not in json:
            os.remove(v+'.jpg')
    print(main_path+'완료')
