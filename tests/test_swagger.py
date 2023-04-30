import shutil

import pytest
import requests

from swagger_coverage.src.coverage import (
    SwaggerCoverage,
    _SWAGGER_REPORT_DIR,
)
from swagger_coverage.src.deco import swagger
from swagger_coverage.src.files import load_yaml, is_file_exist

SWAGGER_URL_2 = "https://petstore.swagger.io/v2/swagger.json"
OPEN_API_URL = "xxxx"


@swagger("getPetById")
def get_pet_by_id():
    return requests.get("https://petstore.swagger.io/v2/pet/999")


def delete_after_test(path="swagger_report"):
    shutil.rmtree(path)


def test_inc_passed_route():
    """
    Check, that checked rout is increased
    :return:
    """
    status_codes = [200, 404]
    swagger = SwaggerCoverage(url=SWAGGER_URL_2, status_codes=status_codes)
    swagger.create_coverage_data(file_name="swagger_files_exist.yaml")

    res = get_pet_by_id()
    status_code = res.status_code
    statuses = swagger.data.swagger_data.get("getPetById").get("statuses")
    result = -1
    for status in statuses:
        if status_code in list(status.keys()):
            result = status.get(status_code)
    assert result == 1, "Deco not working"
    swagger.__class__.clear()
    delete_after_test()


def test_check_file_exist():
    """
    Check, that checked rout is increased
    :return:
    """
    name = "swagger_check_file_exist"
    status_codes = [200, 404]
    swagger = SwaggerCoverage(
        url=SWAGGER_URL_2,
        status_codes=status_codes,
    )
    swagger.create_coverage_data(file_name=f"{name}.yaml")
    assert is_file_exist(f"{_SWAGGER_REPORT_DIR}/{name}.yaml")
    swagger.__class__.clear()
    delete_after_test()


def test_check_file_data():
    """
    Check, that checked rout is increased
    :return:
    """
    name = "swagger_check_file_data"
    status_codes = [200, 404]
    swagger = SwaggerCoverage(
        url=SWAGGER_URL_2,
        status_codes=status_codes,
    )
    swagger.create_coverage_data(file_name=f"{name}.yaml")
    file_data = load_yaml(f"{_SWAGGER_REPORT_DIR}/{name}.yaml")
    assert file_data
    swagger.__class__.clear()
    delete_after_test()


def test_save_results():
    name = "swagger_check_save_results"
    status_codes = [200, 404]
    swagger = SwaggerCoverage(
        url=SWAGGER_URL_2,
        status_codes=status_codes,
    )
    swagger.create_coverage_data(file_name=f"{name}.yaml")
    get_pet_by_id()
    file_path = swagger.save_results()
    assert is_file_exist(file_path)
    swagger.__class__.clear()
    delete_after_test()


def test_create_html_report_with_save_file():
    name = "swagger_check_create_html_report"
    status_codes = [200, 404]
    swagger = SwaggerCoverage(
        url=SWAGGER_URL_2,
        status_codes=status_codes,
        api_url="https://petstore.swagger.io/",
    )
    swagger.create_coverage_data(file_name=f"{name}.yaml")
    get_pet_by_id()
    swagger.create_report()
    assert is_file_exist(f"{_SWAGGER_REPORT_DIR}/index.html")
    swagger.__class__.clear()
    delete_after_test()


@pytest.mark.skip(reason="Only for local run")
def test_check_open_api():
    """
    Check, that checked rout is increased
    :return:
    """
    name = "swagger_check_file_exist"
    status_codes = [200, 404]
    swagger = SwaggerCoverage(
        url=OPEN_API_URL, status_codes=status_codes, api_url="xxxx"
    )
    swagger.create_coverage_data(file_name=f"{name}.yaml")
    swagger.create_report()
    assert is_file_exist(f"{_SWAGGER_REPORT_DIR}/index.html")
    swagger.__class__.clear()
    delete_after_test()