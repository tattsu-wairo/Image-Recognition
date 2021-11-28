import tkinter
import json
import os
import time

count = 0
hour=0
minute=0
second=0
command_id=0
timer_flag=False

json_file='setting.json'

def read_json(data_name):
    global count
    if os.path.isfile(json_file):
        with open(json_file) as f:
            data = json.load(f)
            return data[data_name]

def write_json(data_name,number):
    if os.path.isfile(json_file):
        with open(json_file) as f:
            data = json.load(f)
        data[data_name]=number
        with open(json_file,"w",encoding='utf-8') as f:
            json.dump(data,f,indent=4,ensure_ascii=False)

# スタート＆ストップボタンが押された時の処理
def start_button_click(event):
    global timer_flag
    print(event.widget.cget('text'))
    if not timer_flag:
        timer()
        timer_flag=True

# タイマーリセットボタンが押された時の処理
def timer_reset_button_click(event):
    global timer_flag
    if timer_flag:
        timer_flag=False
        app.after_cancel(command_id)

#　スペースキーが押されたとき
def callback(event):
    global count
    count+=1
    count_label["text"]=f"リセット回数：{count}"
    write_json("count",count)

# リセットボタンが押された時の処理
def reset_button_click(event):
    global count
    count=0
    count_label["text"]=f"リセット回数：{count}"
    write_json("count",count)

# 終了ボタンが押された時の処理
def quit_app():
    global app
    write_json("count",count)
    # thread1終了後にアプリ終了
    app.destroy()

#　時間計測機能
def timer():
    global command_id
    global second
    global minute
    global hour
    command_id=app.after(1000,timer)
    if timer_flag:
        if second==59:
            second=0
            minute+=1
        else:
            second+=1
        if minute>59:
            minute=0
            hour+=1
        else:
            pass
        timer_label["text"]=f"{hour}時間{minute}分{second}秒"
        write_json("hour",hour)
        write_json("minute",minute)
        write_json("second",second)
        print(f"{hour}時間{minute}分{second}秒")


# メインウィンドウを作成
app = tkinter.Tk()
app.geometry("300x300")
app.configure(bg='green')
count=read_json("count")
hour=read_json("hour")
minute=read_json("minute")
second=read_json("second")

# ボタンの作成と配置
reset_button = tkinter.Button(
    app,
    text="リセット",
)
reset_button.pack()

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

# ラベルの作成と配置
count_label = tkinter.Label(
    app,
    width=20,
    height=2,
    text=f"リセット回数：{count}",
    font=("", 30),
    background='green'
)
count_label.pack()

timer_label = tkinter.Label(
    app,
    width=20,
    height=2,
    text=f"{hour}時間{minute}分{second}秒",
    font=("", 30),
    background='green'
)
timer_label.pack()

# イベント処理の設定
reset_button.bind("<ButtonPress>", reset_button_click)
start_button.bind("<ButtonPress>", start_button_click)
stop_button.bind("<ButtonPress>", timer_reset_button_click)
app.bind('<space>',callback)
app.protocol("WM_DELETE_WINDOW", quit_app)


# メインループ
app.mainloop()