from typing import List


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
            if avg_time > 1:
                color = "danger"
            elif avg_time > 0.5:
                color = "warning"
            else:
                color = "light"
            results.append({"name": name, "results": avg_time, "color": color})
    sorted_results = sorted(results, key=lambda d: d["results"], reverse=True)
    return sorted_results
