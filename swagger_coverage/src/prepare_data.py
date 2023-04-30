import logging

from swagger_coverage.src.models.swagger_data import SwaggerResponse

logger = logging.getLogger("swagger")


def _prepare_swagger(data, status_codes):
    res_dict = {}
    for key, value in data.items():
        list_values = list(value.values())
        for values in list_values:
            res_dict[values.get("operationId")] = []
        for method, description in value.items():
            res_dict[description.get("operationId")] = {
                "method": method.upper(),
                "description": description.get("description"),
                "path": key,
                "statuses": status_codes,
                "tag": description.get("tags")[0],
            }
    return res_dict


def _prepare_openapi(data, status_codes):
    res_dict = {}
    uuid = 1
    for key, value in data.items():
        for method, description in value.items():
            res_dict[uuid] = {
                "method": method.upper(),
                "description": description.get("summary"),
                "path": key,
                "statuses": status_codes,
                "tag": description.get("tags")[0],
            }
            uuid = uuid + 1
    return res_dict
class PrepareData:
    def prepare_swagger_data(self, data: SwaggerResponse, status_codes: list) -> dict:
        """
        Preparing data for tests
        :param status_codes:
        :param data:
        :return: swagger dict
        """
        type_swagger = data.swagger_type
        return self._map_prepare.get(type_swagger)(data.paths, status_codes)

    @staticmethod
    def prepare_check_file_data(data: dict) -> dict:
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

    _map_prepare = {"swagger": _prepare_swagger, "openapi": _prepare_openapi}

