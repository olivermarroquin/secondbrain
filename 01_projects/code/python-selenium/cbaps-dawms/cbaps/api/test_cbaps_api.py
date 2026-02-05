import pytest
from .api_helper import APIHelper

@pytest.mark.api
class TestCBAPSAPI:
    def test_get_requisitions(self):
        response = APIHelper.get("/requisitions")
        assert response.status_code == 200
    
    def test_create_requisition_via_api(self):
        data = {"title": "API Test", "fund_type": "Operations"}
        response = APIHelper.post("/requisitions", data)
        assert response.status_code == 201
