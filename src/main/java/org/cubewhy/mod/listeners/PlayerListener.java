package org.cubewhy.mod.listeners;

import net.minecraft.client.Minecraft;
import net.minecraft.util.ChatComponentText;
import org.cubewhy.lunarcn.loader.api.event.PlayerListEvent;
import org.cubewhy.lunarcn.loader.api.event.SubscribeEvent;

public class PlayerListener {
    // 事件监听器

    @SubscribeEvent
    public void onPlayerJoin(PlayerListEvent.Add event) {
        // 玩家加入事件
        String playerName = event.getPlayerData().getProfile().getName(); // 获取玩家名字
        Minecraft.getMinecraft().thePlayer.addChatMessage(new ChatComponentText(playerName + " has join"));
    }

    @SubscribeEvent
    public void onPlayerLeft(PlayerListEvent.Remove event) {
        // 玩家离开事件
        String playerName = event.getPlayerData().getProfile().getName(); // 获取玩家名字
        Minecraft.getMinecraft().thePlayer.addChatMessage(new ChatComponentText(playerName + " has left"));
    }
}
