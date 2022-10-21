# 修改游戏标题至Lunar Client CN (版本号)
# import os
import random
import time
# import json
import win32api
import win32gui
import win32con   

time_now = time.localtime(time.time())

motds = [
    "do /g join AllForLove, MTL are Losers",
    "LC-CN原作者为chenmy1903也就是CubeWhy!",
    "LC-CN只在GitHub上面发布",
    "你知道乔博远是跑路主播吗?",
    "ILY<3",
    "huanmeng_LLL: You are banned.",
] + (["Pls a rank because today is 11/7!"] if (time_now.tm_mday == 7 and time_now.tm_mon == 11) else [])

old_title = ""

def set_title():
    global old_title
    windows_list = []
    win32gui.EnumWindows(lambda hWnd, param: param.append(hWnd), windows_list)
    for window in windows_list:
        # classname = win32gui.GetClassName(window)
        title: str = win32gui.GetWindowText(window)
        # print(f'classname:{classname} title:{title}')
        if "Lunar Client" in title:
            if old_title == "":
                old_title = title
            motd = random.choice(motds)
            win32api.SendMessage(window,win32con.WM_SETTEXT,0,"Lunar Client CN" + old_title.replace("Lunar Client", "") + " | " + motd)
            return True


def main():
    while True:
        if set_title():
            print("成功初始化标题!")
            break
        time.sleep(5)
    while True:
        set_title()
        time.sleep(50)

if __name__ == "__main__":
    main()
