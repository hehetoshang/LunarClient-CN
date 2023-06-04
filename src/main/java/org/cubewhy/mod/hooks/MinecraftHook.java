package org.cubewhy.mod.hooks;

import org.cubewhy.lunarcn.loader.api.Hook;
import org.jetbrains.annotations.NotNull;
import org.objectweb.asm.Opcodes;
import org.objectweb.asm.Type;
import org.objectweb.asm.tree.ClassNode;
import org.objectweb.asm.tree.MethodInsnNode;

public class MinecraftHook extends Hook {
    public MinecraftHook() {
        super("net/minecraft/Minecraft"); // 在这里声明你要hook哪个类
    }

    @Override
    public void transform(@NotNull ClassNode classNode, @NotNull AssemblerConfig assemblerConfig) {
        // 注入代码, 和asm一样
        // 因为主播不擅长写这个, 这里就不写了
    }
}
