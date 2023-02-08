# encoding: UTF-8
import json
import os
import sys
import threading
import webbrowser
import requests
import psutil
import configparser

import zipfile

from PyQt5.QtWidgets import QApplication, QMessageBox

__version__ = "v2.11.2-fix19"

PRE_VERSION = False

# ----
SKIP_CRACK_UPDATE = False
SKIP_CRACK_UPDATE = PRE_VERSION
# ----

# time.sleep(114514) # Anti 张子曦L

LATEST_VERSION_URL = "https://github.com/CubeWhyMC/LunarClient-CN/releases"
LATEST_VERSION = __version__

if not SKIP_CRACK_UPDATE:
    try:
        fast_link = "https://github.com/"
        update_link = "CubeWhyMC/lunarclient-cn/releases/latest"

        LATEST_VERSION_URL = "https://github.com/" + "/".join(requests.get(fast_link + update_link, timeout=5).url.split("/")[3:])
        LATEST_VERSION = LATEST_VERSION_URL.split("/")[-1]
    except Exception as e:
        SKIP_CRACK_UPDATE = True

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CLIENT_DIR = os.path.dirname(BASE_DIR)

run_in_pyw = sys.executable.replace("\\", "/").split("/")[-1] in ["pyw.exe", "pythonw.exe"]

def show_cmd_alert(msg: str):
    r_msg = msg.replace("\n", "\\n") + "\n如果你无法解决此问题, 请去找zzxMinecraft (张子曦MC) !"
    os.system(f"start \"LunarClient-CN\" \"{os.path.join(sys.exec_prefix, 'python.exe')}\" -c \"print('{r_msg}'.replace('\\\\n', '\\n'));input('按Enter退出此窗口')\"")

def anti_lowiq() -> bool:
    cwd = os.getcwd()
    if " " in cwd:
        show_cmd_alert("目录中不能包含空格!请将LunarClient CN的文件夹移动到桌面上!")
        return False
    # for path in os.environ["path"]:
    #     if os.path.isfile(os.path.join(path, "qwindows.dll")):
    #         break
    # else:
    #     show_cmd_alert("请使用launchlc.bat启动LunarClient CN或手动下载qt-runtime\nqt-runtime download: https://chenmy1903.lanzoum.com/iXPPM0lodtzi\n将4个dll解压到C:/Windows文件夹里边即可")
    #     return False
    return True

def get_banned():
    blacklist = []
    try:
        r = requests.get("https://chenmy1903.github.io/LunarClient-CN/blacklist.json", proxies={'http': None, 'https': None}) # 防止被抓包软件重定向
        blacklist = json.loads(r.text)
    except:
        print("封禁列表获取失败")
    return blacklist

def account_in_black_list(bl):
    f = os.path.join(os.path.expanduser("~"), ".lunarclient", "settings", "game", "accounts.json")
    with open(f, "r", encoding="utf-8") as f_r:
        j = json.load(f_r)
    accounts: dict = j["accounts"]
    c: dict
    for c in accounts.values():
        user_uuid = c["minecraftProfile"]["id"]
        if user_uuid in ["ee0d0448641e405a96ba242c92845d85", "ec8e77dcb178476088912ee208111cc3"]:
            return False, ""
        if user_uuid in bl:
            return True, bl[user_uuid], user_uuid, c["minecraftProfile"]["name"]
    return False, ""

def get_java_agents():
    jagents_dir = os.path.join(os.path.dirname(BASE_DIR), "javaagents")
    agents_path = []
    if not os.path.isdir(jagents_dir):
        return []
    init_agent = False
    for f in os.listdir(jagents_dir):
        if f.endswith(".jar"):
            cfg = configparser.ConfigParser()
            agent_config = os.path.join(jagents_dir, f + ".ini")
            if not os.path.isfile(agent_config):
                init_agent = True
            cfg_file = os.path.join(agent_config)
            cfg.read(cfg_file)
            cfg.add_section("cnclient") if not cfg.has_section("cnclient") else ""
            cfg.set("cnclient", "args", "") if not cfg.has_option("cnclient", "args") else ""
            with open(cfg_file, "w") as fr:
                cfg.write(fr)
            try:
                arg = cfg["cnclient"]["args"]
            except configparser.NoSectionError: 
                QMessageBox.critical(None, "LC-CnLauncher", "加载Java助理配置时出现错误\n文件: {}\n删除此文件可能会解决问题。\n点击确定跳过加载此Jar".format(cfg_file))
                continue
            agents_path.append("-javaagent:\"" + os.path.join(jagents_dir, f) + "\"" + (("=\"" + arg + "\"") if arg != "" else ""))
    if init_agent:
        QMessageBox.information(None, "Lunar Client CN", "新的JavaAgents配置文件已经添加!\n请调整参数然后点击确认来启动游戏!")
        return get_java_agents()
    return agents_path

def end_launch():
    add_f = os.path.join(os.path.join(BASE_DIR, "end_launch"))
    for py_file in os.listdir(add_f):
        os.system("start \"Lunar Client CN\" " + "\"" + sys.executable + "\" " + os.path.join(add_f, py_file))

def launchclient(arg):
    exitcode = os.system("start \"Lunar Client CN\" " + arg)
    sys.exit(exitcode)

term = """主播你好, 请你看完这个再去问LowIQ问题
1. 如果游戏长时间不启动, 请检查后台是否有进程
2. 请将LunarClient CN文件夹放到没空格/中文的路径, 并使用bat启动
3. 帮助网址lunarcn.top/faq/index.html请先看这个再问问题
4. 带空格的路径的应该启动不了, 我没测试, 你可以测试一下
====
此版本更新内容
1. 去除封禁
2. 修复存档目录的空格bug
3. 修复中文目录问题(未测试)
====
点击Yes启动游戏, 且此提示在下次更新之前不再弹出。
"""

