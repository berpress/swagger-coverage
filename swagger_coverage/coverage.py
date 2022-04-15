import copy
import logging
import os
from os.path import exists
from typing import Dict

import yaml
import requests

from swagger_coverage.models import (
    SwaggerData,
    EndpointStatisticsHtml,
    PercentStatistic,
)
from swagger_coverage.report import ReportHtml
from swagger_coverage.singltone_like import Singleton

logger = logging.getLogger("swagger")


class SwaggerCoverage(metaclass=Singleton):
    """
    Tool for calculating status coverage in api tests
    First, you need to create a file for verification, for example

        swagger = SwaggerCoverage(url='https://test.com', status_codes=[200, 400])
        swagger.create_coverage_data()


    Where you need to specify a link to the swagger.

    Second, use html report

        ReportHtml(
            api_url='https://test.com', swagger_url='https://test.com',
            data=swagger.result()
        )

    Report will be created in the folder 'swagger_report/index.html'
    """

    _TEST_SWAGGER_FILE_NAME = "data_swagger.yaml"
    _SWAGGER_REPORT_DIR = "swagger_report"
    _DEFAULT_STATUS_CODE = [200, 400, 401, 403]

    def __init__(
        self,
        url: str = None,
        api_url: str = None,
        status_codes: list = None,
    ):
        """
        Init Swagger Coverage
        :param url:
        :param api_url:
        :param status_codes:
        """
        self.url = url
        self.path_dict = None
        self.data = SwaggerData()
        self.prepare_data = None
        self.api_url = api_url
        if status_codes is None:
            self.status_codes = self._DEFAULT_STATUS_CODE
        else:
            self.status_codes = [int(s) for s in status_codes]

    def _save_file(self, data: dict, path_file: str) -> None:
        """
        Try so safe test data in ${TEST_SWAGGER_FILE_NAME} file
        :param data: dict data
        :param file_name: file name, default TEST_SWAGGER_FILE_NAME
        :return: None
        """
        with open(path_file, "w") as outfile:
            yaml.Dumper.ignore_aliases = lambda self, data: True
            yaml.dump(data, outfile, default_flow_style=False, Dumper=yaml.Dumper)

    @staticmethod
    def _create_dir(dir_name):
        if not exists(dir_name):
            os.mkdir(dir_name)

    def _prepare_swagger_data(self, data) -> dict:
        """
        Preparing data for tests
        :param data:
        :return: swagger dict
        """
        res_dict = {}
        for key, value in data.items():
            list_values = list(value.values())
            for values in list_values:
                res_dict[values.get("operationId")] = []
            for k, v in value.items():
                res_dict[v.get("operationId")] = {
                    "method": k.upper(),
                    "description": v.get("description"),
                    "path": key,
                    "statuses": self.status_codes,
                    "tag": v.get("tags")[0],
                }
        return res_dict

    def _load_swagger(self) -> Dict:
        """
        Load and get swagger data
        """
        logger.info(f"Start load swagger {self.url}")
        res = requests.get(self.url)
        if res.status_code == 200:
            try:
                data = yaml.safe_load(res.text)
                self.path_dict = data.get("paths")
                return data.get("paths")
            except Exception:
                raise ValueError("Couldn't load yaml")
        else:
            logger.error(f"Couldn't get the file, status code is {res.status_code}")

    def _create_swagger_test_file(
        self, is_safe: bool = False, path_file: str = None
    ) -> None:
        """
        Create file for tests
        Prepare loaded swagger data
        """
        if self.path_dict is None:
            logger.error("Couldn't load yaml")
        else:
            prepare_data = self._prepare_swagger_data(self.path_dict)
            self.prepare_data = prepare_data
            if is_safe:
                self._save_file(prepare_data, path_file)

    def swagger_check(self, key, res) -> None:
        """
        Try to check response status code and swagger data
        """
        swagger_data = self.data
        dict_data = copy.deepcopy(swagger_data)
        new_data = self._set_check_result(key, res.status_code, dict_data)
        self.data = new_data

    @staticmethod
    def _set_check_result(key, status_code, data) -> dict:
        """
        Set check result
        """
        endpoint = data.swagger_data.get(key)
        if endpoint:
            statuses = endpoint.get("statuses")
            for status in statuses:
                for key in status.keys():
                    if key == status_code:
                        status[key] = status.get("key", 0) + 1
                        return data
        return data

    def _data_diff(self, swagger_data: dict, file_data: dict) -> dict:
        """
        Get diff between swagger and checked file
        """
        prepare_data = self._prepare_swagger_data(swagger_data)
        diff = {k: prepare_data[k] for k in set(prepare_data) - set(file_data)}
        return diff

    @staticmethod
    def _prepare_check_file_data(data: dict) -> dict:
        """
        Prepare data for check
        """
        for k, value in data.items():
            statuses = value.get("statuses")
            if statuses:
                new_statuses = []
                for s in statuses:
                    new_statuses.append({s: 0})
                value["statuses"] = new_statuses
        return data

    def create_coverage_data(self, file_name: str = _TEST_SWAGGER_FILE_NAME) -> None:
        """
        Create coverage data
        """
        parent_dir = os.path.abspath(os.path.abspath(os.curdir))
        swagger_dir = os.path.join(parent_dir, self._SWAGGER_REPORT_DIR)
        self._create_dir(swagger_dir)
        path_to_file = os.path.join(parent_dir, self._SWAGGER_REPORT_DIR, file_name)
        if exists(path_to_file) is False:
            self._load_swagger()
            self._create_swagger_test_file(is_safe=True, path_file=path_to_file)
        with open(path_to_file, "r") as stream:
            data_loaded = yaml.safe_load(stream)
            dict_data = copy.deepcopy(data_loaded)
            data_new = self._prepare_check_file_data(dict_data)
            self.data.swagger_data = data_new
        logger.info("Data coverage creation completed successfully")

    def _get_summary(self, diff: dict) -> [EndpointStatisticsHtml, PercentStatistic]:
        """
        Calculate report summary
        """
        count_success = 0
        count_of_unverified = 0
        data = copy.deepcopy(self.data.swagger_data)
        for key, value in data.items():
            is_checked_list = [
                list(status.values())[0] for status in value.get("statuses")
            ]
            count_success += len([status for status in is_checked_list if status > 0])
            count_of_unverified += len(
                [status for status in is_checked_list if status == 0]
            )
        count_diff = len(list(diff.items()))
        count_total = count_success + count_of_unverified
        # get percent
        percentage_success = self._percentage(count_success, count_total)
        percentage_unverified = self._percentage(count_of_unverified, count_total)
        return (
            EndpointStatisticsHtml(
                count_total, count_success, count_of_unverified, count_diff
            ),
            PercentStatistic(percentage_success, percentage_unverified),
        )

    @staticmethod
    def _percentage(part, whole) -> str:
        """
        Calculate percentage of verified statuses
        """
        res = 100 * float(part) / float(whole)
        return format(res, ".1f")

    def _swagger_diff(self):
        """
        Get swagger diff
        """
        if self.path_dict is None:
            swagger_data = self._load_swagger()
        else:
            swagger_data = copy.deepcopy(self.path_dict)
        return self._data_diff(swagger_data, self.data.swagger_data)

    def _result(self):
        """
        Get swagger check result, need for build html report
        """
        self.data.diff = self._swagger_diff()
        self.data.summary = self._get_summary(self.data.diff)
        return self.data

    def create_report(self):
        """
        Save result in html file
        :return:
        """
        reporter = ReportHtml(
            api_url=self.api_url, swagger_url=self.url, data=self._result()
        )
        reporter.save_html()
