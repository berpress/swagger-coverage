from datetime import datetime

import requests

from swagger_coverage.src.coverage import SwaggerCoverage
from swagger_coverage.src.deco import swagger

SWAGGER_URL = "https://petstore.swagger.io/v2/swagger.json"


@swagger("regUser")
def register_user(payload: dict):
    return requests.post(
        "https://stores-tests-api.herokuapp.com/register", json=payload
    )


class TestSwagger:
    def test_swagger_files_exist(self, path="report"):
        """
        Checking that files have been created
        """
        swagger_url = "https://api.swaggerhub.com/apis/berpress/flask-rest-api/1.0.0"
        api_url = "https://api.swaggerhub.com/apis/"
        status_codes = [200, 400]
        swagger = SwaggerCoverage(
            url=swagger_url, api_url=api_url, status_codes=status_codes, path=path
        )
        swagger.create_coverage_data(file_name="data.yaml")

        # test
        dt = datetime.now()
        data = {
            "username": f"test_{datetime.timestamp(dt)}@test.com",
            "password": "Password",
        }
        response = register_user(data)
        assert response.status_code == 201

        swagger.create_report()