def pop_tip_of_first_launch():
    return QMessageBox.question(None, "Lunar Client-CN", term) == QMessageBox.Yes


cnclient = os.path.join(os.path.expanduser("~"), ".lunarclient", "cnclient")


def update_lunarcn():
    source_code = "https://github.com/chenmy1903/LunarClient-CN/archive/refs/tags/" + LATEST_VERSION + ".zip"
    white_list = ["java-runtime", "javaagents", "python"]
    launcher = os.path.join(CLIENT_DIR, "Lunar Client CN.exe")
    anti_lowiq = launcher + ".LunarCN正在更新不要启动启动器不要关电脑请等待更新完成.LowIQ"
    upd_temp = os.path.join(os.path.expanduser("~"), "cnclient", "auto-update")
    if not os.path.isdir(upd_temp):
        os.makedirs(upd_temp)
    update_file = os.path.join(upd_temp, LATEST_VERSION + ".zip")
    try:
        r = requests.get(source_code, headers={"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5 (.NET CLR 3.5.30729)"})
        with open(update_file, "wb") as f:
            f.write(r.raw)
        if os.path.isfile(launcher):
            os.rename(launcher, anti_lowiq) # Anti LowIQ
        for upd in os.listdir(CLIENT_DIR):
            if upd not in white_list: # Remove source from LunarCN
                need_upd = os.path.join(CLIENT_DIR, upd)
                if os.path.isdir(need_upd):
                    os.removedirs(need_upd)
                elif os.path.isfile(need_upd):
                    os.remove(need_upd)
        z = zipfile.ZipFile(update_file)
        z.extractall(upd_temp)
        new_files = os.path.join(upd_temp, LATEST_VERSION)
        for upd_file in os.listdir(new_files):
            os.rename(os.path.join(new_files, upd_file), os.path.join(CLIENT_DIR, upd_file))
    except Exception as e:
        print(e)
        QMessageBox.critical(None, "Lunar Client CN AutoUpdate", "自动更新失败,请使用Steam++或其他加速器软件或手动更新!")
    else:
        QMessageBox.information(None, "Lunar Client CN AutoUpdate", "LunarCN更新完成")
    finally:
        if os.path.isfile(anti_lowiq):
            os.rename(anti_lowiq, launcher) # Update done

ban_end = """主播我建议你想想自己为啥被ban
"""
reason = "No reason"

def main():
    print("启动Lunar Client!")
    if not anti_lowiq():
        return # 张子曦LowIQ检测
    # blacklist = get_banned()
    # fix19 移除封禁
    # banned = account_in_black_list(blacklist)
    app = QApplication([sys.executable])
    # if banned[0]:
    #     for pid in psutil.pids():
    #         try:
    #             p = psutil.Process(pid)
    #             if p.exe().endswith("javaw.exe") or p.exe().endswith("java.exe") or p.exe().endswith("Lunar Client CN.exe") or p.exe().endswith("Lunar Client.exe"):
    #                 p.kill()
    #         except:
    #             pass
    #     reason = banned[1]["reason"] if "reason" in banned[1] else reason
    #     ban_end = banned[1]["ban_end"] if "ban_end" in banned[1] else ban_end
    #     u_id = banned[2]
    #     u_nick = banned[3]
    #     QMessageBox.critical(None, "LunarClient-CN ban", "你的lc-cn账户已被封禁~\n申诉/购买unban加QQ -> 2834886052 <-\nPlayer: {}\nUUID: {}\n原因: {}\n{}\n{}\n{}".format(u_nick, u_id, reason, len(ban_end) * "-", ban_end, len(ban_end) * "-"))
    #     sys.exit()
    if not os.path.isdir(cnclient):
        os.makedirs(cnclient)
    At = os.path.join(cnclient, "AcceptedTerm")
    first_launch = not os.path.isfile(At)
    if LATEST_VERSION != __version__ and not SKIP_CRACK_UPDATE:
        if QMessageBox.question(None, "Lunar Client CN AutoUpdate", "你的LC-CN需要更新!\n当前版本: {}\n最新版本: {}\n点击确定则更新(点击取消退出LC-CN)\n{}".format(__version__, LATEST_VERSION, LATEST_VERSION_URL)) == QMessageBox.Yes:
            webbrowser.open(LATEST_VERSION_URL)
            # update_lunarcn()
        sys.exit()
    if not first_launch:
        with open(At, "r") as f:
            if __version__ not in f.read():
                first_launch = True
    if first_launch:
        if not pop_tip_of_first_launch():
            return
        with open(At, "w") as f:
            f.write(__version__)
    java = os.path.join(os.path.dirname(BASE_DIR), "java-runtime", "bin", "javaw.exe" if run_in_pyw else "java.exe")
    java_agents = get_java_agents()
    launch_arg = "\"" + java + "\" " + " ".join(java_agents) + " " + " ".join(sys.argv[1:])
    with open(os.path.join(cnclient, "lastlaunch.bat"), "w") as f:
        f.write("@echo off" + "\n" + f"cd /d {os.path.abspath('.')}" + "\n" + " ".join([os.path.join(os.path.dirname(BASE_DIR), "java-runtime", "bin", "java.exe")] + launch_arg.split(" ")[1:]) + "\npause")
    print("启动参数: {}".format(launch_arg))
    launch = threading.Thread()
    launch.run = lambda: launchclient(launch_arg)
    launch.start()
    end_launch()

if __name__ == "__main__":
    sys.exit(main())
