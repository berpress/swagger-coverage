from functools import wraps

from swagger_coverage.coverage import Swagger


def swagger(key):
    def wrapper(function):
        @wraps(function)
        def inner(*args, **kwargs):
            res = function(*args, **kwargs)
            Swagger().swagger_check(key, res)
            return res

        return inner

    return wrapper
