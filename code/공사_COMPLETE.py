import pyautogui as m
import keyboard
import time
import mouse


point3 = (1860, 1010) # Complete
point4 = (820, 510) # Center -> BB커서
print("H : COMPLETE\n")
print("/ : 단축키 일시중지/실행\n")
print("* 크롬 전체화면, 화면비율 100% 기준입니다\n")
def start():
    while True:
        if keyboard.is_pressed('F3'):
            m.click(point3[0],point3[1])
            m.click(point4[0],point4[1])
            time.sleep(1)
            m.typewrite("r")
        if keyboard.is_pressed('/'):
            return        

while True:
    start()
    time.sleep(0.5)
    while True:
        if keyboard.is_pressed('/'):
            time.sleep(0.5)
            break
    # pip install pyautogui
    # pip3 install keyboard
    # pip install mouse    
