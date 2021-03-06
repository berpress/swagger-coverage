import os
from os.path import exists

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
    def load_yaml(path_to_file: str) -> dict:
        with open(path_to_file, "r") as stream:
            return yaml.safe_load(stream)

    @staticmethod
    def get_path_to_file(path: str, file_name: str) -> str:
        return os.path.join(path, file_name)
