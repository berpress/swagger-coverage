import time
from functools import wraps

from swagger_coverage.src.check_data import SwaggerChecker


def swagger(key):
    def wrapper(function):
        @wraps(function)
        def inner(*args, **kwargs):
            start = time.time()
            res = function(*args, **kwargs)
            end = time.time()
            time_execution = end - start
            try:
                SwaggerChecker().swagger_check(key, res, time_execution)
                return res
            except AttributeError:
                return res

        return inner

    return wrapper
