import json
import os
from os.path import exists
from time import time


import yaml


class FileOperation:
    @staticmethod
    def create_dir(dir_name: str):
        if not exists(dir_name):
            os.mkdir(dir_name)

    @staticmethod
    def save_yaml(data: dict, path_file: str):
        """
        save yaml
        """
        with open(path_file, "w") as outfile:
            yaml.Dumper.ignore_aliases = lambda self, data: True
            yaml.dump(data, outfile, default_flow_style=False, Dumper=yaml.Dumper)

    @staticmethod
    def save_json(data: dict, path_file: str):
        """
        save json file
        """
        FileOperation.create_dir(path_file + "/json_results/")
        file_to_write = (
            path_file + f"/json_results/{str(int(time() * 1000))}_results.json"
        )
        with open(file_to_write, "w") as f:
            json.dump(data, f)

    @staticmethod
    def load_yaml(path_to_file: str) -> dict:
        with open(path_to_file, "r") as stream:
            return yaml.safe_load(stream)

    @staticmethod
    def get_path_to_file(path: str, file_name: str) -> str:
        return os.path.join(path, file_name)

    @staticmethod
    def load_json(path):
        with open(path) as handle:
            return json.loads(handle.read())
