package com.thehutgroup.security.jersey;

import com.thehutgroup.security.jersey.example.*;
import com.thehutgroup.security.model.Endpoint;
import org.junit.Test;

import javax.ws.rs.*;
import java.lang.reflect.Field;
import java.util.*;

import static org.junit.Assert.assertEquals;

/**
 * Created by diniscruz on 21/10/15.
 */
public class JerseyTestUtilsTest {

    @Test
    public void method_ENDPOINT_ANNOTATIONS() throws IllegalAccessException, NoSuchFieldException
    {

        HashSet expected_values = new HashSet<Class<?>>(Arrays.<Class<?>>asList(GET.class, POST.class, PUT.class, DELETE.class, HEAD.class, OPTIONS.class));

        HashSet endpoint_Annotations = getStaticFieldValue(JerseyTestUtils.class, "ENDPOINT_ANNOTATIONS", HashSet.class );
        assertEquals(endpoint_Annotations, expected_values);
    }

    @Test
    public void method_GetAllRESTfulEndpoints() throws Exception {
        ApplicationConfig application = new ApplicationConfig();
        List<Endpoint> actual = JerseyTestUtils.getAllRESTfulEndpoints(application);
        List<Endpoint> expected = new ArrayList<Endpoint>();

        Collections.sort(actual);

        expected.add(new Endpoint("GET" , "/pojo"));
        expected.add(new Endpoint("POST", "/pojo/{c}"));
    }

    @Test
    public void test_SimpleRESTPojo()
    {
        SimpleRESTPojo simpleRESTPojo = new SimpleRESTPojo();
        assertEquals(simpleRESTPojo.pojo(), "pojo ok");
        assertEquals(simpleRESTPojo.withPathParam((double)12), "it's 42");
    }
    //reflection methods
    public static <T> T getStaticFieldValue(Class source, String fieldName, Class<T> returnType) throws NoSuchFieldException, IllegalAccessException
    {
        Field field = source.getDeclaredField(fieldName);
        field.setAccessible(true);
        return (T)field.get( JerseyTestUtils.class);
    }


}