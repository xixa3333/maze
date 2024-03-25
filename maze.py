from tkinter import *
from functools import partial
import random
from random import randint as rand
import os

# 創建Tkinter窗口
root = Tk()
root.title("迷宮")

# 初始化變數
game_screen_icon = []
scope = []
Map = []
X = 1
Y = 1
victory_or_defeat = StringVar()
victory_or_defeat.set('')
portal = 0
size = 0
mode = 0
transmit_flag = 0
perspective_flag = 0
mallet_flag = 0
number_of_mallets = 0
mallet = 0
Number_of_props = StringVar()
Number_of_props.set('槌子x' + str(number_of_mallets))
perspective = None
vision=1


# 輸入視野大小，檢查是否是正整數且為1-2
def field_of_view_size():
    while True:
        try:
            vision = int(input('請輸入你的視野大小(1-4): '))
            if vision not in [1, 2,3,4]:
                print("視野大小要為1-4。")
            else:
                return vision
        except ValueError:
            print("視野大小要為1-4。")
# 輸入地圖大小，檢查是否是正整數且至少為vision*2+1
def get_map_size(vision):
    while True:
        try:
            size = int(input('請輸入你的地圖大小(生成正方形地圖)(數字要'+str(vision*2+1)+'或以上): '))
            if size < vision*2+1:
                print("地圖大小至少數字要"+str(vision*2+1)+"或以上。")
            else:
                return size
        except ValueError:
            print("請輸入一個正整數。")
# 輸入難易度，檢查是否是1、2、3、4中的一個數字
def get_difficulty():
    while True:
        try:
            mode = int(input('選擇你的難易度(1)(2)(3)(4): '))
            if mode not in [1, 2, 3, 4]:
                print("請輸入1、2、3或4中的一個數字。")
            else:
                return mode
        except ValueError:
            print("請輸入1、2、3或4中的一個數字。")

# 輸入是否開啟傳送門模式
def get_portal_mode():
    while True:
        try:
            portal = int(input('要開傳送門模式嗎(1/0): '))
            if portal not in [0, 1]:
                print("請輸入0或1。")
            else:
                return portal
        except ValueError:
            print("請輸入0或1。")

# 輸入是否要槌子道具
def get_mallet():
    while True:
        try:
            mallet = int(input('要槌子道具嗎(1/0): '))
            if mallet not in [0, 1]:
                print("請輸入0或1。")
            else:
                return mallet
        except ValueError:
            print("請輸入0或1。")
def input_map_info():
    vision = field_of_view_size()
    size = get_map_size(vision)
    mode = get_difficulty()
    portal = 0
    if mode != 1:
        portal = get_portal_mode()
    mallet = get_mallet()
    return size+2, mode, portal, mallet,vision

# 主函數中調用 input_map_info 來獲取用戶輸入


    

# 建立地圖
def map_creation():
    global Map, X, Y, number_of_mallets
    Xrand = rand(2, size - 2)
    Yrand = rand(2, size - 2)
    
    # 初始化地圖
    for i in range(0, size):
        Map.append([''] * size)
    for i in range(0, size):
        Map[i][0] = '|'
        Map[i][size - 1] = '|'
        Map[size - 1][size - i - 1] = '_'
        Map[0][i] = '_'
    
    # 創建傳送門
    if portal == 1:
        Map[2][2] = '●'
        Map[2][size - 3] = '●'
        Map[size - 3][2] = '●'
        Map[size - 3][size - 3] = '●'
    
    # 根據難度設置起點和終點
    if mode == 1:
        Map[Y][X] = 'O'
        Map[Y][X + 1] = '-'
        Map[size - 2][size - 2] = '㊣'
        Map[size - 2][size - 2 - 1] = '-'
    elif mode == 2:
        Map[Y][X] = 'O'
        Map[Y][X + 1] = '-'
        while Map[Yrand][Xrand] != '':
            Xrand = rand(2, size - 2)
            Yrand = rand(2, size - 2)
        Map[Yrand][Xrand] = '㊣'
    elif mode == 3 or mode == 4:
        while Map[Yrand][Xrand] != '':
            Xrand = rand(2, size - 2)
            Yrand = rand(2, size - 2)
        X = Xrand
        Y = Yrand
        Map[Y][X] = 'O'
        while Map[Yrand][Xrand] != '':
            Xrand = rand(2, size - 2)
            Yrand = rand(2, size - 2)
        Map[Yrand][Xrand] = '㊣'
    
    # 創建障礙物和道具
    if mallet == 1:
        number_of_mallets += 1
        Number_of_props.set('槌子x' + str(number_of_mallets))
        for _ in range(0, int(size / 10), 1):
            while Map[Yrand][Xrand] != '':
                Xrand = rand(2, size - 2)
                Yrand = rand(2, size - 2)
            Map[Yrand][Xrand] = '╤'
    
    for i in range(1, size - 1):
        for j in range(i % 2 + 1, size - 1, 2):
            Obstacle = rand(0, 1)
            if Obstacle == 1 and Map[i][j] == '':
                Map[i][j] = 'X'
    
    for i in range(1, size - 1):
        for j in range(1, size - 1):
            if Map[i][j] == '':
                Map[i][j] = '-'


    
