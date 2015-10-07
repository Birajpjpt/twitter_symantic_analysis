package com.thehutgroup.security.jersey;

import javax.ws.rs.DELETE;
import javax.ws.rs.GET;
import javax.ws.rs.HEAD;
import javax.ws.rs.OPTIONS;
import javax.ws.rs.POST;
import javax.ws.rs.PUT;
import javax.ws.rs.Path;
import javax.ws.rs.core.Application;
import java.lang.annotation.Annotation;
import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.LinkedList;
import java.util.List;
import java.util.Set;

public class JerseyTestUtils {

    private static final Set<Class<?>> ENDPOINT_ANNOTATIONS =
            new HashSet<Class<?>>(Arrays.<Class<?>>asList(GET.class, POST.class, PUT.class, DELETE.class, HEAD.class, OPTIONS.class));

    public static List<String> getAllRESTfulEndpoints(Application application) {
        List<String> endpoints = new ArrayList<>();

        for (Class<?> aClass : application.getClasses()) {
            if (!isAnnotatedResourceClass(aClass)) {
                continue;
            }

            String classPath = getPath(aClass);

            for (Method method : aClass.getMethods()) {
                if (!isEndpointMethod(method)) {
                    continue;
                }

                String methodPath = getPath(method);

                endpoints.add(getFullPath(classPath, methodPath));
            }
        }

        return endpoints;
    }

    private static <T> boolean isAnnotatedResourceClass(Class<T> rc) {
        if (rc.isAnnotationPresent(Path.class)) {
            return true;
        }

        for (Class<?> i : rc.getInterfaces()) {
            if (i.isAnnotationPresent(Path.class)) {
                return true;
            }
        }

        return false;
    }

    private static boolean isEndpointMethod(Method method) {
        for (Annotation annotation : method.getAnnotations()) {
            if (ENDPOINT_ANNOTATIONS.contains(annotation.annotationType())) {
                return true;
            }
        }
        return false;
    }

    private static <T> String getPath(Class<T> aClass) {
        return getSingleAnnotationValue(getAnnotationsByType(aClass, Path.class));
    }

    private static String getPath(Method method) {
        return getSingleAnnotationValue(getAnnotationsByType(method, Path.class));
    }

    private static String getSingleAnnotationValue(List<Annotation> annotations) {
        if (annotations.size() == 0) {
            return "";
        } else if (annotations.size() == 1) {
            return ((Path)annotations.get(0)).value();
        } else {
            throw new IllegalArgumentException("Multiple @Path annotations found");
        }
    }

    private static List<Annotation> getAnnotationsByType(Class<?> aClass, Class<?> annotationClass) {
        List<Annotation> result = new LinkedList<Annotation>();
        for (Annotation annotation : aClass.getAnnotations()) {
            if (annotation.annotationType().equals(annotationClass)) {
                result.add(annotation);
            }
        }
        return result;
    }

    private static List<Annotation> getAnnotationsByType(Method method, Class<?> annotationClass) {
        List<Annotation> result = new LinkedList<Annotation>();
        for (Annotation annotation : method.getAnnotations()) {
            if (annotation.annotationType().equals(annotationClass)) {
                result.add(annotation);
            }
        }
        return result;
    }

    private static String getFullPath(String classPath, String methodPath) {
        if (classPath.length() > 0 && methodPath.length() > 0) {
            return classPath + "/" + methodPath;
        } else {
            return classPath + methodPath;
        }
    }

}
