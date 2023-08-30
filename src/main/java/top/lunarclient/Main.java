package top.lunarclient;
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.net.MalformedURLException;
import java.net.URL;
import java.io.*;

public class Main extends JFrame {
    // 创建一个名为Version的字符串变量
    private String version = "1.8.9";
    // 创建一个新的字符串变量，用于存储用户输入的分支名称
    String[] branch = {"master"};
    public Main() {
        // 设置窗口标题
        super("Lunar GUI");

        // 设置窗口大小为1200x750像素
        setSize(1200, 750);

        // 设置窗口关闭时退出程序
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        try (FileInputStream fileIn = new FileInputStream("version.ser");
             ObjectInputStream in = new ObjectInputStream(fileIn)) {
            version = (String) in.readObject();
        } catch (IOException | ClassNotFoundException i) {
            i.printStackTrace();
        }
        try (FileInputStream fileIn = new FileInputStream("branch.ser");
             ObjectInputStream in = new ObjectInputStream(fileIn)) {
            branch = (String[]) in.readObject();
        } catch (IOException | ClassNotFoundException i) {
            i.printStackTrace();
        }
        // 创建一个卡片布局
        CardLayout cardLayout = new CardLayout();

        // 创建一个主面板容器，并设置为卡片布局
        JPanel mainPanel = new JPanel(cardLayout);

// 创建第一个面板
        JPanel firstPanel = new JPanel();
        firstPanel.setLayout(new BorderLayout());


// 在面板一的顶部添加一个新的面板容器，用于存放按钮1和图片
        JPanel titlePanel = new JPanel(new FlowLayout(FlowLayout.CENTER));
// 在面板一的左上角显示网址为 http://null.com/ 的图片
        try {
            ImageIcon icon = new ImageIcon(new URL("https://assets.badlion.net/site/assets/badlion-white.png"));
            Image image = icon.getImage();
            Image scaledImage = image.getScaledInstance(150, 50, Image.SCALE_SMOOTH);
            ImageIcon scaledIcon = new ImageIcon(scaledImage);
            JLabel imageLabel = new JLabel(scaledIcon);
            titlePanel.add(imageLabel);
            titlePanel.add(Box.createHorizontalStrut(500));
        } catch (MalformedURLException e) {
            // 处理异常
            e.printStackTrace();
        }

// 添加4个新按钮
        JButton button1 = new JButton("首页");
        JButton button2 = new JButton("Button 2");
        JButton button3 = new JButton("分支");
        JButton button4 = new JButton("Button 4");

// 将按钮添加到标题面板中
        titlePanel.add(button1);
        titlePanel.add(button2);

// 为按钮3添加动作监听器，当用户点击按钮时，切换到第三个面板
        button3.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                cardLayout.show(mainPanel, "Third Panel");
            }
        });

        titlePanel.add(button3);
        titlePanel.add(button4);

// 创建一个新的面板容器，用于存放按钮
        JPanel buttonPanel = new JPanel(new FlowLayout(FlowLayout.CENTER));

// 添加一个启动按钮，并设置其字体大小为20
        JButton start = new JButton("启动"+version);
        start.setFont(new Font(start.getFont().getName(), start.getFont().getStyle(), 20));
        buttonPanel.add(start);

// 添加一个切换版本按钮，并设置其字体大小为20
        JButton vs = new JButton(">");
        vs.setFont(new Font(vs.getFont().getName(), vs.getFont().getStyle(), 20));

// 为按钮添加动作监听器
        vs.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                // 当用户点击按钮时，切换到另一个面板
                cardLayout.next(mainPanel);
            }
        });

        buttonPanel.add(vs);

// 将标题面板和按钮面板添加到第一个面板中
        firstPanel.add(titlePanel, BorderLayout.NORTH);
        firstPanel.add(buttonPanel, BorderLayout.CENTER);

