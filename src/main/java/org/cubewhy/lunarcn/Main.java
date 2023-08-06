package org.cubewhy.lunarcn;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.cubewhy.lunarcn.file.ConfigFile;
import org.cubewhy.lunarcn.gui.GuiMainWindow;
import org.cubewhy.lunarcn.utils.GitUtils;

import java.io.File;
import java.io.IOException;

public class Main {
    public static final String productName = "LunarCN-X";
    public static final String productVersion;

    static {
        String productVersion1;
        try {
            productVersion1 = GitUtils.getVersion();
        } catch (IOException e) {
            productVersion1 = "1.0";
        }
        productVersion = productVersion1;
    }

    public static final File configDir = new File(System.getProperty("user.home"), ".cubewhy/lunarcn");

    public static final ConfigFile config = new ConfigFile(new File(configDir, "/config.json"));
    public static final Logger logger = LogManager.getLogger(productName);

    public static void main(String[] args) {
        config.load();
        logger.info("Show window");
        new GuiMainWindow().show();
    }
}