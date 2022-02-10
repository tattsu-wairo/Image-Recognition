import tkinter
import threading
import pyautogui
import time
import json
import os

start_flag = False
quitting_flag = False
count = 0

prtsc_x = 220
prtsc_y = 610
prtsc_width = 250
prtsc_height = 50
prtsc_range = (prtsc_x, prtsc_y, prtsc_width, prtsc_height)
sample_image='test.png'
json_file='setting.json'

sleep_time = 4

def read_json():
    global count
    if os.path.isfile(json_file):
        with open(json_file) as f:
            data = json.load(f)
            count=data['count']
            return count

def write_json(number):
    if os.path.isfile(json_file):
        with open(json_file) as f:
            data = json.load(f)
        data['count']=number
        with open(json_file,"w",encoding='utf-8') as f:
            json.dump(data,f,indent=4,ensure_ascii=False)

def counter():
    """カウンター"""
    global label
    global start_flag
    global quitting_flag
    global count

    count = read_json()
    label.config(text=count)
    while not quitting_flag:
        if start_flag:
            try:
                x, y = pyautogui.locateCenterOnScreen(
                    sample_image, region=prtsc_range)
                count += 1
                label.config(text=count)
                time.sleep(sleep_time)
            except:
                pass


# スタートボタンが押された時の処理
def start_button_click(event):
    global start_flag
    global count

    #count=read_json()
    start_flag = True


# ストップボタンが押された時の処理
def stop_button_click(event):
    global start_flag
    start_flag = False

# スクショボタンが押された時の処理
def screenshot_button_click(event):
    pyautogui.screenshot(sample_image, region=prtsc_range)

# 終了ボタンが押された時の処理
def quit_app():
    global quitting_flag
    global app
    global thread1

    quitting_flag = True

    # thread1終了まで待つ
    thread1.join()
    write_json(count)

    # thread1終了後にアプリ終了
    app.destroy()


# メインウィンドウを作成
app = tkinter.Tk()
app.geometry("200x200")

# ボタンの作成と配置
start_button = tkinter.Button(
    app,
    text="スタート",
)
start_button.pack()

stop_button = tkinter.Button(
    app,
    text="ストップ",
)
stop_button.pack()

screenshot_button = tkinter.Button(
    app,
    text="スクショ",
)
screenshot_button.pack()


# ラベルの作成と配置
label = tkinter.Label(
    app,
    width=7,
    height=2,
    text=0,
    font=("", 50)
)
label.pack()

# イベント処理の設定
start_button.bind("<ButtonPress>", start_button_click)
stop_button.bind("<ButtonPress>", stop_button_click)
screenshot_button.bind("<ButtonPress>",screenshot_button_click)
app.protocol("WM_DELETE_WINDOW", quit_app)

# スレッドの生成と開始
thread1 = threading.Thread(target=counter)
thread1.start()

# メインループ
app.mainloop()