#前端設置
def frontend_settings():
    global game_screen_icon,scope, perspective,root
    root.geometry(str(100+150*vision)+"x"+str(500+110*vision)+"+800+90")
    for item in root.winfo_children():
      item.destroy()
    scope=[]
    game_screen_icon = []
    #上方設置
    upper_end = Frame(bg="yellow")
    upper_end.grid(row=0, column=0, rowspan=2, columnspan=vision*2+1)

    mallet_mode = Button(upper_end, text='使用槌子', width=7, height=2, command=partial(control_character, 'Mallet'))
    mallet_mode.grid(row=0, column=vision-1)
    reset = Button(upper_end, text='重置', width=7, height=2, command=partial(control_character, 'reset'))
    reset.grid(row=0, column=vision)
    number_of_props_label = Label(upper_end, textvariable=Number_of_props, width=7, height=2, bg="yellow")
    number_of_props_label.grid(row=0, column=vision+1)
    victory_or_defeat_label = Label(upper_end, textvariable=victory_or_defeat, height=2, bg="yellow", fg="red", font=('Arial', 15, 'bold'))
    victory_or_defeat_label.grid(row=1, column=0, columnspan=vision*2+1)

    #遊戲畫面設置
    game_screen = Frame(bg="orange", bd=10, relief=SUNKEN)
    game_screen.grid(row=2, column=vision-1, rowspan=3, columnspan=3)
    Y_min_out_of_range = Y - vision if Y - vision >= 0 else 0
    X_min_out_of_range = X - vision if X - vision >= 0 else 0
    Y_max_out_of_range = Y_min_out_of_range + vision*2+1 if Y_min_out_of_range + vision*2+1 <size else size
    X_max_out_of_range = X_min_out_of_range + vision*2+1 if X_min_out_of_range + vision*2+1 <size else size
    for i in range(Y_min_out_of_range-(Y_min_out_of_range + vision*2+1-Y_max_out_of_range), Y_max_out_of_range):
        game_screen_icon.append([StringVar() for _ in range(vision*2+1)])
        scope.append([None] * (vision*2+1))
        for j in range(X_min_out_of_range-(X_min_out_of_range + vision*2+1-X_max_out_of_range), X_max_out_of_range):
            scope[i - Y_min_out_of_range+(Y_min_out_of_range + vision*2+1-Y_max_out_of_range)][j - X_min_out_of_range+(X_min_out_of_range + vision*2+1-X_max_out_of_range)] = Label(game_screen, textvariable=game_screen_icon[i - Y_min_out_of_range][j - X_min_out_of_range], width=7, height=3)
            scope[i - Y_min_out_of_range+(Y_min_out_of_range + vision*2+1-Y_max_out_of_range)][j - X_min_out_of_range+(X_min_out_of_range + vision*2+1-X_max_out_of_range)].grid(row=i - Y_min_out_of_range + 2, column=j - X_min_out_of_range)
            game_screen_icon[i - Y_min_out_of_range+(Y_min_out_of_range + vision*2+1-Y_max_out_of_range)][j - X_min_out_of_range+(X_min_out_of_range + vision*2+1-X_max_out_of_range)].set(Map[i][j])

    #遊戲按鍵設置
    game_button = Frame(bg="blue")
    game_button.grid(row=4+vision*2+1, column=0, rowspan=3, columnspan=vision*2+1)
    
    up = Button(game_button, text='↑', width=7, height=3, command=partial(control_character, 'up'))
    up.grid(row=4+vision*2+1, column=vision)
    left = Button(game_button, text='←', width=7, height=3, command=partial(control_character, 'left'))
    left.grid(row=4+vision*2+1+1, column=vision-1)
    perspective = Button(game_button, text='第三視角', width=7, height=3, command=partial(control_character, 'Thirdperspective'))
    perspective.grid(row=4+vision*2+1+1, column=vision)
    right = Button(game_button, text='→', width=7, height=3, command=partial(control_character, 'right'))
    right.grid(row=4+vision*2+1+1, column=vision+1)
    down = Button(game_button, text='↓', width=7, height=3, command=partial(control_character, 'down'))
    down.grid(row=4+vision*2+1+2, column=vision)



