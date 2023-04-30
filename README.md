# swagger-coverage
[![Tests](https://github.com/berpress/swagger-coverage/actions/workflows/python-app.yml/badge.svg)](https://github.com/berpress/swagger-coverage/actions/workflows/python-app.yml)
![versions](https://img.shields.io/pypi/pyversions/pybadges.svg)
[![Maintainability](https://api.codeclimate.com/v1/badges/45afb8b947b1c7e9cec8/maintainability)](https://codeclimate.com/github/berpress/swagger-coverage/maintainability)
[![PyPI version](https://badge.fury.io/py/test-swagger-coverage.svg)](https://badge.fury.io/py/test-swagger-coverage)
[![Downloads](https://pepy.tech/badge/test-swagger-coverage)](https://pepy.tech/project/test-swagger-coverage)

About
------------

Swagger coverage report helps the QA automation and developer to get a simple API coverage report for endpoints tests

![](https://github.com/berpress/python-api-tests/blob/main/images/1.png?raw=true)

Installation
------------

You can install ``test-swagger-coverage`` via `pip`_ from `PyPI`_::

    $ pip install test-swagger-coverage

or with poetry

    $ poetry add test-swagger-coverage

How it works
------------
We take a swagger as data for testing coverage and, based on it, we create a file that will be the settings for our tests. The file can be created automatically or manually.

Next, we set up api calls in our tests (we wrap them with decorators, see examples) and at the end of testing we generate html report.
We will check which endpoints were called and what statuses we checked.

We can't always trust our swagger, so you can manually set the status of the codes yourself, which need to be checked.

Examples
------------

First, we need a link to your swagger. For example,  let's take this  https://petstore.swagger.io/

Next, in our project, we need to create a file describing our endpoints, which our tests will use to generate a coverage report.

We can do it automatically via the command line, get json swagger file

    $ swagger_coverage https://petstore.swagger.io/v2/swagger.json

Result

    $ 2022-04-15 11:22:37 INFO Start load swagger swagger_coverage https://petstore.swagger.io/v2/swagger.json
    $ 2022-04-15 11:22:38 INFO The swagger report was successfully saved to the folder: /Users/user/Documents/git/python-api-tests/swagger_report



The **swagger_report** directory will be created
and a **data_swagger.yaml** file will appear inside, which will be the settings for building a test coverage report

The **data_swagger.yaml** file looks something like this


 ```
 ...
addPet:
  description: 'Add new pet'
  method: POST
  path: /pet
  statuses:
  - 200
  - 404
  tag: pet
  ...
 ```

where **addPet** is the unique id of our endpoint

 ```
 ...
addPet:
  description: 'Add new pet'
  method: POST
  path: /pet
  statuses:
  - 200
  - 404  <---- add 404 status code 
  - 404
  tag: pet
  ...
 ```

We can change or add our data, for example, a new status code, which will need to be checked

**statuses** is a list of statuses that we will check (that they were called).
You can customize this list yourself.



Let's create a simple test and build a report. For requests, you will use the **requests** library.
We will check that a non-existent pet returns a 404 status code

```python
import requests

from swagger_coverage.src.coverage import SwaggerCoverage
from swagger_coverage.src.deco import swagger

# settings
SWAGGER_URL = 'https://petstore.swagger.io/v2/swagger.json'
STATUS_CODES = [200, 404]


# our request that we will cover
@swagger("getPetById")
def get_pet_by_id():
    return requests.get("https://petstore.swagger.io/v2/pet/999")  # <-- 999 pet id no such exists


# create swagger objects
swagger = SwaggerCoverage(
    url=SWAGGER_URL,
    status_codes=STATUS_CODES,
    api_url="https://petstore.swagger.io/",
)
swagger.create_coverage_data()
get_pet_by_id()
swagger.create_report()


```
**swagger data preparation**: Prepare our file data_swagger.yaml, it will be created automatically.

**function to call a request to the server**:  We will write a user registration call. Declaring a function with a decorator **@swagger("regUser")**.
**"regUser"** taken from file **data_swagger.yaml**, this is unique id of our endpoint.

**test**: run the test

**create report**: create a report.


After that, in the folder **swagger_report** we will receive a report **index.html**.

Let's see it

![](https://github.com/berpress/python-api-tests/blob/main/images/4.png?raw=true)

As you can see, an endpoint appeared in the report, which was partially verified. Filtering the results and open more info window

![](https://github.com/berpress/python-api-tests/blob/main/images/5.png?raw=true)

Test and coverage passed successfully!


If you use **pytest**, add this code in conftest.py

```python
import pytest
from swagger_coverage.src.coverage import SwaggerCoverage

@pytest.fixture(scope="session", autouse=True)
def swagger_checker(request):
    url = 'https://petstore.swagger.io/v2/swagger.json'
    url_api = 'https://petstore.swagger.io'
    swagger = SwaggerCoverage(api_url=url_api, url=url)
    swagger.create_coverage_data()
    yield
    swagger.create_report()
```
Also, at the end of the report, you can find a table of average request times for routes

More example with pytest and API tests https://github.com/berpress/python-api-tests

Report example https://github.com/berpress/python-api-tests/blob/main/swagger_report/index.html
