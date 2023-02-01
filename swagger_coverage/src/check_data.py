import copy

from requests import Response

from swagger_coverage.src.coverage import SwaggerCoverage


class SwaggerChecker:
    def __init__(self):
        self.data = SwaggerCoverage().data

    def swagger_check(self, key: str, res: Response, time_execution: float) -> None:
        """
        Try to check response status code and swagger data
        """
        dict_data = copy.deepcopy(self.data)
        SwaggerCoverage().data = self._set_check_result(
            key, res.status_code, dict_data, time_execution
        )

    @staticmethod
    def _set_check_result(
        key: str, status_code: int, data, time_execution: float
    ) -> dict:
        """
        Set check result
        """
        endpoint = data.swagger_data.get(key)
        if endpoint:
            if endpoint.get("time_executions") is None:
                endpoint["time_executions"] = [time_execution]
            else:
                t_exc = endpoint.get("time_executions")
                t_exc.append(time_execution)
            statuses = endpoint.get("statuses")
            for status in statuses:
                for key in status.keys():
                    if key == status_code:
                        status[key] = status.get(key, 0) + 1

                        return data
        return data
