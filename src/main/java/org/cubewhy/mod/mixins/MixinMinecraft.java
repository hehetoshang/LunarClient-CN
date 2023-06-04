package org.cubewhy.mod.mixins;

import net.minecraft.client.Minecraft;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

@Mixin(Minecraft.class)
public class MixinMinecraft {
    // Minecraft Mixin
    // 这个class仅为一个示例, 并不是只能注入这个class
    // Mixin需要在resources/examplemod.mixin.json中声明才会调用

    @Inject(method = "startGame", at = @At("HEAD"))
    public void onStartGame(CallbackInfo ci) {
        System.out.println("[MOD] Hello World LunarCN"); // 启动游戏时调用
    }

    // 具体用法请参考Mixin docs
}
