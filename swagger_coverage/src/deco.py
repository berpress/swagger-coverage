from functools import wraps

from swagger_coverage.src.check_data import SwaggerChecker


def swagger(key):
    def wrapper(function):
        @wraps(function)
        def inner(*args, **kwargs):
            res = function(*args, **kwargs)
            try:
                SwaggerChecker().swagger_check(key, res)
                return res
            except AttributeError:
                return res

        return inner

    return wrapper
