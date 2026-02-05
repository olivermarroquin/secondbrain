"""CBAPS API Tests"""
import pytest
from .api_helper import APIHelper

@pytest.mark.api
class TestCBAPSAPI:
    def test_get_requisitions(self):
        response = APIHelper.get("/requisitions")
        APIHelper.validate_status(response, 200)
        assert "data" in response.json()
    
    def test_create_requisition_via_api(self):
        data = {"title": "API Test", "fund_type": "Operations"}
        response = APIHelper.post("/requisitions", data)
        APIHelper.validate_status(response, 201)
        assert "id" in response.json()
