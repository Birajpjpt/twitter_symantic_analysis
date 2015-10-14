package com.thehutgroup.security.spring;

import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;

import com.thehutgroup.security.model.Endpoint;

import static com.thehutgroup.security.util.AnnotationUtil.getAnnotation;

public class ControllerAnnotationScanner
{
    public ControllerAnnotationScanner(final Class clazz)
    {
        this.clazz = clazz;
    }

    public List<Endpoint> getControllerUrls()
    {
        final Controller controllerAnnotation = getAnnotation(this.clazz, Controller.class);
        if (controllerAnnotation == null) {
            return Collections.emptyList();
        }

        final Set<Endpoint> endpoints = new HashSet<Endpoint>();
        final String value = controllerAnnotation.value();

        final Method[] methods = this.clazz.getDeclaredMethods();
        for (final Method method : methods)
        {
            final RequestMapping annotation = method.getAnnotation(RequestMapping.class);
            if (annotation != null)
            {
                final RequestMethod[] requestMethods = annotation.method();

                // Paths can be specified using 2 attributes
                final Set<String> paths = new HashSet<String>();
                paths.addAll(Arrays.asList(annotation.value()));
                paths.addAll(Arrays.asList(annotation.path()));

                for (final RequestMethod requestMethod : requestMethods) {
                    for (final String path : paths) {
                        final String fullPath = this.buildPath(value, path);
                        final Endpoint endpoint = new Endpoint(requestMethod.name(), fullPath);
                        endpoints.add(endpoint);
                    }
                }
            }
        }

        return new ArrayList<Endpoint>(endpoints);
    }

    private String buildPath(final String prefix, final String value) {
        final StringBuilder buf = new StringBuilder();
        if (prefix != null) {
            buf.append(prefix);
        }
        if (! ((prefix != null && prefix.endsWith("/")) || (value != null && value.startsWith("/")))) {
            buf.append("/");
        }
        if (value != null) {
            buf.append(value);
        }
        return buf.toString();
    }

    private final Class clazz;
}
