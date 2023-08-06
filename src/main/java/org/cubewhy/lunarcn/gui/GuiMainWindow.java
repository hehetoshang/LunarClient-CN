package org.cubewhy.lunarcn.gui;

import org.apache.logging.log4j.Level;
import org.cubewhy.launcher.LunarClient;
import org.cubewhy.launcher.LunarDir;
import org.cubewhy.launcher.LunarDownloader;
import org.cubewhy.launcher.game.MinecraftArgs;
import org.cubewhy.lunarcn.JavaAgent;
import org.cubewhy.lunarcn.Main;
import org.cubewhy.lunarcn.utils.FileUtils;
import org.cubewhy.lunarcn.utils.GitUtils;
import org.cubewhy.lunarcn.utils.JavaAgentUtils;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.io.IOException;
import java.net.URI;
import java.net.URISyntaxException;
import java.util.Comparator;
import java.util.List;
import java.util.Objects;

import static org.cubewhy.lunarcn.Main.*;

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
        frame = new JFrame(Main.productName + " " + Main.productVersion);
        frame.setSize(450, 300);
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

        // launch button
        JButton startButton = new JButton("Launch");
        startButton.setBounds(130, 200, 80, 25);
        startButton.addActionListener(event -> {
            String version = versionList.getSelectedItem().toString();
            String module = Objects.requireNonNull(moduleList.getSelectedItem()).toString();
            String branch = branchInput.getText();
            logger.info("Launch " + version + " Module: " + module);
            MinecraftArgs mcArgs = new MinecraftArgs(LunarDir.lunarDir + "/game", LunarDir.lunarDir + "/textures", 400, 300);
            JavaAgent[] agents = JavaAgentUtils.search();
            String[] jvmArgs = {};
            String[] programArgs = {};
            try {
                LunarDownloader.downloadLunarArtifacts(LunarDir.lunarDir + "/offline", LunarDownloader.getLunarArtifacts(version, branch, module));
            } catch (IOException e) {
                logger.catching(e);
            }
            try {
                LunarClient.launch(version, module, branch, LunarDir.lunarDir + "/offline", mcArgs, System.getProperty ("java.home") + "/bin/java", jvmArgs, programArgs, agents);
            } catch (IOException e) {
                JOptionPane.showMessageDialog(this.frame, "Launch failed", productName, JOptionPane.ERROR_MESSAGE);
                logger.catching(e);
            }
        });
        panel.add(startButton);

        // GitHub button
        ImageIcon gitHubIcon = new ImageIcon(FileUtils.getFile("github.png").readAllBytes());

        JLabel gitHubLabel = getGitHubLabel(gitHubIcon);

        panel.add(gitHubLabel);
        // donate button
        ImageIcon donateButton = new ImageIcon(FileUtils.getFile("donate.png").readAllBytes());

        JLabel donate = getDonate(donateButton);

        panel.add(donate);

    }

    private static JLabel getDonate(ImageIcon donateButton) {
        JLabel donate = new JLabel();
        donate.setIcon(donateButton);
        donate.setBounds(290, 200, 50, 50);
        donate.setCursor(new Cursor(Cursor.HAND_CURSOR));
        donate.setToolTipText("Donate us"); // hover text

        donate.addMouseListener(new MouseAdapter() {
            public void mouseClicked(MouseEvent event) {
                try {
                    Desktop.getDesktop().browse(new URI("https://donate.lunarcn.top"));
                } catch (IOException | URISyntaxException e) {
                    logger.catching(e);
                }
            }
        });
        return donate;
    }

    private static JLabel getGitHubLabel(ImageIcon gitHubIcon) {
        JLabel gitHubLabel = new JLabel();
        gitHubLabel.setIcon(gitHubIcon);
        gitHubLabel.setBounds(350, 200, 50, 50);
        gitHubLabel.setCursor(new Cursor(Cursor.HAND_CURSOR));
        gitHubLabel.setToolTipText("Source");

        gitHubLabel.addMouseListener(new MouseAdapter() {
            public void mouseClicked(MouseEvent evt) {
                try {
                    Desktop.getDesktop().browse(new URI(GitUtils.getRemoteUrl()));
                } catch (IOException | URISyntaxException e) {
                    logger.catching(e);
                }
            }
        });
        return gitHubLabel;
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
