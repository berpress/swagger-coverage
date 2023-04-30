from swagger_coverage.src.files import save_results_to_json
from swagger_coverage.src.models.swagger_data import SwaggerData
from swagger_coverage.src.prepare_data import PrepareData
from swagger_coverage.src.requests import load_swagger
from swagger_coverage.src.results.swagger_diff import SwaggerDiff
from swagger_coverage.src.results.swagger_summary import SwaggerSummary


class SwaggerResults:
    def __init__(self, data):
        self.results = data.data
        self.swagger_url = data.swagger_url
        self.path = data.path
        self.api_url = data.api_url
        self.status_codes = data.status_codes

    def save_results(self, path: str):
        """
        Save result in json file
        :return:
        """
        load_data = load_swagger(self.swagger_url)
        prepare = PrepareData()
        prepare_data = prepare.prepare_swagger_data(
            data=load_data, status_codes=self.status_codes
        )
        diff = SwaggerDiff(
            local_swagger=self.results.swagger_data, actual_swagger=prepare_data
        )
        swagger_diff = diff.get_diff()
        summary = SwaggerSummary(self.results.swagger_data, swagger_diff)
        swagger_summary = summary.get_summary()
        swagger_data = SwaggerData(
            swagger_data=self.results.swagger_data,
            summary=swagger_summary,
            diff=swagger_diff,
            url=self.api_url,
        )
        return save_results_to_json(swagger_data, path)
