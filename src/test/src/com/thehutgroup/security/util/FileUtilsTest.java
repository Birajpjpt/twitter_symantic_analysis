package com.thehutgroup.security.util;

import com.thehutgroup.security.model.Endpoint;
import com.thehutgroup.security.spring.ControllerAnnotationScanner;
import com.thehutgroup.security.spring.example.ControllerAnnotationExample;
import org.junit.Test;

import java.io.File;
import java.net.MalformedURLException;
import java.net.URISyntaxException;
import java.util.List;

import static org.junit.Assert.*;
/**
 * Created by diniscruz on 21/10/15.
 */
public class FileUtilsTest
{

    @Test
    public void FileUtils_Ctor()
    {
        assertNotNull(new FileUtils());
    }
    @Test
    public void method_getPathFromClass() throws URISyntaxException, MalformedURLException, ClassNotFoundException
    {
        Class target = ControllerAnnotationExample.class;
        String file_Path = FileUtils.getPathFromClass(target);
        File file = new File(file_Path);
        assertTrue(file.exists());
    }

    @Test
    public void method_loadClassFromPath() throws URISyntaxException, MalformedURLException, ClassNotFoundException
    {
        Class target = ControllerAnnotationExample.class;
        String file_Path = FileUtils.getPathFromClass(target);
        System.out.println(file_Path);
        Class clazz = FileUtils.loadClassFromPath(file_Path, target);
        assertNotNull(clazz);
        assertEquals(clazz.getName(), target.getName());


    }
    @Test
    public void method_getJsonForObject() throws URISyntaxException, MalformedURLException, ClassNotFoundException
    {
        Class target = ControllerAnnotationExample.class;
        Class clazz = FileUtils.loadClassFromPath(FileUtils.getPathFromClass(target), target);

        final ControllerAnnotationScanner scanner = new ControllerAnnotationScanner(clazz);
        final List<Endpoint> endpoints = scanner.getControllerUrls();

        String endpoints_Json = FileUtils.getJsonForObject(endpoints,false);
        assertEquals(endpoints_Json, "[{\"httpMethod\":\"GET\",\"path\":\"/root/method1\"},{\"httpMethod\":\"POST\",\"path\":\"/root/method2\"}]");

        String endpoints_Json_Pretty = FileUtils.getJsonForObject(endpoints);
        assertEquals(endpoints_Json_Pretty, "[\n" +
                                            "  {\n" +
                                            "    \"httpMethod\": \"GET\",\n" +
                                            "    \"path\": \"/root/method1\"\n" +
                                            "  },\n" +
                                            "  {\n" +
                                            "    \"httpMethod\": \"POST\",\n" +
                                            "    \"path\": \"/root/method2\"\n" +
                                            "  }\n" +
                                            "]");

    }
}