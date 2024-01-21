
import pymysql
import pandas as pd
## 수정 파일 리스트 들고 오기
aa = pd.read_excel('Z:/공사/0205_오프라인툴/0205.xlsx', header=None)
filelist = list(aa[0])

for file_name in filelist:
# Connect DB
    conn = pymysql.connect(host = '172.16.0.20', user = 'humanf', password = '1234', port = 3307, database = 'unidentify')
    # conn = pymysql.connect(host = '172.16.0.5', user = 'uniden', password = 'uniden2020!@', port = 3306, database = 'indentify')  ### 5서버 DB접속
    curs = conn.cursor()
# Select Query
    sql = "UPDATE imagetbl SET Work_Yn = %s, Work_User = %s, Coordinates = %s WHERE Img_Name= %s;"
    curs.execute(sql, ('N', 'humanf2','NULL', file_name+'.jpg'))
    # commit 필수
    conn.commit()    
    conn.close()
    
print('완료')