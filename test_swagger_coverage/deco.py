from functools import wraps

from test_swagger_coverage.swagger_coverage import Swagger


def swagger(key):
    def wrapper(function):
        @wraps(function)
        def inner(*args, **kwargs):
            res = function(*args, **kwargs)
            Swagger().swagger_check(key, res)
            return res

        return inner

    return wrapper
