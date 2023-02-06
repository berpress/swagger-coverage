import logging
import os
import pathlib
from os.path import exists

from swagger_coverage.src.models import (
    SwaggerData,
    EndpointStatisticsHtml,
    PercentStatistic,
)
from swagger_coverage.src.report import ReportHtml
from swagger_coverage.src.singltone_like import Singleton
from swagger_coverage.src.swagger_diff import DataDiff
from swagger_coverage.src.files import FileOperation
from swagger_coverage.src.prepare_data import PrepareData
from swagger_coverage.src.utils import to_dict, merge_results

logger = logging.getLogger("swagger")


class SwaggerCoverage(metaclass=Singleton):
    """
    Tool for calculating status coverage in api tests
    First, you need to create a file for verification, for example

        swagger = SwaggerCoverage(url='https://test.com', status_codes=[200, 400],
            path='/report')
        swagger.create_coverage_data()


    Where you need to specify a link to the swagger.

    Second, use html report

        swagger_rep.create_report()

    Report will be created in the folder './report/index.html'
    """

    _TEST_SWAGGER_FILE_NAME = "data_swagger.yaml"
    _SWAGGER_REPORT_DIR = "swagger_report"
    _DEFAULT_STATUS_CODE = [200, 400, 401, 403]

    def __init__(
        self,
        url: str = None,
        api_url: str = None,
        status_codes: list = None,
        path: str = None,
    ):
        """
        Init Swagger Coverage
        :param url:
        :param api_url:
        :param status_codes:
        :param path:
        """
        self.url = url
        self.api_url = api_url
        self.paths = None
        self.prepare_data = None
        if status_codes is None:
            self.status_codes = self._DEFAULT_STATUS_CODE
        else:
            self.status_codes = [int(s) for s in status_codes]
        self.path = self._prepare_path(path=path)
        self.data = SwaggerData()
        self.report = ReportHtml
        self.file = FileOperation
        self.prepare = PrepareData
        self.diff = DataDiff()

    def _prepare_path(self, path: str) -> str:
        """
        param path: parth to report dir, for example '/report'
        :return: return path to report dir
        """
        if path is None:
            parent_dir = os.path.abspath(os.path.abspath(os.curdir))
            return os.path.join(parent_dir, self._SWAGGER_REPORT_DIR)
        parent_dir = os.path.abspath(os.path.abspath(os.curdir))
        path = path[1:] if path.find("/") == 0 else path
        return os.path.join(parent_dir, path)

    def create_coverage_data(self, file_name: str = _TEST_SWAGGER_FILE_NAME):
        """
        Create coverage data
        """
        self.file.create_dir(self.path)
        path_to_file = self.file.get_path_to_file(self.path, file_name)
        if exists(path_to_file) is False:
            self.paths = self.prepare.load_swagger(self.url)
            self.prepare_data = self.prepare.prepare_swagger_data(
                data=self.paths, status_codes=self.status_codes
            )
            self.file.save_yaml(path_file=path_to_file, data=self.prepare_data)
        dict_data = self.file.load_yaml(path_to_file=path_to_file)
        data_new = self.prepare.prepare_check_file_data(dict_data)
        self.data.swagger_data = data_new
        logger.info("Data coverage creation completed successfully")

    @staticmethod
    def create_results_from_json(path: str = None):
        # Load data from json files
        parent_dir = os.path.abspath(os.path.abspath(os.curdir))
        path_to_results = os.path.join(parent_dir, "swagger_report", "json_results")
        get_all_files = list(pathlib.Path(path_to_results).glob("*.json"))
        results = merge_results(get_all_files)
        api_url = results.get("api_url")
        swagger_url = results.get("swagger_url")
        summary_dict = results.get("data").get("summary")
        if not path:
            path = results.get("path")
        summary_class = (
            EndpointStatisticsHtml(
                endpoints=summary_dict[0].get("endpoints"),
                checked_endpoints=summary_dict[0].get("checked_endpoints"),
                not_checked_endpoints=summary_dict[0].get("not_checked_endpoints"),
                not_added_endpoints=summary_dict[0].get("not_added_endpoints"),
            ),
            PercentStatistic(
                summary_dict[1].get("success"), summary_dict[1].get("failed")
            ),
        )
        data_class = SwaggerData(
            swagger_data=results.get("data").get("swagger_data"),
            diff=results.get("data").get("diff"),
            summary=summary_class,
        )
        reporter = ReportHtml(
            path=path, api_url=api_url, swagger_url=swagger_url, data=data_class
        )
        reporter.save_html()

    def save_results(self, path: str = None):
        """
        Save result in json file
        :return:
        """
        paths = self.prepare.load_swagger(self.url)
        if self.prepare_data is None:
            self.prepare_data = self.prepare.prepare_swagger_data(
                data=paths, status_codes=self.status_codes
            )
        data = self.diff.result_diff(
            self.data, self.data.swagger_data, self.prepare_data
        )
        self.report(
            api_url=self.api_url,
            swagger_url=self.url,
            data=data,
            path=self.path,
        )
        if path is None:
            path = self.path
        data_dict = {
            "data": to_dict(self.data),
            "api_url": self.api_url,
            "swagger_url": self.url,
            "path": self.path,
        }
        self.file.save_json(data_dict, path)

    def create_report(self):
        """
        Save result in html file
        :return:
        """
        paths = self.prepare.load_swagger(self.url)
        if self.prepare_data is None:
            self.prepare_data = self.prepare.prepare_swagger_data(
                data=paths, status_codes=self.status_codes
            )
        reporter = self.report(
            api_url=self.api_url,
            swagger_url=self.url,
            data=self.diff.result_diff(
                self.data, self.data.swagger_data, self.prepare_data
            ),
            path=self.path,
        )
        reporter.save_html()
