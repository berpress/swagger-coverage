import logging

import requests

import yaml

from swagger_coverage.src.models.swagger_data import SwaggerResponse

logger = logging.getLogger("swagger")


def load_swagger(url: str) -> SwaggerResponse:
    """
    Load and get swagger data
    """
    logger.info(f"Start load swagger {url}")
    res = requests.get(url)
    if res.status_code == 200:
        try:
            if res.json().get("swagger"):
                type_swagger = "swagger"
            elif res.json().get("openapi"):
                type_swagger = "openapi"
            else:
                raise ValueError("Type of file is not defined")
            data = yaml.safe_load(res.text)
            return SwaggerResponse(paths=data.get("paths"), swagger_type=type_swagger)
        except Exception:
            raise ValueError("Couldn't load yaml")
    else:
        logger.error(f"Couldn't get the file, status code is {res.status_code}")
