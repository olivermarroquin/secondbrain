package com.playwright.dawms.api;
import org.testng.Assert;
import org.testng.annotations.Test;
import io.restassured.response.Response;

public class DAWMS_APITests {
    @Test
    public void testGetSubmissions() {
        Response response = APIHelper.get("/submissions");
        Assert.assertEquals(response.getStatusCode(), 200);
    }
}
