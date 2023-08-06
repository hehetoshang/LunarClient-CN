package org.cubewhy.lunarcn.utils;

import org.jetbrains.annotations.NotNull;

import java.io.*;

public class FileUtils {
    public static InputStream getFile(String pathToFile) {
        return FileUtils.class.getResourceAsStream("/" + pathToFile);
    }

    public void copyFile(File sourceFile, @NotNull File targetFolder) throws IOException {
        if (!targetFolder.exists()) {
            targetFolder.mkdirs();
        }

        File targetFile = new File(targetFolder, sourceFile.getName());
        try (InputStream in = new FileInputStream(sourceFile);
             OutputStream out = new FileOutputStream(targetFile)) {
            byte[] buffer = new byte[1024];
            int length;
            while ((length = in.read(buffer)) > 0) {
                out.write(buffer, 0, length);
            }
        }
    }
}
