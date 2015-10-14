package com.thehutgroup.security.spring;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;

@Controller("/root")
public class ControllerAnnotationExample
{
    @RequestMapping(path = "/method1", method = RequestMethod.GET)
    public String method1()
    {
        return "";
    }

    @RequestMapping(value = "/method2", method = RequestMethod.POST)
    public String method2()
    {
        return "";
    }
}
