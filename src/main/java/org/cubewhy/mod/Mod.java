package org.cubewhy.mod;

import kotlinx.serialization.Serializable;
import org.cubewhy.lunarcn.loader.api.ModInitializer;
import org.cubewhy.lunarcn.loader.api.command.CommandBus;
import org.cubewhy.lunarcn.loader.api.event.EventBus;
import org.cubewhy.mod.commands.TestCommand;
import org.cubewhy.mod.listeners.PlayerListener;

import java.util.Arrays;
import java.util.Collections;
import java.util.List;

public class Mod implements ModInitializer {
    @Override
    public void preInit() {
        // Mod初始化方法

        CommandBus.register(new TestCommand()); // 注册指令

        EventBus.subscribe(new PlayerListener()); // 注册监听器
    }
}