//https://assets.badlion.net/site/assets/badlion-black.png
// 将第一个面板添加到主面板中
        mainPanel.add(firstPanel, "First Panel");

// 创建第二个面板
        JPanel secondPanel = new JPanel();
        secondPanel.setLayout(new BorderLayout());

        JPanel buttonPanel2 = new JPanel();
        buttonPanel2.setLayout(new BoxLayout(buttonPanel2, BoxLayout.Y_AXIS));


        JButton button5 = new JButton("1.7.10");
        button5.setFont(new Font(button5.getFont().getName(), button5.getFont().getStyle(), 25));
        button5.setPreferredSize(new Dimension(250, 50));

// 为按钮1添加动作监听器
        button5.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                // 当用户点击按钮1时，将变量 version 设为 "1.8.9"
                version = "1.7.10";
                // 更新分支标签的文本
                start.setText("启动" +version);
                // 打印 version 变量的值
                System.out.println("[Debug]Version: " + version);
            }
        });

        buttonPanel2.add(button5);

        buttonPanel2.add(Box.createVerticalStrut(10));

        JButton button6 = new JButton("1.8.9");
        button6.setFont(new Font(button6.getFont().getName(), button6.getFont().getStyle(), 25));
        button6.setPreferredSize(new Dimension(250, 50));
        buttonPanel2.add(button6);

        // 为按钮2添加动作监听器
        button6.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                // 当用户点击按钮2时，将变量 version 设为 "1.8.9"
                version = "1.8.9";
                // 更新分支标签的文本
                start.setText("启动" +version);
                // 打印 version 变量的值
                System.out.println("[Debug]Version: " + version);
            }
        });


        buttonPanel2.add(Box.createVerticalStrut(10));

        JButton button7 = new JButton("1.12.2");
        button7.setFont(new Font(button7.getFont().getName(), button7.getFont().getStyle(), 25));
        button7.setPreferredSize(new Dimension(250, 50));
        buttonPanel2.add(button7);

        // 为按钮3添加动作监听器
        button7.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                // 当用户点击按钮3时，将变量 version 设为 "1.12.2"
                version = "1.12.2";
                // 更新分支标签的文本
                start.setText("启动" +version);
                // 打印 version 变量的值
                System.out.println("[Debug]Version: " + version);
            }
        });
        buttonPanel2.add(Box.createVerticalStrut(10));

        JButton button8 = new JButton("1.16.5");
        button8.setFont(new Font(button8.getFont().getName(), button8.getFont().getStyle(), 25));
        button8.setPreferredSize(new Dimension(250, 50));
        buttonPanel2.add(button8);

        // 为按钮4添加动作监听器
        button8.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                // 当用户点击按钮4时，将变量 version 设为 "1.16.5"
                version = "1.16.5";
                // 更新分支标签的文本
                start.setText("启动" +version);
                // 打印 version 变量的值
                System.out.println("[Debug]Version: " + version);
            }
        });
        buttonPanel2.add(Box.createVerticalStrut(10));

        JButton button9 = new JButton("1.17.1");
        button9.setFont(new Font(button9.getFont().getName(), button9.getFont().getStyle(), 25));
        button9.setPreferredSize(new Dimension(250, 50));
        buttonPanel2.add(button9);
        buttonPanel2.add(Box.createVerticalStrut(10));

        // 为按钮5添加动作监听器
        button9.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                // 当用户点击按钮4时，将变量 version 设为 "1.17.1"
                version = "1.17.1";
                // 更新分支标签的文本
                start.setText("启动" +version);
                // 打印 version 变量的值
                System.out.println("[Debug]Version: " + version);
            }
        });

        JButton button10 = new JButton("1.18.2");
        button10.setFont(new Font(button10.getFont().getName(), button10.getFont().getStyle(), 25));
        button10.setPreferredSize(new Dimension(250, 50));
        buttonPanel2.add(button10);
        buttonPanel2.add(Box.createVerticalStrut(10));

        // 为按钮5添加动作监听器
        button10.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                // 当用户点击按钮4时，将变量 version 设为 "1.18.2"
                version = "1.18.2";
                // 更新分支标签的文本
                start.setText("启动" +version);
                // 打印 version 变量的值
                System.out.println("[Debug]Version: " + version);
            }
        });

        JButton button11 = new JButton("1.19.2");
        button11.setFont(new Font(button11.getFont().getName(), button11.getFont().getStyle(), 25));
        button11.setPreferredSize(new Dimension(250, 50));
        buttonPanel2.add(button11);
        buttonPanel2.add(Box.createVerticalStrut(10));

        // 为按钮5添加动作监听器
        button11.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                // 当用户点击按钮4时，将变量 version 设为 "1.19.2"
                version = "1.19.2";
                // 更新分支标签的文本
                start.setText("启动" +version);
                // 打印 version 变量的值
                System.out.println("[Debug]Version: " + version);
            }
        });

        JButton button12 = new JButton("1.19.3");
        button12.setFont(new Font(button12.getFont().getName(), button12.getFont().getStyle(), 25));
        button12.setPreferredSize(new Dimension(250, 50));
        buttonPanel2.add(button12);
        buttonPanel2.add(Box.createVerticalStrut(10));

        // 为按钮5添加动作监听器
        button12.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                // 当用户点击按钮4时，将变量 version 设为 "1.19.3"
                version = "1.19.3";
                // 更新分支标签的文本
                start.setText("启动" +version);
                // 打印 version 变量的值
                System.out.println("[Debug]Version: " + version);
            }
        });

        JButton button13 = new JButton("1.19.4");
        button13.setFont(new Font(button13.getFont().getName(), button13.getFont().getStyle(), 25));
        button13.setPreferredSize(new Dimension(250, 50));
        buttonPanel2.add(button13);
        buttonPanel2.add(Box.createVerticalStrut(10));

        // 为按钮5添加动作监听器
        button13.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                // 当用户点击按钮4时，将变量 version 设为 "1.19.4"
                version = "1.19.4";
                // 更新分支标签的文本
                start.setText("启动" +version);
                // 打印 version 变量的值
                System.out.println("[Debug]Version: " + version);
            }
        });

        JButton button14 = new JButton("1.20");
        button14.setFont(new Font(button14.getFont().getName(), button14.getFont().getStyle(), 25));
        button14.setPreferredSize(new Dimension(250, 50));
        buttonPanel2.add(button14);
        buttonPanel2.add(Box.createVerticalStrut(10));

        // 为按钮5添加动作监听器
        button14.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                // 当用户点击按钮4时，将变量 version 设为 "1.20"
                version = "1.20";
                // 更新分支标签的文本
                start.setText("启动" +version);
                // 打印 version 变量的值
                System.out.println("[Debug]Version: " + version);
            }
        });

        JButton button15 = new JButton("1.20.1");
        button15.setFont(new Font(button15.getFont().getName(), button15.getFont().getStyle(), 25));
        button15.setPreferredSize(new Dimension(250, 50));
        buttonPanel2.add(button15);
        buttonPanel2.add(Box.createVerticalStrut(10));

        // 为按钮5添加动作监听器
        button15.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                // 当用户点击按钮4时，将变量 version 设为 "1.20.1"
                version = "1.20.1";
                // 更新分支标签的文本
                start.setText("启动" +version);
                // 打印 version 变量的值
                System.out.println("[Debug]Version: " + version);
            }
        });

        secondPanel.add(buttonPanel2, BorderLayout.WEST);

        JSeparator separator = new JSeparator(SwingConstants.VERTICAL);
        secondPanel.add(separator, BorderLayout.CENTER);


