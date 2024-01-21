import os, glob

class Getallfiles:
    def __init__(self):
        pass
    def getFiles(self,dir):
        x = 0
        for pack in os.walk(dir):
            for f in pack[2]:
                if f.endswith('.jpg'):
                    x+=1
        print(('Dir: %s, 전체 파일수 : %s')%(dir,str(x)))
if __name__ =='__main__':
    f= Getallfiles()
    f.getFiles('F:/비어노테이션(이미지)')
    f.getFiles('E:/비어노테이션이미지')