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


def merge_results(paths: list):
    results = []
    for path in paths:
        results.append(FileOperation.load_json(str(path)))
    summary_res = {}
    for res in results:
        summary_res = res | summary_res
        pass
    return summary_res
