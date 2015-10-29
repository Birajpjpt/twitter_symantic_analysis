package com.thehutgroup.security.spring;

import com.thehutgroup.security.model.Endpoint;
import com.thehutgroup.security.spring.example.ControllerAnnotationExample;
import com.thehutgroup.security.spring.example.ControllerAnnotationImplExample;
import org.junit.Test;

import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

import static org.junit.Assert.*;

public class ControllerAnnotationScannerTest {
    @Test
    public void method_getControllerUrls() {
        final Class clazz = ControllerAnnotationExample.class;
        final ControllerAnnotationScanner scanner = new ControllerAnnotationScanner(clazz);
        final List<Endpoint> actual = scanner.getControllerUrls();
        final List<Endpoint> expected = new ArrayList<Endpoint>();

        expected.add(new Endpoint("GET", "/root/method1"));
        expected.add(new Endpoint("POST", "/root/method2"));

        Collections.sort(actual);
        Collections.sort(expected);
        assertEquals(expected, actual);

        Class clazz_No_Results = ControllerAnnotationScannerTest.class;
        ControllerAnnotationScanner scanner_No_Results = new ControllerAnnotationScanner(clazz_No_Results);
        assertEquals(scanner_No_Results.getControllerUrls(), new ArrayList<Endpoint>());
    }

    @Test
    public void method_buildPath() throws NoSuchMethodException, InvocationTargetException, IllegalAccessException
    {
        assertEquals(buildPath("aaa"  ,"bbb"  ), "aaa/bbb"   );
        assertEquals(buildPath("aaa"  ,"/bbb" ), "aaa/bbb"    );
        assertEquals(buildPath("/aaa" ,"bbb"  ), "/aaa/bbb"  );
        assertEquals(buildPath("/aaa" ,"/bbb" ), "/aaa/bbb"  );
        assertEquals(buildPath("/aaa/","/bbb" ), "/aaa//bbb" );
        assertEquals(buildPath("/aaa/","/bbb/"), "/aaa//bbb/");
    }


    @Test
    public void test_ControllerAnnotationScanner_Methods() {
        ControllerAnnotationExample controllerAnnotationExample = new ControllerAnnotationExample();

        assertEquals(controllerAnnotationExample.method1(), "an value 1");
        assertEquals(controllerAnnotationExample.method2(), "an value 2");
        ControllerAnnotationImplExample controllerAnnotationImplExample = new ControllerAnnotationImplExample();
        assertEquals(controllerAnnotationImplExample.method3(), "an value 3");
    }

    // reflection methods
    public static String buildPath(String prefix, String value) throws NoSuchMethodException, InvocationTargetException, IllegalAccessException
    {
        Class                       dummyClass = String.class;
        ControllerAnnotationScanner scanner    = new ControllerAnnotationScanner(dummyClass);
        Method                      method     = getMethod(scanner, "buildPath", String.class, String.class);
        String                      result     = invokeMethod(method, scanner, String.class,  prefix, value);
        return result;
    }

    public static Method getMethod(Object object, String name, Class... paramTypes) throws NoSuchMethodException
    {
        return object.getClass().getDeclaredMethod(name, paramTypes);
    }

    public static <T> T invokeMethod(Method method, Object object, Class<T> returnType, Object... params) throws InvocationTargetException, IllegalAccessException
    {
        method.setAccessible(true);
        return (T)method.invoke(object, params);
    }
}
