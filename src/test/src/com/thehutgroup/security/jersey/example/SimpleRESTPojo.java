package com.thehutgroup.security.jersey.example;

import javax.ws.rs.*;

@Path("/pojo")
public class SimpleRESTPojo {
    @GET
    public String pojo() {
        return "pojo ok";
    }

    @Path("{c}")
    @POST
    @Produces("application/xml")
    public String withPathParam(@PathParam("c") Double c) {
        return "it's 42";
    }
}