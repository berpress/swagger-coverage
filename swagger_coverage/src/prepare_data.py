from typing import Dict

import requests

import logging

import yaml

logger = logging.getLogger("swagger")


class PrepareData:
    @staticmethod
    def load_swagger(url: str) -> Dict:
        """
        Load and get swagger data
        """
        logger.info(f"Start load swagger {url}")
        res = requests.get(url)
        if res.status_code == 200:
            try:
                data = yaml.safe_load(res.text)
                return data.get("paths")
            except Exception:
                raise ValueError("Couldn't load yaml")
        else:
            logger.error(f"Couldn't get the file, status code is {res.status_code}")

    @staticmethod
    def prepare_swagger_data(data, status_codes: list) -> dict:
        """
        Preparing data for tests
        :param status_codes:
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
                    "statuses": status_codes,
                    "tag": v.get("tags")[0],
                    "time": [],
                }
        return res_dict

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
