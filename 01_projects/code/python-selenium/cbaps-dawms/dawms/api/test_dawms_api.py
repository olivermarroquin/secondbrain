import pytest
from .api_helper import APIHelper

@pytest.mark.api
class TestDAWMSAPI:
    def test_get_submissions(self):
        response = APIHelper.get("/submissions")
        assert response.status_code == 200
    
    def test_create_submission_via_api(self):
        data = {"type": "NDA", "app_number": "APP-123"}
        response = APIHelper.post("/submissions", data)
        assert response.status_code == 201
