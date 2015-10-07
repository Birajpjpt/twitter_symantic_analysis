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

    public Endpoint(String httpMethod, String path, List<String> params) {
        this.httpMethod = httpMethod;
        if(params != null && params.size() > 0){
            List<String> queryParams = new ArrayList<>();
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

        if (httpMethod != null ? !httpMethod.equals(endpoint.httpMethod) : endpoint.httpMethod != null) return false;
        return !(path != null ? !path.equals(endpoint.path) : endpoint.path != null);

    }

    @Override
    public int hashCode() {
        int result = httpMethod != null ? httpMethod.hashCode() : 0;
        result = 31 * result + (path != null ? path.hashCode() : 0);
        return result;
    }
}
