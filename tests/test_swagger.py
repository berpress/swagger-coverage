import os

import pytest
import yaml

from os.path import exists, dirname, abspath

from requests.exceptions import MissingSchema

from swagger_coverage.coverage import Swagger

SWAGGER_URL = 'https://petstore.swagger.io/v2/swagger.json'


class TestSwagger:
    def test_swagger_files_exist(self):
        """
        Checking that files have been created
        """
        url = SWAGGER_URL
        status_codes = [200, 400]
        swagger = Swagger(url=url, status_codes=status_codes)
        swagger.create_coverage_data(file_name='swagger_files_exist.yaml')
        report_dir = os.path.join(dirname(dirname(abspath(__file__))), 'swagger_report') # noqa
        assert exists(report_dir)

    def test_swagger_data(self):
        """
        Checking swagger data
        """
        url = SWAGGER_URL
        status_codes = [200, 400]
        swagger = Swagger(url=url, status_codes=status_codes)
        swagger.create_coverage_data(file_name='swagger_data.yaml')
        report_path = os.path.join(dirname(dirname(abspath(__file__))), 'swagger_report', 'swagger_data.yaml') # noqa
        with open(report_path) as f:
            data = yaml.safe_load(f)
        for key, value in data.items():
            assert value.get('statuses') == status_codes

    @pytest.mark.skip(reason='Need destroy singltone class')
    def test_swagger_invalid_url(self):
        """
        Checking with invalid url
        """
        Swagger().clear()
        with pytest.raises(MissingSchema):
            url = 'test.djhdhg'
            status_codes = [200, 400]
            swagger = Swagger(url=url, status_codes=status_codes)
            swagger.create_coverage_data(file_name='swagger_invalid_url.yaml')
            report_dir = os.path.join(dirname(dirname(abspath(__file__))), 'swagger_report') # noqa
            assert exists(report_dir)

    @pytest.mark.skip(reason='Need destroy singltone class')
    def test_swagger_none_exist_url(self, delete_swagger):
        """
        Checking valid url, but not swagger link
        """
        with pytest.raises(ValueError):
            url = 'https://github.com/berpress'
            status_codes = [200, 400]
            swagger = Swagger(url=url, status_codes=status_codes)
            swagger.create_coverage_data(file_name='swagger_none_exist_url.yaml')
            report_dir = os.path.join(dirname(dirname(abspath(__file__))), 'swagger_report') # noqa
            assert exists(report_dir)
