import json
import pathlib
import uuid
import os
from os.path import exists
from typing import List

import yaml

from swagger_coverage.src.models.swagger_data import SwaggerData
from swagger_coverage.src.utils import to_dict


def prepare_path(path: str, report_dir: str) -> str:
    """
    param path: parth to report dir, for example '/report'
    :return: return path to report dir
    """
    if path is None:
        parent_dir = os.path.abspath(os.path.abspath(os.curdir))
        return os.path.join(parent_dir, report_dir)
    parent_dir = os.path.abspath(os.path.abspath(os.curdir))
    path = path[1:] if path.find("/") == 0 else path
    return os.path.join(parent_dir, path)


def get_parent_dir() -> str:
    return os.path.abspath(os.path.abspath(os.curdir))


def get_path_results(parent_dir: str, report_dir) -> str:
    return os.path.join(parent_dir, report_dir, "json_results")


def create_dir(dir_name: str):
    if not exists(dir_name):
        os.mkdir(dir_name)


def get_path_to_file(path: str, file_name: str) -> str:
    return os.path.join(path, file_name)


def is_file_exist(path: str) -> bool:
    return exists(path)


def save_yaml(data: dict, path_file: str):
    """
    save yaml
    """
    with open(path_file, "w") as outfile:
        yaml.Dumper.ignore_aliases = lambda self, data: True
        yaml.dump(data, outfile, default_flow_style=False, Dumper=yaml.Dumper)


def load_yaml(path_to_file: str) -> dict:
    with open(path_to_file, "r") as stream:
        return yaml.safe_load(stream)


def save_results_to_json(data: SwaggerData, path_file: str) -> str:
    """
    save json file
    """
    create_dir(path_file + "/json_results/")
    file_to_write = path_file + f"/json_results/{uuid.uuid4()}.json"
    with open(file_to_write, "w") as f:
        json.dump(to_dict(data), f)
    return file_to_write


def get_json_result_path(path) -> List[pathlib.Path]:
    return list(pathlib.Path(path).glob("*.json"))


def load_json(path):
    with open(path) as handle:
        return json.loads(handle.read())
