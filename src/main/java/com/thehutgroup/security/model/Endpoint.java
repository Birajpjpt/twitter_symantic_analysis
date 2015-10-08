package com.thehutgroup.security.model;

import org.apache.commons.lang.StringUtils;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by nevinc on 07/10/2015.
 */
public class Endpoint {

    private String httpMethod;
    private String path;

    public Endpoint(String httpMethod, String path) {
        this.httpMethod = httpMethod;
        this.path = path;
    }

    public String getHttpMethod() {
        return httpMethod;
    }

    public void setHttpMethod(String httpMethod) {
        this.httpMethod = httpMethod;
    }

    public String getPath() {
        return path;
    }

    public void setPath(String path) {
        this.path = path;
    }

    public Endpoint(String httpMethod, String path, List<String> params) {
        this.httpMethod = httpMethod;
        if(params != null && params.size() > 0){
            List<String> queryParams = new ArrayList<String>();
            for(String query: params){
                queryParams.add("[" + query + "]");
            }
            this.path = path + "?" + StringUtils.join(queryParams, "&");
        } else {
            this.path = path;
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
}