# 移動角色的函數，根據方向更新角色位置和地圖狀態
def control_character(direction):
    global X, Y, perspective_flag, transmit_flag, mallet_flag, number_of_mallets,size, mode, portal, mallet,vision
    # 如果角色往上移動且移動方向上不是障礙物或者有槌子道具可使用，並且不是邊界
    if direction == 'up' and (Map[Y - 1][X] != 'X' or (mallet_flag == 1 and number_of_mallets > 0)) and Map[Y - 1][X] != '_':
        # 如果使用了槌子道具，則消耗一個槌子
        if mallet_flag == 1 and Map[Y - 1][X] == 'X' and number_of_mallets > 0:
            number_of_mallets -= 1
            Number_of_props.set('槌子x' + str(number_of_mallets))            
        Y -= 1  # 更新Y座標
        # 如果移動到的位置是傳送門，則更新相應的地圖狀態
        if Map[Y][X] == '●':
            Map[Y + 1][X] = '-'  # 上一個位置變為空格
            # 判斷傳送門的方向並更新Y座標
            if Y == 2:
                Y = size - 3
            else:
                Y = 2
            transmit_flag = 1  # 設置傳送標誌為1
        else:
            if transmit_flag == 0:
                Map[Y + 1][X] = '-'  # 上一個位置為空格
            else:
                Map[Y + 1][X] = '●'  # 上一個位置變為傳送門
                transmit_flag = 0  # 設置傳送標誌為0
        move()  # 更新角色位置和地圖
    # 同理，處理其他方向的移動情況
    elif direction == 'down' and (Map[Y + 1][X] != 'X' or (mallet_flag == 1 and number_of_mallets > 0)) and Map[Y + 1][X] != '_':
        if mallet_flag == 1 and Map[Y + 1][X] == 'X' and number_of_mallets > 0:
            number_of_mallets -= 1
            Number_of_props.set('槌子x' + str(number_of_mallets))  
        Y += 1
        if Map[Y][X] == '●':
            Map[Y - 1][X] = '-'
            if Y == 2:
                Y = size - 3
            else:
                Y = 2
            transmit_flag = 1
        else:
            if transmit_flag == 0:
                Map[Y - 1][X] = '-'
            else:
                Map[Y - 1][X] = '●'
                transmit_flag = 0
        move()
    elif direction == 'left' and (Map[Y][X - 1] != 'X' or (mallet_flag == 1 and number_of_mallets > 0)) and Map[Y][X - 1] != '|':
        if mallet_flag == 1 and Map[Y][X - 1] == 'X' and number_of_mallets > 0:
            number_of_mallets -= 1
            Number_of_props.set('槌子x' + str(number_of_mallets))  
        X -= 1
        if Map[Y][X] == '●':
            Map[Y][X + 1] = '-'
            if X == 2:
                X = size - 3
            else:
                X = 2
            transmit_flag = 1
        else:
            if transmit_flag == 0:
                Map[Y][X + 1] = '-'
            else:
                Map[Y][X + 1] = '●'
                transmit_flag = 0
        move()
    elif direction == 'right' and (Map[Y][X + 1] != 'X' or (mallet_flag == 1 and number_of_mallets > 0)) and Map[Y][X + 1] != '|':
        if mallet_flag == 1 and Map[Y][X + 1] == 'X' and number_of_mallets > 0:
            number_of_mallets -= 1
            Number_of_props.set('槌子x' + str(number_of_mallets))  
        X += 1
        if Map[Y][X] == '●':
            Map[Y][X - 1] = '-'
            if X == 2:
                X = size - 3
            else:
                X = 2
            transmit_flag = 1
        else:
            if transmit_flag == 0:
                Map[Y][X - 1] = '-'
            else:
                Map[Y][X - 1] = '●'
                transmit_flag = 0
        move()
    elif direction == 'Thirdperspective':  # 控制第三視角的開關
        perspective_flag = (perspective_flag + 1) % 2
        if perspective_flag == 1:
            os.system('cls')
            print('第三視角開啟')
            for i in range(1, size - 1):
                for j in range(1, size - 1):
                    print(Map[i][j], end=" ")
                print('\n')
            print('\n')
            if mode == 4:
                perspective.config(state="disabled")  # 若為難度4，則禁用第三視角按鈕
                perspective_flag = 0
        else:
            os.system('cls')
            print('第三視角關閉')
    elif direction == 'Mallet':  # 控制槌子道具的開關
        mallet_flag = (mallet_flag + 1) % 2
        if mallet_flag == 1:
            print('開始使用槌子，再按一次此按鈕可關閉')
        else:
            print('取消使用槌子')
    elif direction == 'reset':  # 控制遊戲重置
        remake_parameters() # 重置遊戲參數
        size, mode, portal, mallet,vision = input_map_info()  # 重新輸入地圖
        map_creation()
        frontend_settings()
        root.mainloop()


