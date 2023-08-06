package org.cubewhy.lunarcn;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.cubewhy.lunarcn.file.ConfigFile;
import org.cubewhy.lunarcn.gui.GuiMainWindow;

import java.io.File;

public class Main {
    public static final String productName = "LunarCN-X";
    public static final ConfigFile config = new ConfigFile(new File(System.getProperty("user.home"), ".cubewhy/lunarcn/config.json"));

    public static final Logger logger = LogManager.getLogger(productName);

    public static void main(String[] args) {
        config.load();
        logger.info("Show window");
        new GuiMainWindow().show();
    }
}