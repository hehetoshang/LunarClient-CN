# 修改游戏标题至Lunar Client CN (版本号)
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
    "do /g join AllForLove, MTL are Losers",
    "LC-CN原作者为chenmy1903也就是CubeWhy!",
    "LC-CN只在GitHub上面发布",
    "你知道乔博远是跑路主播吗?",
    "qby love hyc<3",
    "诶哟~嘿~",
    "QiaoBoYuanL died :(",
    "小黑板你得改密码啊,你号都被盗了",
    "小黑板树脂666我们都叫他乔博远,就他叫他小黑板",
    "傻逼乔博远想想别人为什么不去你工会而来我们AFL",
    "Title changed by rename_window.py!",
    "[Loser XiaoHeiPa] 差点忘了自己是来打飞机的了",
    "Buy iqbooster?",
    "MTL会长 XiaoHeiPa 实名乔博远",
    "你知道吗, SadAndSmlie是卧底!",
    "看到他的名字，他先是身体一颤，眼睛中闪过了一丝光亮，但是很快又黯淡了下去。他就坐在马桶上，就那样一直坐着。许久，他终于决定说点什么：“妈，我在直播！”"
    "ILY<3",
    "github.com/XiaoHeiPa - 乔博远Official GitHub!",
    "Sub to 兰方翔Official on bilibili!",
    "huanmeng_LLL: You are banned.",
] + (["Pls a rank because today is 11/6!"] if (time_now.tm_mday == 6 and time_now.tm_mon == 11) else [])

old_title = ""
inited = False

def set_title():
    global old_title, inited
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
            win32api.SendMessage(window, win32con.WM_SETTEXT,0,"Lunar Client CN" + old_title.replace("Lunar Client", "") + " | " + motd)
            return True
    if inited:
        sys.exit()


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
