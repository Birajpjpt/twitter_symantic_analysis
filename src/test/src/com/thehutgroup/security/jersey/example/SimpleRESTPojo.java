package com.thehutgroup.security.jersey.example;

import javax.ws.rs.*;
import java.util.Date;

@Path("/pojo")
public class SimpleRESTPojo {
    @GET
    public String pojo() {
        return "pojo ok @ " + new Date().toString();
    }

    @Path("{c}")
    @POST
    @Produces("application/xml")
    public String withPathParam(@PathParam("c") Double c) {
        return "it's 42";
    }
}