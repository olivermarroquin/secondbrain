package com.playwright.cbaps.api;

import org.testng.Assert;
import org.testng.annotations.Test;
import io.restassured.response.Response;
import com.playwright.cbaps.models.RequisitionData;

/**
 * CBAPS API Tests - REST Assured Integration
 */
public class CBAPS_APITests {
    
    @Test(description = "GET requisitions list")
    public void testGetRequisitions() {
        Response response = APIHelper.get("/requisitions");
        APIHelper.validateStatusCode(response, 200);
        Assert.assertTrue(response.jsonPath().getList("data").size() >= 0);
    }
    
    @Test(description = "POST create requisition via API")
    public void testCreateRequisitionAPI() {
        RequisitionData data = new RequisitionData("API Test", "API created", "Operations", "High");
        Response response = APIHelper.post("/requisitions", data);
        APIHelper.validateStatusCode(response, 201);
        Assert.assertNotNull(response.jsonPath().getString("id"));
    }
    
    @Test(description = "GET specific requisition by ID")
    public void testGetRequisitionById() {
        Response response = APIHelper.get("/requisitions/REQ-12345");
        APIHelper.validateStatusCode(response, 200);
        Assert.assertNotNull(response.jsonPath().getString("status"));
    }
}
