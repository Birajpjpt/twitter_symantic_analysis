package com.thehutgroup.security.util;

import java.lang.annotation.Annotation;

public class AnnotationUtil
{
    public static boolean isAnnotationPresent(final Class clazz,
                                              final Class<? extends Annotation> annotation) {
        if (clazz == null ) {
            throw new IllegalArgumentException("clazz is null!");
        }
        if (annotation == null) {
            return false;
        }

        if (clazz.isAnnotationPresent(annotation)) {
            return true;
        }

        for (final Class i : clazz.getInterfaces()) {
            if (i.isAnnotationPresent(annotation)) {
                return true;
            }
        }

        return false;
    }

    public static <T extends Annotation> T getAnnotation(final Class clazz, final Class<T> annotation) {

        final T classAnnotation = (T) clazz.getAnnotation(annotation);
        return classAnnotation;
    }

    private AnnotationUtil() {}
}