// 添加一个返回按钮，并设置其首选大小为40x40像素
        JButton backButton = new JButton("保存");
        backButton.setPreferredSize(new Dimension(80, 45));

// 为返回按钮添加动作监听器
        backButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                // 当用户点击返回按钮时，返回第一个面板
                cardLayout.first(mainPanel);
            }
        });

        JPanel backButtonPanel = new JPanel(new FlowLayout(FlowLayout.RIGHT));
        backButtonPanel.add(backButton);

        secondPanel.add(backButtonPanel, BorderLayout.SOUTH);

// 将第二个面板添加到主面板中
        mainPanel.add(secondPanel, "second");




        JPanel thirdPanel = new JPanel();
        thirdPanel.setLayout(new BorderLayout());

// 设置窗口布局为流式布局
        thirdPanel.setLayout(new FlowLayout());

// 创建一个新的 JLabel 对象，用于显示标签文本
        JLabel label = new JLabel("自定义分支");

// 将标签添加到窗口中
        thirdPanel.add(label);

// 创建一个新的 JTextField 对象，用于接收用户输入
        JTextField textField = new JTextField();

// 设置文本框的大小
        textField.setPreferredSize(new Dimension(200, 25));

// 将第三个面板添加到主面板中，并命名为"Third Panel"
        mainPanel.add(thirdPanel, "Third Panel");

