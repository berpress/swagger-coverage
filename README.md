# swagger-coverage
[![Tests](https://github.com/berpress/swagger-coverage/actions/workflows/python-app.yml/badge.svg)](https://github.com/berpress/swagger-coverage/actions/workflows/python-app.yml)
![versions](https://img.shields.io/pypi/pyversions/pybadges.svg)
[![Maintainability](https://api.codeclimate.com/v1/badges/45afb8b947b1c7e9cec8/maintainability)](https://codeclimate.com/github/berpress/swagger-coverage/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/45afb8b947b1c7e9cec8/test_coverage)](https://codeclimate.com/github/berpress/swagger-coverage/test_coverage)
[![PyPI version](https://badge.fury.io/py/test-swagger-coverage.svg)](https://badge.fury.io/py/test-swagger-coverage)
[![Downloads](https://pepy.tech/badge/test-swagger-coverage)](https://pepy.tech/project/test-swagger-coverage)

About
------------

Swagger coverage report helps the QA automation and developer to get a simple API coverage report for endpoints tests

![](https://github.com/berpress/python-api-tests/blob/main/images/swagger_report_2.png)

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

First, we need a link to your swagger. For example,  let's take this  https://app.swaggerhub.com/apis-docs/berpress/flask-rest-api/1.0.0 (see more about this api https://github.com/berpress/flask-restful-api),
and take url to yaml/yml/json swagger file - https://api.swaggerhub.com/apis/berpress/flask-rest-api/1.0.0

Next, in our project, we need to create a file describing our endpoints, which our tests will use to generate a coverage report.

We can do it automatically via the command line

    $ swagger_coverage https://api.swaggerhub.com/apis/berpress/flask-rest-api/1.0.0

Result

    $ 2022-04-15 11:22:37 INFO Start load swagger https://api.swaggerhub.com/apis/berpress/flask-rest-api/1.0.0
    $ 2022-04-15 11:22:38 INFO The swagger report was successfully saved to the folder: /Users/user/Documents/git/python-api-tests/swagger_report



The **swagger_report** directory will be created
and a **data_swagger.yaml** file will appear inside, which will be the settings for building a test coverage report

The **data_swagger.yaml** file looks something like this


 ```
 ...
regUser:
  description: null
  method: POST
  path: /register
  statuses:
  - 201  <---- change from 200 to 201
  - 400
  - 401
  - 403
  tag: register
  ...
 ```

where **regUser** is the unique id of our endpoint

**statuses** is a list of statuses that we will check (that they were called).
You can customize this list yourself.

Only we will check 201 status, as described in the user registration swagger. So I will add it.


Let's create a simple test and build a report. For requests, you will use the **requests** library.

```python
import requests
from swagger_coverage.src.coverage import SwaggerCoverage
from swagger_coverage.src.deco import swagger

# swagger data preparation
swagger_url = "https://api.swaggerhub.com/apis/berpress/flask-rest-api/1.0.0"
api_url = "https://api.swaggerhub.com/apis/"
path='/report' # path to swagger coverage report
swagger_rep = SwaggerCoverage(api_url=api_url, url=swagger_url, path=path)
swagger_rep.create_coverage_data()


# function to call a request to the server
@swagger("regUser")
def register_user(payload: dict):
    return requests.post('https://stores-tests-api.herokuapp.com/register',
                         json=payload)


# test
data = {"username": "test2023@test.com", "password": "Password"}
response = register_user(data)
assert response.status_code == 201

# create report
swagger_rep.create_report()

```
**swagger data preparation**: Prepare our file data_swagger.yaml, it will be created automatically.

**function to call a request to the server**:  We will write a user registration call. Declaring a function with a decorator **@swagger("regUser")**.
**"regUser"** taken from file **data_swagger.yaml**, this is unique id of our endpoint.

**test**: run the test

**create report**: create a report.


After that, in the folder **swagger_report** we will receive a report **index.html**.

Let's see it

![](https://github.com/berpress/python-api-tests/blob/main/images/swagger_register.png)

As you can see, we have increased the counter of verified endpoints

If you use **pytest**, add this code in conftest.py

```python
@pytest.fixture(scope="session", autouse=True)
def swagger_checker(request):
    url = request.config.getoption("--swagger-url")
    url_api = request.config.getoption("--api-url")
    path = '/report'
    swagger = SwaggerCoverage(api_url=url_api, url=url, path=path)
    swagger.create_coverage_data()
    yield
    swagger.create_report()
```
Also, at the end of the report, you can find a table of average request times for routes
![](https://github.com/berpress/python-api-tests/blob/main/images/requets_time.png?raw=true)


Also, at the end of the report, you can find a table of average request times for routes

More example with pytest and API tests https://github.com/berpress/python-api-tests

Report example [https://github.com/berpress/python-api-tests/tree/main/swagger_report](https://github.com/berpress/python-api-tests/tree/main/report)
