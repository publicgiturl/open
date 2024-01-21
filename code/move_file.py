from re import split
import shutil, os, glob

# move_list = os.listdir('F:/') ### for the copytree

# for i in move_list:
#     try:
#         shutil.copytree('F:/{}'.format(i), 'E:/산업안전_공사/{}'.format(i))

#     except :
#         pass

## for the individual file copy
for path, dir, files in os.walk('F:/1.Training/라벨링데이터'): 
    for file_name in files:
        try :
            if os.path.isfile(os.path.join('E:/비어노테이션이미지', file_name)):
                pass
            else:
                src = os.path.join(path, file_name)
                dst = os.path.join('E:/비어노테이션이미지', file_name)
                shutil.copy(src, dst)
        except:
            pass
### 특정 확장자 지우기
# for i in glob.glob('E:/비어노테이션이미지/*.json'):
#     if os.path.isfile(i):
#         os.remove(i)