package com.playwright.dawms.api;
import io.restassured.RestAssured;
import io.restassured.response.Response;
import io.restassured.http.ContentType;
import static io.restassured.RestAssured.*;

public class APIHelper {
    private static final String BASE_URL = "https://api.dawms.example.com";
    static { RestAssured.baseURI = BASE_URL; }
    
    public static Response get(String endpoint) {
        return given().contentType(ContentType.JSON).when().get(endpoint).then().extract().response();
    }
    
    public static Response post(String endpoint, Object body) {
        return given().contentType(ContentType.JSON).body(body).when().post(endpoint).then().extract().response();
    }
}
