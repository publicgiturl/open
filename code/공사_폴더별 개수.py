import glob, os, shutil
import csv
import xml.etree.ElementTree as ET
import json
from openpyxl import Workbook
import pandas as pd
import pymysql
from openpyxl import Workbook
from openpyxl import load_workbook

write_xl = Workbook()
write_ws = write_xl.active
write_ws.append(['Folder', 'Image', 'BB', 'polygon'])

bb_list = os.listdir('F:/작업폴더/카운트/csv파일/BB')
po_list = os.listdir('F:/작업폴더/카운트/csv파일/PO')

for i in range(len(bb_list)):
    globals()[bb_list[i]] = pd.read_csv('F:/작업폴더/카운트/csv파일/BB/' + bb_list[i], index_col=0)
    globals()[po_list[i]] = pd.read_csv('F:/작업폴더/카운트/csv파일/PO/' + po_list[i], index_col=0)
    
    write_ws.append([bb_list[i].split('.csv')[0], len(globals()[bb_list[i]]), globals()[bb_list[i]]['BB'].sum(), globals()[po_list[i]]['PO'].sum()])

write_xl.save('Y:/양식/공사_폴더별_개수.xlsx')