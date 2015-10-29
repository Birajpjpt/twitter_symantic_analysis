package com.thehutgroup.security.spring.example;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;

@Controller("/root2")
interface ControllerAnnotationInterfaceExample
{
    @RequestMapping(value = "/method3", method = RequestMethod.POST)
    public String method3();
}

public class ControllerAnnotationImplExample implements ControllerAnnotationInterfaceExample
{
    public String method3()
    {
        return "an value 3";
    }
}
