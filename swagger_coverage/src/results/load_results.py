from pathlib import Path
from typing import List

from swagger_coverage.src.files import load_json
from swagger_coverage.src.models.swagger_data import SwaggerData

from swagger_coverage.src.results.swagger_summary import SwaggerSummary


class LoadSwaggerResults:
    def _calculate_list_dict_res(self, res1: list, res2: list):
        res = res1 + res2
        total = {}
        for item in res:
            for key, val in item.items():
                if key in total:
                    total[key] += val
                else:
                    total[key] = val
        return [{k: v} for k, v in total.items()]

    def merge_results(self, paths: List[Path]) -> SwaggerData:
        """
        merge results in one obj (dict)
        need, for example, if you use pytest xdist
        """
        results = []
        for path in paths:
            results.append(load_json(str(path)))
        if len(results) == 1:
            summary = SwaggerSummary(
                results[0].get("swagger_data"), results[0].get("diff")
            )
            swagger_summary = summary.get_summary()
            return SwaggerData(
                swagger_data=results[0].get("swagger_data"),
                summary=swagger_summary,
                diff=results[0].get("diff"),
                url=results[0].get("url"),
            )

        sum_res = {}
        for res in results:
            if sum_res.get("diff") is None:
                sum_res["diff"] = res.get("diff")
            if sum_res.get("url") is None:
                sum_res["url"] = res.get("url")
            if sum_res.get("swagger_data") is None:
                sum_res["swagger_data"] = {}
            sw_data = res["swagger_data"]
            for key, value in sw_data.items():
                if sum_res.get("swagger_data").get(key) is None:
                    sum_res["swagger_data"][key] = value
                else:
                    sum_list_statuses = sum_res.get("swagger_data").get(key)["statuses"]
                    current_list_statuses = value["statuses"]
                    sum_list_statuses = self._calculate_list_dict_res(
                        sum_list_statuses, current_list_statuses
                    )
                    sum_res.get("swagger_data").get(key)["statuses"] = sum_list_statuses
        summary = SwaggerSummary(sum_res.get("swagger_data"), sum_res.get("diff"))
        swagger_summary = summary.get_summary()
        return SwaggerData(
            swagger_data=sum_res.get("swagger_data"),
            summary=swagger_summary,
            diff=sum_res.get("diff"),
            url=sum_res.get("url"),
        )
