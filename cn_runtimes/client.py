import os
import sys
import threading

from PyQt5.QtWidgets import QApplication, QMessageBox

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

run_in_pyw = sys.executable.replace("\\", "/").split("/")[-1] in ["pyw.exe", "pythonw.exe"]

def get_java_agents():
    jagents_dir = os.path.join(os.path.dirname(BASE_DIR), "javaagents")
    agents_path = []
    if not os.path.isdir(jagents_dir):
        return []
    for f in os.listdir(jagents_dir):
        if f.endswith(".jar"):
            agents_path.append("-javaagent:" + os.path.join(jagents_dir, f))
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
点击Yes启动游戏, 且此提示不在弹出
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
    if first_launch:
        if not pop_tip_of_first_launch():
            return
        with open(At, "w") as f:
            f.write("True")
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
