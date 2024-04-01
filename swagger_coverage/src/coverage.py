from typing import List

from swagger_coverage.src.files import (
    prepare_path,
    create_dir,
    get_path_to_file,
    is_file_exist,
    save_yaml,
    load_yaml,
    get_json_result_path,
)
from swagger_coverage.src.models.swagger_data import SwaggerData
from swagger_coverage.src.prepare_data import PrepareData
from swagger_coverage.src.report.html.html_report import HtmlReport
from swagger_coverage.src.requests import load_swagger
from swagger_coverage.src.results.load_results import LoadSwaggerResults
from swagger_coverage.src.results.swagger_results import SwaggerResults
from swagger_coverage.src.singltone_like import Singleton

_TEST_SWAGGER_FILE_NAME = "data_swagger.yaml"
_SWAGGER_REPORT_DIR = "swagger_report"
_DEFAULT_STATUS_CODE = [200, 400, 401, 403]


class SwaggerCoverage(metaclass=Singleton):
    def __init__(
            self,
            url: str = None,
            urls: List[str] = None,
            api_url: str = None,
            status_codes: List[int] = None,
            path: str = _SWAGGER_REPORT_DIR,
    ):
        """
        :param url: Swagger url, example https://petstore.swagger.io/v2/swagger.json # noqa
        :param api_url: Api url, example https://petstore3.swagger.io/
        :param status_codes: List off status codes, example [200, 400]
        :param path: path to
        """
        self.swagger_url = self._select_urls(url, urls)
        self.api_url = api_url
        if status_codes is None:
            self.status_codes = _DEFAULT_STATUS_CODE
        else:
            self.status_codes = [int(s) for s in status_codes]
        self.path = prepare_path(path=path, report_dir=_SWAGGER_REPORT_DIR)
        self.data = SwaggerData()
        self.path_to_file = None

    # parent_dir = get_parent_dir()
    # path_to_results = get_path_results(parent_dir, _SWAGGER_REPORT_DIR)

    def create_coverage_data(self, file_name: str = _TEST_SWAGGER_FILE_NAME):
        """
        Create coverage data
        """
        create_dir(self.path)
        self.path_to_file = get_path_to_file(self.path, file_name)
        if not is_file_exist(path=self.path_to_file):
            load_data = load_swagger(self.swagger_url)
            prepare = PrepareData()
            prepare_data = prepare.prepare_swagger_data(
                data=load_data, status_codes=self.status_codes
            )
            save_yaml(path_file=self.path_to_file, data=prepare_data)
        self._prepare_exist_swagger()

    def _select_urls(self, url: str, urls: str):
        if url:
            return [url]
        if len(urls) > 0:
            return urls
        return None

    def _prepare_exist_swagger(self):
        dict_data = load_yaml(path_to_file=self.path_to_file)
        prepare = PrepareData()
        self.data.swagger_data = prepare.prepare_check_file_data(dict_data)

    def save_results(self) -> str:
        results = SwaggerResults(self)
        return results.save_results(self.path)

    def create_report(self, path=_SWAGGER_REPORT_DIR, report_type="html"):
        # merge results
        result_path = f"{path}/json_results"
        if not is_file_exist(result_path):
            create_dir(self.path)
        self.save_results()
        result_paths = get_json_result_path(path=result_path)
        load_results = LoadSwaggerResults()
        merge_result = load_results.merge_results(result_paths)
        # create report
        report = HtmlReport(merge_result)
        report.create(path)