# 移動角色
def move():
    global number_of_mallets
    if Map[Y][X] == '㊣':
        victory_or_defeat.set('win')
    elif Map[Y][X] == '╤':
        number_of_mallets += 1
        Number_of_props.set('槌子x' + str(number_of_mallets))
    Map[Y][X] = 'O'
    #視野
    Y_min_out_of_range = Y - vision if Y - vision >= 0 else 0
    X_min_out_of_range = X - vision if X - vision >= 0 else 0
    Y_max_out_of_range = Y_min_out_of_range + vision*2+1 if Y_min_out_of_range + vision*2+1 <size else size
    X_max_out_of_range = X_min_out_of_range + vision*2+1 if X_min_out_of_range + vision*2+1 <size else size
    for i in range(Y_min_out_of_range-(Y_min_out_of_range + vision*2+1-Y_max_out_of_range), Y_max_out_of_range):
        for j in range(X_min_out_of_range-(X_min_out_of_range + vision*2+1-X_max_out_of_range), X_max_out_of_range):
            game_screen_icon[i - Y_min_out_of_range+(Y_min_out_of_range + vision*2+1-Y_max_out_of_range)][j - X_min_out_of_range+(X_min_out_of_range + vision*2+1-X_max_out_of_range)].set(Map[i][j])
    if perspective_flag == 1:
        os.system('cls')
        for i in range(1, size - 1):
            for j in range(1, size - 1):
                print(Map[i][j], end=" ")
            print('\n')
        print('\n')







# 重置遊戲
def remake_parameters():
    global Map, X, Y, victory_or_defeat, portal, perspective_flag, transmit_flag, mallet_flag, number_of_mallets, mallet, Number_of_props, perspective,vision
    os.system('cls')
    Map = []
    X = 1
    Y = 1
    victory_or_defeat.set('')
    portal = 0
    transmit_flag = 0
    perspective_flag = 0
    mallet_flag = 0
    number_of_mallets = 0
    mallet = 0
    vision=1
    perspective.config(state="normal")
    Number_of_props.set('槌子x' + str(number_of_mallets))
    


        

def main():
    global size, mode, mallet, portal,vision

    # 打印遊戲說明和提示
    print("歡迎來到迷宮遊戲！")
    print("O是你的位置，X是障礙物過不去，㊣是終點，●是傳送門，╤是槌子，-是路，|跟_是邊界")
    print("在遊戲中，你可以使用 ↑、↓、←、→ 分別來控制上、下、左、右移動。")
    print("第三視角可以看地圖\n")
    print("槌子可以破障礙物\n")
    print("難易度說明：")
    print("難易度1時你在左上角，終點在右下角")
    print("難易度2時你在左上角，終點隨機")
    print("難易度3時你隨機，終點隨機")
    print("難易度4時你隨機，終點隨機，且只能看一次地圖\n")
    print("傳送門模式：\n四周有傳送門，從左上傳送門上往下進入傳送門會傳到左下傳送門，從左上傳送門左往右進入傳送門會傳到右上傳送門")
    print("\n注意自己或終點或傳送門可能會被障礙物完全擋住，小心")
    print("準備好了嗎？讓我們開始吧！\n")

    # 輸入地圖相關設定
    size, mode, portal, mallet,vision = input_map_info()
    map_creation()
    
    # 前端設置
    frontend_settings()
    
    root.mainloop()

main()


