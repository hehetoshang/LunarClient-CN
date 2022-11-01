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
    if not exitcode:
        QMessageBox.information(None, "Lunar Client CN", "游戏非正常退出\n退出码: {}\n请勿截图此界面给其他人!!!".format(exitcode))

def main():
    print("启动Lunar Client!")
    java = os.path.join(os.path.dirname(BASE_DIR), "java-runtime", "bin", "javaw.exe" if run_in_pyw else "java.exe")
    java_agents = get_java_agents()
    launch_arg = "\"" + java + "\" " + " ".join(java_agents) + " " + " ".join(sys.argv[1:])
    app = QApplication([sys.executable])
    print("启动参数: {}".format(launch_arg))
    launch = threading.Thread()
    launch.run = lambda: launchclient(launch_arg)
    launch.start()
    end_launch()

if __name__ == "__main__":
    sys.exit(main())
