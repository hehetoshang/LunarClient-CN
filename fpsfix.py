import psutil

PRIORITY_CLASS = psutil.HIGH_PRIORITY_CLASS # 优先级

for pid in psutil.pids():
    try:
        p = psutil.Process(pid)
        if p.exe().endswith("javaw.exe"):
            print(p.exe())
            p.nice(PRIORITY_CLASS)
    except:
        pass
