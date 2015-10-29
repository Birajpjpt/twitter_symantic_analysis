package com.thehutgroup.security.model;

import org.junit.Before;
import org.junit.Test;

import java.util.ArrayList;
import java.util.List;

import static org.junit.Assert.assertEquals;
/**
 * Created by diniscruz on 15/10/15.
 */
public class EndpointTest {

    String httpMethod = "an method";
    String path       = "an path";
    Endpoint endpoint = null;

    @Before
    public void initialize()
    {
        endpoint = new Endpoint(httpMethod, path);
    }

    @Test
    public void Endpoint_Ctor_String_String()
    {
        assertEquals(endpoint.getHttpMethod(), httpMethod);
        assertEquals(endpoint.getPath()      , path);
    }

    @Test
    public void Endpoint_Ctor_String_Array()
    {
        List<String> params = new ArrayList<String>();
        Endpoint endpoint = new Endpoint(httpMethod, path, params);     // with no params
        assertEquals(endpoint.getHttpMethod(), "an method");
        assertEquals(endpoint.getPath()      , "an path");

        params.add("param-1");
        params.add("param-2");
        endpoint = new Endpoint(httpMethod, path, params);            // with no two
        assertEquals(endpoint.getHttpMethod(), "an method");
        assertEquals(endpoint.getPath()      , "an path?[param-1]&[param-2]");
    }

    @Test
    public void method_setHttpMethod() throws Exception
    {
        endpoint.setHttpMethod("new value");
        assertEquals(endpoint.getHttpMethod(), "new value");
        endpoint.setHttpMethod(null);
        assertEquals(endpoint.getHttpMethod(), "");
    }

    @Test
    public void method_setPath() throws Exception
    {
        endpoint.setPath("new value");
        assertEquals(endpoint.getPath(), "new value");
        endpoint.setPath(null);
        assertEquals(endpoint.getPath(), "");
    }

    @Test
    public void method_compareTo() throws Exception
    {
        String httpMethod = "an method";
        String path       = "an path";
        Endpoint endpoint2 = new Endpoint(httpMethod  , path  );
        Endpoint endpoint3 = new Endpoint("httpMethod", path  );
        Endpoint endpoint4 = new Endpoint( httpMethod , "path");

        assertEquals(endpoint.compareTo(endpoint ), 0 );
        assertEquals(endpoint.compareTo(endpoint2), 0 );
        assertEquals(endpoint.compareTo(endpoint3), -7);
        assertEquals(endpoint.compareTo(endpoint4), -15);

        try
        {
            endpoint.compareTo(null);
        }
        catch(Exception ex)
        {
            assertEquals(ex.getClass() , IllegalArgumentException.class);
            assertEquals(ex.getMessage(), "o is null!");}                   // added } to here due to code coverage
    }
    @Test
    public void method_equals() throws Exception
    {
        String httpMethod = "an method";
        String path       = "an path";
        Endpoint endpoint2 = new Endpoint(httpMethod  , path  );
        Endpoint endpoint3 = new Endpoint("httpMethod", path  );
        Endpoint endpoint4 = new Endpoint( httpMethod , "path");

        assertEquals(endpoint.equals(endpoint2), true );
        assertEquals(endpoint.equals(endpoint3), false);
        assertEquals(endpoint.equals(endpoint4), false);
        assertEquals(endpoint.equals(null     ), false);

    }
    @Test
    public void method_toString() throws Exception
    {
        assertEquals(endpoint.toString(), "an method-an path");
    }
}