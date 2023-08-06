package org.cubewhy.lunarcn.gui;

import org.cubewhy.launcher.LunarDownloader;
import org.cubewhy.lunarcn.Main;
import org.cubewhy.lunarcn.utils.FileUtils;

import javax.swing.*;
import java.io.IOException;
import java.util.Comparator;
import java.util.List;
import java.util.Objects;

import static org.cubewhy.lunarcn.Main.config;
import static org.cubewhy.lunarcn.Main.logger;

public class GuiMainWindow {
    public final JFrame frame;
    public ImageIcon icon = null;

    {
        try {
            icon = new ImageIcon(FileUtils.getFile("icon.png").readAllBytes());
        } catch (Exception e) {
            logger.catching(e);
        }
    }

    public GuiMainWindow() {
        frame = new JFrame(Main.productName);
        frame.setSize(350, 200);
        frame.setResizable(false);
        if (icon != null) {
            frame.setIconImage(icon.getImage());
        }
        frame.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);

        JPanel panel = new JPanel();
        frame.add(panel);

        try {
            place(panel);
        } catch (IOException e) {
            JOptionPane.showMessageDialog(this.frame, "Load failed", Main.productName, JOptionPane.ERROR_MESSAGE);
        }
    }

    private void place(JPanel panel) throws IOException {
        panel.setLayout(null);

        JLabel labelX = new JLabel(Main.productName);
        labelX.setBounds(10, 20, 80, 25);
        panel.add(labelX);

        JComboBox<String> versionList = new JComboBox<>();
        JComboBox<String> moduleList = new JComboBox<>();
        // get support versions
        List<String> versions = LunarDownloader.getSupportVersions();
        versions.sort(Comparator.reverseOrder());
        for (String supportVersion : versions) {
            versionList.addItem(supportVersion);
        }

        JLabel labelVersion = new JLabel("Version: ");
        labelVersion.setBounds(10, 45, 50, 25);
        panel.add(labelVersion);
        versionList.setBounds(70, 45, 80, 25);

        versionList.addItemListener(event -> {
            // flush modules
            flushModules(event.getItem().toString(), moduleList);
        });

        versionList.setSelectedItem(config.getValue("version").getAsString());

        flushModules(Objects.requireNonNull(versionList.getSelectedItem()).toString(), moduleList);

        moduleList.setSelectedItem(config.getValue("module").getAsString());

        JLabel labelModule = new JLabel("Module: ");
        labelModule.setBounds(10, 75, 80, 25);

        moduleList.setBounds(70, 75, 80, 25);

        panel.add(labelModule);

        panel.add(versionList);
        panel.add(moduleList);

        // branch
        JLabel labelBranch = new JLabel("Branch: ");
        labelBranch.setBounds(10, 105, 80, 25);
        panel.add(labelBranch);

        JTextField branchInput = new JTextField();
        branchInput.setText(config.getValue("branch").getAsString());
        branchInput.setBounds(70, 105, 80, 25);

        panel.add(branchInput);
    }

    public void show() {
        frame.setVisible(true);
    }

    private void flushModules(String version, JComboBox<String> moduleComboBox) {
        moduleComboBox.removeAllItems();
        try {
            for (String module : LunarDownloader.getSupportModules(version)) {
                moduleComboBox.addItem(module);
            }
        } catch (IOException e) {
            moduleComboBox.addItem("lunar");
            JOptionPane.showMessageDialog(this.frame, "Failed to load Modules", Main.productName, JOptionPane.ERROR_MESSAGE);
            logger.catching(e);
        }
    }
}
