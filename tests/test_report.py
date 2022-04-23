import os

from os.path import exists, dirname, abspath


from swagger_coverage.coverage import SwaggerCoverage


SWAGGER_URL = "https://petstore.swagger.io/v2/swagger.json"


class TestSReport:
    def test_report_files_exist(self, path="report"):
        """
        Checking that html files have been created
        """
        url = SWAGGER_URL
        status_codes = [200, 400]
        swagger = SwaggerCoverage(
            url=url, api_url="api_test.com", status_codes=status_codes, path=path
        )
        swagger.create_coverage_data(file_name="swagger_files_exist.yaml")
        swagger.create_report()
        report_path = os.path.join(
            dirname(dirname(abspath(__file__))), path, "index.html"
        )  # noqa
        assert exists(report_path)
