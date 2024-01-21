
import pymysql
import pandas as pd


# Connect DB
conn = pymysql.connect(host = '172.16.0.20', user = 'humanf', password = '1234', port = 3307, database = 'unidentify') ### 20서버 DB접속
curs = conn.cursor()

# Select Query
sql = "SELECT Work_User, Date_Format(Work_Date, '%Y-%m-%d'), count(*) FROM workhistory group by Date_Format(Work_Date, '%Y-%m-%d'), Work_User;"  ### 전체 작업량(패스 포함)
sql2 =  "SELECT Work_User, Date_Format(Work_Date, '%Y-%m-%d'), count(*) FROM imagetbl group by Date_Format(Work_Date, '%Y-%m-%d'), Work_User, Work_Yn HAVING Work_Yn = 'Y';"  ### 실 작업량

curs.execute(sql)
rows = curs.fetchall()

curs.execute(sql2)
rows2 = curs.fetchall()
    
conn.close()
daily_work = pd.DataFrame(rows, columns=['Worker', 'Date', 'Work'])
daily_work2 = pd.DataFrame(rows2, columns=['Worker', 'Date', 'Work_T'])

daily_merge = pd.merge(daily_work, daily_work2, on = ['Date', 'Worker'] )
daily_count = daily_merge.groupby(['Date','Worker'])['Work','Work_T'].sum()
daily_count.to_excel('Z:/공사/daily_count.xlsx', header=True, encoding='utf-8')
print(daily_count)

### 서버 작업량 확인

# Connect DB
conn = pymysql.connect(host = '172.16.0.5', user = 'uniden', password = 'uniden2020!@', port = 3306, database = 'indentify')  ### 5서버 DB접속
curs = conn.cursor()

# Select Query
sql = "SELECT Work_User, Date_Format(Work_Date, '%Y-%m-%d'), count(*) FROM workhistory group by Date_Format(Work_Date, '%Y-%m-%d'), Work_User;"  ### 전체 작업량(패스 포함)
sql2 =  "SELECT Work_User, Date_Format(Work_date, '%Y-%m-%d'), count(*) FROM imagetbl group by Date_Format(Work_date, '%Y-%m-%d'), Work_User, Work_Yn HAVING Work_Yn = 'Y';"  ### 실 작업량

curs.execute(sql)
rows = curs.fetchall()

curs.execute(sql2)
rows2 = curs.fetchall()
    
conn.close()
daily_work = pd.DataFrame(rows, columns=['Worker', 'Date', 'Work'])
daily_work2 = pd.DataFrame(rows2, columns=['Worker', 'Date', 'Work_T'])

daily_merge = pd.merge(daily_work, daily_work2, on = ['Date', 'Worker'] )
daily_count = daily_merge.groupby(['Date','Worker'])['Work','Work_T'].sum()
daily_count.to_excel('Z:/공사/daily_count_server.xlsx', header=True, encoding='utf-8')
print(daily_count)