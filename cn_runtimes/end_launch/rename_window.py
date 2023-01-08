# 修改游戏标题至Lunar Client CN (版本号) | Motd
# import os
import random
import sys
import time
# import json
import win32api
import win32gui
import win32con   

time_now = time.localtime(time.time())

motds = [
    "LC-CN原作者为chenmy1903也就是CubeWhy!",
    "LC-CN只在GitHub上面发布",
    "qby love hyc<3",
    "诶哟~嘿~",
    "sub to 咸鱼SaltyFish in bilibili",
    # "QiaoBoYuanL died :(",
    "小黑板你得改密码啊,你号都被盗了",
    "Title changed by rename_window.py!",
    # "[XiaoHeiPa] 差点忘了自己是来打飞机的了",
    "Buy iqbooster?",
    "看到他的名字，他先是身体一颤，眼睛中闪过了一丝光亮，但是很快又黯淡了下去。他就坐在马桶上，就那样一直坐着。许久，他终于决定说点什么：“妈，我在直播！”",
    "ILY<3",
    "github.com/XiaoHeiPa - XiaoHeiPa Official GitHub!",
    "Sub to 兰方翔Official on bilibili!",
] + (["Pls a rank because today is 11/7!", "Pls duel XiaoHeiPa for a free rank!", "Happy birthday XiaoHeiPa <3"] if (time_now.tm_mday == 7 and time_now.tm_mon == 11) else []) + \
    (["Happy birthday CubeWhy <3", "do /gift CubeWhy plz LOL", "Sub to CubeWhy on Bilibili today bcz it's he's birthday?"] if (time_now.tm_mday == 21 and time_now.tm_mon == 12) else []) + \
        (["I love cym forever <3"] if (time_now.tm_mday == 7 and time_now.tm_mon == 2) else []) + \
            (["Happy new year"] if (time_now.tm_mday == 1 and time_now.tm_mon == 1) else [])

old_title = ""
inited = False
s_count = 0

def set_title():
    global old_title, inited, s_count
    windows_list = []
    win32gui.EnumWindows(lambda hWnd, param: param.append(hWnd), windows_list)
    for window in windows_list:
        classname = win32gui.GetClassName(window)
        title: str = win32gui.GetWindowText(window)
        if "Lunar Client" in title and classname == "LWJGL":
                inited = True
                s_count += 1
                print("成功定位游戏窗口! [x{}]".format(s_count), end="\r")
                if old_title == "":
                    old_title = title
                motd = random.choice(motds)
                win32api.SendMessage(window, win32con.WM_SETTEXT,0,"Lunar Client CN" + old_title.replace("Lunar Client", "") + " | " + motd)
                return True
    if inited:
        print("\n无法寻找到游戏窗口!结束进程!")
        sys.exit()


def main():
    print("正在寻找窗口...")
    falled_count = 0
    while True:
        if set_title():
            print("成功初始化标题!")
            break
        time.sleep(5)
        falled_count += 1
        if falled_count >= 20:
            print("游戏崩溃或故意启动此文件, 退出程序!")
            sys.exit()
        print("未找到...尝试重新查找... [x{}]".format(falled_count), end="\r")
    print("\nRandom title toggled!")
    while True:
        set_title()
        time.sleep(10)

if __name__ == "__main__":
    main()
