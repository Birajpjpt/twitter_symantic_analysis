package com.thehutgroup.security.spring;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

import org.junit.Test;

import com.thehutgroup.security.model.Endpoint;

import static org.junit.Assert.assertEquals;

public class ControllerAnnotationScannerTest
{
    @Test
    public void testGetControllerUrls()
    {
        final Class clazz = ControllerAnnotationExample.class;
        final ControllerAnnotationScanner scanner = new ControllerAnnotationScanner(clazz);
        final List<Endpoint> actual = scanner.getControllerUrls();
        final List<Endpoint> expected = new ArrayList<Endpoint>();
        expected.add(new Endpoint("GET", "/root/method1"));
        expected.add(new Endpoint("POST", "/root/method2"));

        Collections.sort(actual);
        Collections.sort(expected);
        assertEquals(expected, actual);
    }
}
