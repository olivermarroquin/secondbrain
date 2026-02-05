package com.playwright.cbaps.api;

import io.restassured.RestAssured;
import io.restassured.response.Response;
import io.restassured.http.ContentType;
import static io.restassured.RestAssured.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * REST Assured APIHelper for API testing
 */
public class APIHelper {
    private static final Logger log = LoggerFactory.getLogger(APIHelper.class);
    private static final String BASE_URL = "https://api.cbaps.example.com";
    
    static { RestAssured.baseURI = BASE_URL; }
    
    public static Response get(String endpoint) {
        log.info("📡 GET: {}", endpoint);
        Response r = given().contentType(ContentType.JSON).when().get(endpoint).then().extract().response();
        log.info("✅ Status: {}", r.getStatusCode());
        return r;
    }
    
    public static Response post(String endpoint, Object body) {
        log.info("📡 POST: {}", endpoint);
        Response r = given().contentType(ContentType.JSON).body(body).when().post(endpoint).then().extract().response();
        log.info("✅ Status: {}", r.getStatusCode());
        return r;
    }
    
    public static void validateStatusCode(Response r, int expected) {
        int actual = r.getStatusCode();
        if (actual == expected) log.info("✅ Status validated: {}", actual);
        else { log.error("❌ Status mismatch: Expected {}, Got {}", expected, actual); throw new AssertionError(); }
    }
}
