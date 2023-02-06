import json
from typing import List

from swagger_coverage.src.files import FileOperation


def sort_requests_results(data: dict) -> List:
    """
    Sort request result
    """
    results = []
    for key, value in data.items():
        if value.get("time_executions") is not None:
            name = f"{value.get('tag')} ({value.get('method')} {value.get('path')})"
            avg_time = sum(value.get("time_executions")) / len(
                value.get("time_executions")
            )
            if avg_time > 3:
                color = "danger"
            elif avg_time > 1:
                color = "warning"
            else:
                color = "light"
            results.append({"name": name, "results": avg_time, "color": color})
    sorted_results = sorted(results, key=lambda d: d["results"], reverse=True)
    return sorted_results


def to_dict(data) -> dict:
    """
    Convert nested object to dict
    :return: dict
    """
    return json.loads(json.dumps(data, default=lambda o: o.__dict__))


def _get_summary(data):
    summary_res_endpoints = data.get("data").get("summary")[0]
    summary_percent = data.get("data").get("summary")[1]
    endpoints = summary_res_endpoints.get("endpoints")
    checked_endpoints = summary_res_endpoints.get("checked_endpoints")
    not_checked_endpoints = summary_res_endpoints.get("not_checked_endpoints")
    not_added_endpoints = summary_res_endpoints.get("not_added_endpoints")
    success = summary_percent.get("success")
    failed = summary_percent.get("failed")
    return (
        endpoints,
        checked_endpoints,
        not_checked_endpoints,
        not_added_endpoints,
        success,
        failed,
    )


def merge_results(paths: list):
    results = []
    for path in paths:
        results.append(FileOperation.load_json(str(path)))
    summary_res = {}
    for res in results:
        if summary_res.get("summary") is None:
            summary_res["data"] = {"summary": res.get("data").get("summary")}
        else:
            (
                endpoints,
                checked_endpoints,
                not_checked_endpoints,
                not_added_endpoints,
                success,
                failed,
            ) = _get_summary(res)
            summary_res_endpoints = summary_res.get("data").get("summary")[0]
            summary_percent = summary_res.get("data").get("summary")[1]
            summary_res_endpoints["endpoints"] = (
                summary_res_endpoints["endpoints"] + endpoints
            )
            summary_res_endpoints["checked_endpoints"] = (
                summary_res_endpoints["checked_endpoints"] + checked_endpoints
            )
            summary_res_endpoints["not_checked_endpoints"] = (
                summary_res_endpoints["not_checked_endpoints"] + not_checked_endpoints
            )
            summary_res_endpoints["not_added_endpoints"] = (
                summary_res_endpoints["not_added_endpoints"] + not_added_endpoints
            )
            summary_percent["success"] = summary_percent["success"] + success
            summary_percent["failed"] = summary_percent["failed"] + failed
        if summary_res.get("data").get("swagger_data") is None:
            summary_res.get("data")["swagger_data"] = res.get("data").get(
                "swagger_data"
            )
        if summary_res.get("data").get("diff") is None:
            summary_res.get("data")["diff"] = res.get("data").get("diff")
        summary_res.get("data")["diff"] = res.get("data").get("diff") | summary_res.get(
            "data"
        ).get("diff")
        summary_res.get("data")["swagger_data"] = res.get("data").get(
            "swagger_data"
        ) | summary_res.get("data").get("swagger_data")
        summary_res["api_url"] = res.get("api_url")
        summary_res["swagger_url"] = res.get("swagger_url")
        summary_res["path"] = res.get("path")
        summary_res["data"]["diff"] = res["data"].get("diff")
    return summary_res
