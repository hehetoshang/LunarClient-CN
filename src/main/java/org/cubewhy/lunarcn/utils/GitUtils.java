package org.cubewhy.lunarcn.utils;

import java.io.IOException;
import java.io.InputStream;
import java.util.Properties;

public class GitUtils {
    public static Properties getGitInfo() throws IOException {
        InputStream gitInfo = FileUtils.getFile("git.properties");
        Properties properties = new Properties();
        properties.load(gitInfo);
        return properties;
    }

    public static String getBranch() throws IOException {
        return getGitInfo().getProperty("git.branch", "unknown");
    }

    public static String getBuilder() throws IOException {
        return getGitInfo().getProperty("git.build.user.name");
    }

    public static String getVersion() throws IOException {
        return getGitInfo().getProperty("git.build.version");
    }

    public static String getCommitIdAbbrev() throws IOException {
        return getGitInfo().getProperty("git.commit.id.abbrev");
    }

    public static String getCommitId() throws IOException {
        return getGitInfo().getProperty("git.commit.id");
    }

    public static String getRemoteUrl() throws IOException {
        return getGitInfo().getProperty("git.remote.origin.url");
    }
}
