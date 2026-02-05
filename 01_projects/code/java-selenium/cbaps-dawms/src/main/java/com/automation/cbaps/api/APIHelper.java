package com.automation.cbaps.api;

import io.restassured.RestAssured;
import io.restassured.response.Response;
import io.restassured.specification.RequestSpecification;
import io.restassured.http.ContentType;
import static io.restassured.RestAssured.*;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

/**
 * APIHelper - REST Assured helper for API testing
 * Provides common methods for GET, POST, PUT, DELETE requests
 */
public class APIHelper {
    private static final Logger log = LogManager.getLogger(APIHelper.class);
    private static final String BASE_URL = "https://api.cbaps.example.com";
    
    static {
        RestAssured.baseURI = BASE_URL;
    }
    
    public static Response get(String endpoint) {
        log.info("📡 GET Request: " + endpoint);
        Response response = given()
            .contentType(ContentType.JSON)
            .when()
            .get(endpoint)
            .then()
            .extract().response();
        
        log.info("✅ Response Status: " + response.getStatusCode());
        return response;
    }
    
    public static Response post(String endpoint, Object body) {
        log.info("📡 POST Request: " + endpoint);
        Response response = given()
            .contentType(ContentType.JSON)
            .body(body)
            .when()
            .post(endpoint)
            .then()
            .extract().response();
        
        log.info("✅ Response Status: " + response.getStatusCode());
        return response;
    }
    
    public static Response put(String endpoint, Object body) {
        log.info("📡 PUT Request: " + endpoint);
        Response response = given()
            .contentType(ContentType.JSON)
            .body(body)
            .when()
            .put(endpoint)
            .then()
            .extract().response();
        
        log.info("✅ Response Status: " + response.getStatusCode());
        return response;
    }
    
    public static Response delete(String endpoint) {
        log.info("📡 DELETE Request: " + endpoint);
        Response response = given()
            .contentType(ContentType.JSON)
            .when()
            .delete(endpoint)
            .then()
            .extract().response();
        
        log.info("✅ Response Status: " + response.getStatusCode());
        return response;
    }
    
    public static void validateStatusCode(Response response, int expectedCode) {
        int actualCode = response.getStatusCode();
        if (actualCode == expectedCode) {
            log.info("✅ Status Code Validation Passed: " + actualCode);
        } else {
            log.error("❌ Status Code Mismatch: Expected " + expectedCode + ", Got " + actualCode);
            throw new AssertionError("Status code mismatch");
        }
    }
}
