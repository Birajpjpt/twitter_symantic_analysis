package com.thehutgroup.security.util;

import com.thehutgroup.security.spring.example.*;
import org.junit.Test;
import org.springframework.stereotype.Controller;

import static org.junit.Assert.*;

public class AnnotationUtilTest {

    @Test
    public void test_AnnotationUtil_Ctor()
    {
        AnnotationUtil annotationUtil = new AnnotationUtil();
        assertNotNull(annotationUtil);
    }
    @Test
    public void test_IsAnnotationPresent() throws Exception
    {
        Class clazz_OK      = ControllerAnnotationExample.class;            // with annotation in Class
        Class clazz_OK_Impl = ControllerAnnotationImplExample.class;        // with annotation in Interface
        Class clazz_Not_OK  = AnnotationUtilTest.class;
        Class annotation    = Controller.class;
        assertTrue(AnnotationUtil.isAnnotationPresent(clazz_OK      , annotation));
        assertFalse(AnnotationUtil.isAnnotationPresent(clazz_Not_OK , annotation));
        assertTrue(AnnotationUtil.isAnnotationPresent(clazz_OK_Impl , annotation));
        assertFalse(AnnotationUtil.isAnnotationPresent(clazz_OK     , null      ));

        try
        {
            AnnotationUtil.isAnnotationPresent(null, annotation);
        }
        catch(Exception ex)
        {
            assertEquals(ex.getClass() , IllegalArgumentException.class);
            assertEquals(ex.getMessage(), "clazz is null!");}                   // added } to here due to code coverage
    }



    @Test
    public void test_GetAnnotation() throws Exception
    {

    }
}