// 将文本框添加到窗口中
        thirdPanel.add(textField);

// 创建一个新的 JLabel 对象，用于显示当前分支名称
        JLabel branchLabel = new JLabel("当前分支: ");

// 更新分支标签的文本
        branchLabel.setText("当前分支: " + branch[0]);

// 将分支标签添加到窗口中
        thirdPanel.add(branchLabel);

// 创建一个新的 JButton 对象，用于保存用户输入
        JButton saveButton = new JButton("保存");

// 为保存按钮添加动作监听器
        saveButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                // 检查文本框是否为空
                if (textField.getText().isEmpty()) {
                    // 如果文本框为空，则显示一个消息对话框，提示用户分支不能为空
                    JOptionPane.showMessageDialog(Main.this, "分支不能为空");
                } else {
                    // 如果文本框不为空，则获取文本框中的文本并保存到变量 branch 中
                    branch[0] = textField.getText();

                    // 更新分支标签的文本
                    branchLabel.setText("当前分支: " + branch[0]);

                    // 显示一个消息对话框，显示当前分支名称
                    JOptionPane.showMessageDialog(Main.this, "当前分支: " + branch[0]);

                    // 切换回第一个面板
                    cardLayout.show(mainPanel, "First Panel");
                }
            }
        });

// 将保存按钮添加到窗口中
        thirdPanel.add(saveButton);

// 创建一个新的 JButton 对象，用于取消操作
        JButton cancelButton = new JButton("取消");

// 为取消按钮添加动作监听器
        cancelButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                // 切换回第一个面板
                cardLayout.show(mainPanel, "First Panel");
            }
        });

// 将取消按钮添加到窗口中
        thirdPanel.add(cancelButton);

// 将分支标签移动到取消按钮的右边
        thirdPanel.remove(branchLabel);
        thirdPanel.add(branchLabel);

// 将主面板添加到窗口中
        add(mainPanel);

// 显示窗口
        setVisible(true);
        // 添加关闭钩子，在程序退出之前执行代码
        Runtime.getRuntime().addShutdownHook(new Thread() {
            public void run() {
                try (FileOutputStream fileOut = new FileOutputStream("version.ser");
                     ObjectOutputStream out = new ObjectOutputStream(fileOut)) {
                    out.writeObject(version);
                } catch (IOException i) {
                    i.printStackTrace();
                }
                try (FileOutputStream fileOut = new FileOutputStream("branch.ser");
                     ObjectOutputStream out = new ObjectOutputStream(fileOut)) {
                    out.writeObject(branch);
                } catch (IOException i) {
                    i.printStackTrace();
                }
                System.out.println("[Debug]Version: " + version);
            }
        });


    }


    public static void main(String[] args) {
        new Main();
    }
}
