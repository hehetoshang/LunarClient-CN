import os
import sys
import threading
import requests
import webbrowser
import configparser

import zipfile

from PyQt5.QtWidgets import QApplication, QMessageBox

__version__ = "v2.11.2-fix16"

PRE_VERSION = False

# ----
SKIP_CRACK_UPDATE = False
SKIP_CRACK_UPDATE = PRE_VERSION
# ----

LATEST_VERSION_URL = "https://github.com/chenmy1903/LunarClient-CN/releases"
LATEST_VERSION = __version__

if not SKIP_CRACK_UPDATE:
    try:
        fast_link = "https://github.com/"
        update_link = "chenmy1903/lunarclient-cn/releases/latest"

        LATEST_VERSION_URL = "https://github.com/" + "/".join(requests.get(fast_link + update_link, timeout=5).url.split("/")[3:])
        LATEST_VERSION = LATEST_VERSION_URL.split("/")[-1]
    except Exception as e:
        SKIP_CRACK_UPDATE = True

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CLIENT_DIR = os.path.dirname(BASE_DIR)

run_in_pyw = sys.executable.replace("\\", "/").split("/")[-1] in ["pyw.exe", "pythonw.exe"]

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
    sys.exit()

term = """Emmmmmmmmmm
一些想说的话 (只会弹出一次)
LunarClient-CN从来没有增加过后门, 而且是开源在GitHub上面的
网址: https://github.com/chenmy1903/LunarClient-CN
且唯一作者为chenmy1903 (CubeWhy), 只发布在GitHub上面, 其他地方下载到的都不是正版!
----
关于封禁
LC-CN没有任何外置的反作弊检测!可以开挂!不会封禁开挂的玩家!
> 正常玩家还是不要看具体的关于封禁罢......
------
关于Low IQ
LC-CN从fix12之后启动器核心就换为CNLAUNCHER了, 大大的java启动成功应该看得见罢
如果无法启动就是启动的时候发生了错误
CNLAUNCHER还没有制作错误处理, 请等待更新.
------
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


def main():
    print("启动Lunar Client!")
    if not os.path.isdir(cnclient):
        os.makedirs(cnclient)
    At = os.path.join(cnclient, "AcceptedTerm")
    app = QApplication([sys.executable])
    first_launch = not os.path.isfile(At)
    if LATEST_VERSION != __version__ and not SKIP_CRACK_UPDATE:
        if QMessageBox.question(None, "Lunar Client CN AutoUpdate", "你的LC-CN需要更新!\n当前版本: {}\n最新版本: {}\n点击确定则自动更新(点击取消退出LC-CN)\n{}".format(__version__, LATEST_VERSION, LATEST_VERSION_URL)) == QMessageBox.Yes:
            # webbrowser.open(LATEST_VERSION_URL)
            update_lunarcn()
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
