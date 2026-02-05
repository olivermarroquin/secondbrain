package com.automation.cbaps.api;

import org.testng.Assert;
import org.testng.annotations.Test;
import io.restassured.response.Response;
import com.automation.cbaps.models.RequisitionData;

/**
 * CBAPS API Tests using REST Assured
 */
public class CBAPS_APITests {
    
    @Test(description = "Test GET requisitions endpoint")
    public void testGetRequisitions() {
        Response response = APIHelper.get("/requisitions");
        
        APIHelper.validateStatusCode(response, 200);
        
        int count = response.jsonPath().getList("data").size();
        Assert.assertTrue(count >= 0, "Should return requisitions list");
    }
    
    @Test(description = "Test POST create requisition via API")
    public void testCreateRequisitionAPI() {
        RequisitionData data = new RequisitionData(
            "API Test Requisition",
            "API created requisition",
            "Operations",
            "Medium"
        );
        
        Response response = APIHelper.post("/requisitions", data);
        APIHelper.validateStatusCode(response, 201);
        
        String reqId = response.jsonPath().getString("id");
        Assert.assertNotNull(reqId, "Should return requisition ID");
    }
    
    @Test(description = "Test GET specific requisition")
    public void testGetRequisitionById() {
        String reqId = "REQ-12345";
        Response response = APIHelper.get("/requisitions/" + reqId);
        
        APIHelper.validateStatusCode(response, 200);
        
        String status = response.jsonPath().getString("status");
        Assert.assertNotNull(status, "Should return requisition status");
    }
    
    @Test(description = "Test DELETE requisition")
    public void testDeleteRequisition() {
        String reqId = "REQ-DRAFT-001";
        Response response = APIHelper.delete("/requisitions/" + reqId);
        
        APIHelper.validateStatusCode(response, 204);
    }
}
