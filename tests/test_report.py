import os

from os.path import exists, dirname, abspath


from test_swagger_coverage.report import ReportHtml
from test_swagger_coverage.swagger_coverage import Swagger

SWAGGER_URL = 'https://petstore.swagger.io/v2/swagger.json'


class TestSReport:
    def test_report_files_exist(self):
        """
        Checking that html files have been created
        """
        url = SWAGGER_URL
        status_codes = [200, 400]
        swagger = Swagger(url=url, status_codes=status_codes)
        swagger.create_coverage_data(file_name='swagger_files_exist.yaml')
        reporter = ReportHtml(
            api_url=SWAGGER_URL, swagger_url=SWAGGER_URL, data=swagger.result()
        )
        reporter.save_html(is_copy=False)
        report_path = os.path.join(dirname(dirname(abspath(__file__))), 'tests',
                                   'swagger_report', 'index.html')  # noqa
        assert exists(report_path)