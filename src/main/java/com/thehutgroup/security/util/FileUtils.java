package com.thehutgroup.security.util;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

import java.io.File;
import java.net.MalformedURLException;
import java.net.URISyntaxException;
import java.net.URL;
import java.net.URLClassLoader;

public class FileUtils
{
    public static String getPathFromClass(Class clazz) throws URISyntaxException
    {
        String root_Path    = clazz.getProtectionDomain().getCodeSource().getLocation().toURI().getPath();
        String virtual_Path = clazz.getCanonicalName().replace(".", File.separator) + ".class";
        return root_Path + virtual_Path ;
    }

    public static Class loadClassFromPath(String path, Class clazz) throws MalformedURLException, ClassNotFoundException
    {
        return loadClassFromPath(path, clazz.getCanonicalName());
    }

    public static Class loadClassFromPath(String path, String className) throws MalformedURLException, ClassNotFoundException
    {
        File file         = new File(path);
        URL url           = file.toURI().toURL();
        URL[] urls = new URL[]{url};

        ClassLoader classLoader = new URLClassLoader(urls);
        return classLoader.loadClass(className);
    }

    public static String getJsonForObject(Object object)
    {
        return getJsonForObject(object, true);
    }
    public static String getJsonForObject(Object object, boolean prettyPrint)
    {
        GsonBuilder gsonBuilder = new GsonBuilder();
        if(prettyPrint)
            gsonBuilder.setPrettyPrinting();
        Gson gson = gsonBuilder.create();
        return gson.toJson(object);
    }

//    public static String fileNameWithoutExtension(File file)
//    {
//        String fileName = file.getName();
//
//        int pos = fileName.lastIndexOf(".");
//        if (pos > 0) {
//            return fileName.substring(0, pos);
//        }
//        return fileName;
//    }
}
