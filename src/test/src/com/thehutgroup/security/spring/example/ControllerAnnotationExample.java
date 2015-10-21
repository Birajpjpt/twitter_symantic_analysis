package com.thehutgroup.security.spring.example;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;



@Controller("/root")
public class ControllerAnnotationExample
{

    @RequestMapping(path = "/method1", method = RequestMethod.GET)
    public String method1()  {
        return "an value 1";
    }

    @RequestMapping(value = "/method2", method = RequestMethod.POST)
    public String method2()
    {
        return "an value 2";
    }


}
