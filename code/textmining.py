# f = open("test.txt", "w", encoding="utf-8")
# f.write("안녕, 스파르타!\n")
#
# for i in [1,2,3,4,5]:
#     f.write(f"{i}번째 줄입니다.\n")
#
# f.close()
from wordcloud import WordCloud
from PIL import Image
import numpy as np

# # 파일을 열고
text = ''
with open("임다정.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()
    for line in lines:
        if '] [' in line :
            text += line.split('] ')[2].replace('ㅎㅎ','').replace('으궁','').replace('너가','').replace('내가','').replace('오늘','').replace('웅웅','').replace('그랭','').replace('그럼','').replace('그치','').replace('ㅋ','').replace('ㅠ','').replace('ㅜ','').replace('이모티콘\n','').replace('사진\n','').replace('삭제된 메시지입니다\n','')

# text파일을 읽어와서 각 줄별로 변수에 저장


# # 이용 가능한 폰트 중 '고딕'만 선별
# import matplotlib.font_manager as fm
#
# # 이용 가능한 폰트 중 '고딕'만 선별
# for font in fm.fontManager.ttflist:
#     if 'Gothic' in font.name:
#         print(font.name, font.fname)

# print(text)


# wc = WordCloud(font_path='C:/Windows/Fonts/malgun.ttf', background_color="white", width=600, height=400)
# wc.generate(text)
# wc.to_file("result.png")


mask = np.array(Image.open('cloud.png'))
wc = WordCloud(font_path='C:/Windows/Fonts/malgun.ttf', background_color="white", mask=mask)
wc.generate(text)
wc.to_file("result_masked.png")