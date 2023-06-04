package org.cubewhy.mod.commands;

import org.cubewhy.lunarcn.loader.api.command.Command;
import org.jetbrains.annotations.NotNull;
import org.lwjgl.opengl.Display;

public class TestCommand extends Command {
    public TestCommand() {
        super("title"); // super(<指令>, [指令别名])
    }

    @Override
    public void handle(@NotNull String[] strings) {
        // 指令调用后执行
        Display.setTitle(String.join(" ", strings)); // 此处为设置标题, 可以修改为自己的代码
    }
}
