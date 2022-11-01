import json
import os
import sys
import time
import json
import frida
import psutil
import requests

from PyQt5.QtWidgets import QApplication, QMessageBox # used for black list

WRITE_LOG = False # 是否启用log(log没啥毛用,还会占磁盘空间,除非调试,否则保持关闭)
def get_minecraft_version():
    lunar_settings_ = os.path.join(os.path.expandvars("%USERPROFILE%"), ".lunarclient", "settings", "launcher.json")
    if not os.path.isfile(lunar_settings_):
        return True
    with open(lunar_settings_, "r", encoding="utf-8") as f:
        lunar_settings = f.read()
    try:
        version = json.loads(lunar_settings)["selectedVersion"]
        return version
    except KeyError:
        return True

print("检测游戏版本...")
if not get_minecraft_version() in ["1.8", "1.7", True]:
    sys.exit()
try:
    print("寻找javaw.exe")
    session = frida.attach("javaw.exe")
except frida.ProcessNotFoundError:
    print("没有寻找到javaw.exe, 尝试寻找java.exe")
    try:
        session = frida.attach("java.exe")
    except frida.ProcessNotFoundError:
        print("未找到任何正在运行的java, 启动游戏后在开启中文修复")
        sys.exit()
script = session.create_script("""
function readMessage(p){
    var hwnd = p.readPointer()
    var message = p.add(Process.pointerSize).readUInt()
    var wParam = p.add(Process.pointerSize+8).readU64()
    var lParam = p.add(Process.pointerSize+8+8).readU64()
    return {
        "hwnd": hwnd,
        "message": message,
        "wParam": wParam,
        "lParam": lParam
    }
}

var msgPointer
var messages = []
Interceptor.attach(Module.getExportByName('user32.dll', 'PeekMessageW'), {
    onEnter(args) {
        msgPointer = args[0];
    },
    onLeave(retval) {
        
        if(retval == 0x0){
            if(messages.length > 0){
                var msg = messages.shift()
                msgPointer.writePointer(msg.hwnd)
                msgPointer.add(Process.pointerSize).writeUInt(msg.message)
                msgPointer.add(Process.pointerSize+8).writeU64(msg.wParam)
                msgPointer.add(Process.pointerSize+8+8).writeU64(msg.lParam)
                %s
                retval.replace(0x1)
            }
            return
        }
        
        var msg = readMessage(msgPointer)
        
        // CHAR
        if(msg.message == 258){
            var char = msg.wParam & 65535
            %s
            if(char > 255){
                retval.replace(0x0)
                
                // keydown VK_PACKET
                messages.push({
                    "hwnd": msg.hwnd,
                    "message": 0x0100,
                    "wParam": 0xE7,
                    "lParam": 0x1
                })
                // CHAR
                messages.push({
                    "hwnd": msg.hwnd,
                    "message": 0x0102,
                    "wParam": char,
                    "lParam": 0x1
                })
                // keyup VK_PACKET
                messages.push({
                    "hwnd": msg.hwnd,
                    "message": 0x0101,
                    "wParam": 0xE7,
                    "lParam": 0xC0000001
                })
            }
        }
        
        // KEYDOWN
        if(msg.message == 256){
            var keycode = msg.wParam
            var pervious_state = (msg.lParam >>> 30) & 0x1
            var state = 1 - ((msg.lParam >>> 31) & 0x1)
            %s
        }
    }
})
""" % ('console.log("--> SEND", JSON.stringify(readMessage(msgPointer)))' if WRITE_LOG else "", 'console.log("char", JSON.stringify(msg), String.fromCharCode(char))' if WRITE_LOG else "", 'console.log("keydown", JSON.stringify(msg), String.fromCharCode(keycode))' if WRITE_LOG else ""))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if WRITE_LOG:
    log = os.path.join(BASE_DIR, "inputfixlog.log")
    logf = open(log, "a")
def on_message(message, data):
    """写入日志"""
    if WRITE_LOG:
        print(message, file=logf)

def get_banned():
    blacklist = []
    try:
        r = requests.get("https://chenmy1903.github.io/LunarClient-CN/blacklist", proxies={'http': None, 'https': None}) # 防止被抓包软件重定向
        blacklist = eval(r.text)
    except:
        print("封禁列表获取失败")
    return blacklist

blacklist = get_banned()

def account_in_black_list(bl):
    f = os.path.join(os.path.expanduser("~"), ".lunarclient", "settings", "game", "accounts.json")
    with open(f, "r", encoding="utf-8") as f_r:
        j = json.load(f_r)
    accounts: dict = j["accounts"]
    c: dict
    for c in accounts.values():
        user_uuid = c["minecraftProfile"]["id"]
        if user_uuid in bl:
            return True, bl[user_uuid], user_uuid, c["minecraftProfile"]["name"]
    return False, ""

script.on('message', on_message)
print("将钩子勾上LunarClient...")
script.load() # 注入中文输入
print("中文修复开启成功")
print("不要关闭本窗口,关闭后中文修复会失效")
print("关闭游戏后中文修复会自动关闭 (测试版本, 可能有bug)")
print("log文件: {}".format(log)) if WRITE_LOG else print("log已被禁用,修改WRITE_LOG变量以开启(调试才用开)")

ban_end = """反正是开源的,你自己给自己unban也不是不行
不会unban还是去买iqbooster罢
LL
"""
reason = "原因?什么原因啊!CubeWhy肯定不会神权的, 又不是huanmeng"

while True:
    banned = account_in_black_list(blacklist)
    if banned[0]:
        for pid in psutil.pids():
            try:
                p = psutil.Process(pid)
                if p.exe().endswith("javaw.exe") or p.exe().endswith("java.exe") or p.exe().endswith("Lunar Client CN.exe") or p.exe().endswith("Lunar Client.exe"):
                    p.kill()
            except:
                pass
        app = QApplication(sys.argv)
        print("账户已被封禁。")
        reason = banned[1]["reason"] if "reason" in banned[1] else reason
        ban_end = banned[1]["ban_end"] if "ban_end" in banned[1] else ban_end
        u_id = banned[2]
        u_nick = banned[3]
        QMessageBox.critical(None, "LunarClient-CN ban", "你的lc-cn账户已被封禁~\n申诉加QQ(大概率不解封) -> 2834886052 <-\nPlayer: {}\nUUID: {}\n原因: {}\n{}\n{}\n{}".format(u_nick, u_id, reason, len(ban_end) * "-", ban_end, len(ban_end) * "-"))
        sys.exit()
    if script.is_destroyed:
        print("游戏进程已结束!结束中文修复进程!")
        sys.exit()
    time.sleep(10)
    blacklist = get_banned()
