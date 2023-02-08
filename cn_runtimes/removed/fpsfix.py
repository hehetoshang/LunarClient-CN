import psutil

PRIORITY_CLASS = psutil.BELOW_NORMAL_PRIORITY_CLASS # 优先级

def main():
    for pid in psutil.pids():
        try:
            p = psutil.Process(pid)
            if p.exe().endswith("javaw.exe") or p.exe().endswith("java.exe"):
                print(p.exe())
                p.nice(PRIORITY_CLASS)
        except:
            pass

if __name__ == "__main__":
    main()
