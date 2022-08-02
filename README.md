# LunarClient InputFix

> Write in Chinese

## 下载

> 可以的话去B站给个三连或点击右上角Star给星标, [B站传送门](https://www.bilibili.com/read/cv17100937)

[点击此处](https://github.com/chenmy1903/LunarClient/releases)

## 这是什么

> 中文修复感谢[sduoduo233](https://github.com/sduoduo233/LunarInputFix)的代码

因为低版本的Minecraft无法输入中文, 这是一个Lunar Client的插件, 可以解决中文修复问题

## 快捷方式教程

创建快捷方式不要把主程序`Lunar Client.exe`做成快捷方式, 这样做会使程序出现bug

----------------↓正确方法↓---------------------

1. 将`launchlc.bat`弄成快捷方式
2. 右键->属性->自定义->更改图标->选择LC的主程序-> 选择第一个图标->点击确定

## 部分错误以及解决办法

> 先下载新版本试试

1. [Java启动错误](help/java-launch-failed.md)
2. [启动器卡住](help/launcher-failed.md)

## FAQ

### 会ban吗

不会

### 有后门吗

没有, 开放源代码, 可以去看

## 更新日志

### 预告(不一定是下个版本)

1. 修复中文修复可以被多开

### 2.11.2-fix5

> 此版本可以大幅提升性能

1. 汉化Settings中未汉化的部分
2. 进程优先级修复
3. 隐藏中文修复黑窗口

### 2.11.2-fix4

1. 修复未定义的函数导致中文修复注入失败的错误
2. 增加官网: [lunar.chenmy1903.tk](https://lunar.chenmy1903.tk)
3. 仓库更名为`LunarClient-CN`

### 2.11.2-fix3

> 请下载2.11.2-fix4版本, 本版本在修复1.19无法启动的bug的同时出现了无法注入中文修复的特性

1. 修复1.19无法启动的bug [严重]
2. 汉化部分错误报告

### 2.11.2-fix2

> 直接双击`Lunar Client.exe`就可以打开, 不要再去问咋弄了, 连安装python都没了

1. 1.9+版本不会启动中文修复
2. 游戏关闭后中文修复会自动关闭

### 2.11.2-fix1

> 部分玩家收到了dev版本, 这个是正式版。

1. 增加自定义JVM启动参数, [教程点这里](help/how-to-edit-launch-args.md)
2. `-server`启动参数可以去除
3. 优化inputfix-log, 未开启log的时候不创建log文件
4. 此版本起自带python运行环境(主要是不会安装环境的人太多了, txt写了看不懂)

### 2.11.2

1. 升级到2.11.2版本

### 2.10.1-fix2

1. 修改不是人话的汉化
2. 汉化部分错误报告

### 2.10.1-fix1

1. 修复因为依赖库错误而导致中文输入无法启动的bug

### 2.10.1

> 此版本起开始开源

1. 中文修复使用Python写(主要是c#搞不明白)
2. 汉化启动器(没汉化的地方就是改不了的地方)

### 2.10.1-old1

> bug贼多的版本, 本版本并没有开源

1. 有个毛用的中文修复
2. 汉化About界面
