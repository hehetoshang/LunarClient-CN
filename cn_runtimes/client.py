import os
import sys
import threading
import requests
import webbrowser
import configparser

from PyQt5.QtWidgets import QApplication, QMessageBox

__version__ = "v2.11.2-fix14"

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

run_in_pyw = sys.executable.replace("\\", "/").split("/")[-1] in ["pyw.exe", "pythonw.exe"]

def get_java_agents():
    jagents_dir = os.path.join(os.path.dirname(BASE_DIR), "javaagents")
    agents_path = []
    if not os.path.isdir(jagents_dir):
        return []
    for f in os.listdir(jagents_dir):
        if f.endswith(".jar"):
            cfg = configparser.ConfigParser()
            cfg_file = os.path.join(jagents_dir, f + ".ini")
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
            agents_path.append("-javaagent:\"" + os.path.join(jagents_dir, f) + "\"" + (("=" + arg) if arg != "" else ""))
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

def main():
    print("启动Lunar Client!")
    if not os.path.isdir(cnclient):
        os.makedirs(cnclient)
    At = os.path.join(cnclient, "AcceptedTerm")
    app = QApplication([sys.executable])
    first_launch = not os.path.isfile(At)
    if LATEST_VERSION != __version__ and not SKIP_CRACK_UPDATE:
        if QMessageBox.question(None, "Lunar Client CN AutoUpdate", "你的LC-CN需要更新!\n当前版本: {}\n最新版本: {}\n点击确定跳转到下载页面(点击取消退出LC-CN)\n{}".format(__version__, LATEST_VERSION, LATEST_VERSION_URL)) == QMessageBox.Yes:
            webbrowser.open(LATEST_VERSION_URL)    
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
        f.write("@echo off" + "\n" + launch_arg)
    print("启动参数: {}".format(launch_arg))
    launch = threading.Thread()
    launch.run = lambda: launchclient(launch_arg)
    launch.start()
    end_launch()

if __name__ == "__main__":
    sys.exit(main())
