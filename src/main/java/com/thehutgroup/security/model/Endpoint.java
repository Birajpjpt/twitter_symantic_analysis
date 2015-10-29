package com.thehutgroup.security.model;

import java.util.ArrayList;
import java.util.List;

import org.apache.commons.lang.StringUtils;

/**
 * Created by nevinc on 07/10/2015.
 */
public class Endpoint implements Comparable<Endpoint> {

    private String httpMethod;
    private String path;

    public Endpoint(String httpMethod, String path) {
        this.setHttpMethod(httpMethod);
        this.setPath(path);
    }

    public String getHttpMethod() {
        return httpMethod;
    }

    public void setHttpMethod(String httpMethod) {
        if (httpMethod == null) {
            this.httpMethod = "";
        } else {
            this.httpMethod = httpMethod;
        }
    }

    public String getPath() {
        return path;
    }

    public void setPath(String path) {
        if (path == null) {
            this.path = "";
        } else {
            this.path = path;
        }
    }

    public Endpoint(String httpMethod, String path, List<String> params) {
        this.setHttpMethod(httpMethod);
        if(params != null && params.size() > 0){
            List<String> queryParams = new ArrayList<String>();
            for(String query: params){
                queryParams.add("[" + query + "]");
            }
            this.setPath(path + "?" + StringUtils.join(queryParams, "&"));
        } else {
            this.setPath(path);
        }
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;

        Endpoint endpoint = (Endpoint) o;

        if (getHttpMethod() != null ? !getHttpMethod().equals(endpoint.getHttpMethod()) : endpoint.getHttpMethod() != null)
            return false;
        return !(getPath() != null ? !getPath().equals(endpoint.getPath()) : endpoint.getPath() != null);

    }

    @Override
    public int hashCode() {
        int result = getHttpMethod() != null ? getHttpMethod().hashCode() : 0;
        result = 31 * result + (getPath() != null ? getPath().hashCode() : 0);
        return result;
    }

    @Override
    public int compareTo(Endpoint o)
    {
        if (o == null) {
            throw new IllegalArgumentException("o is null!");
        }

        final int httpMethodCompare = this.httpMethod.compareTo(o.httpMethod);
        if (httpMethodCompare != 0) {
            return httpMethodCompare;
        }
        return this.path.compareTo(o.path);
    }

    @Override
    public String toString() {
        return httpMethod + '-' + path;
    }
}
