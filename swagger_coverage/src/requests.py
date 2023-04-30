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
            type_swagger = 'swagger' # FIXME
            data = yaml.safe_load(res.text)
            return SwaggerResponse(paths=data.get("paths"), swagger_type=type_swagger)
        except Exception:
            raise ValueError("Couldn't load yaml")
    else:
        logger.error(f"Couldn't get the file, status code is {res.status_code}")
