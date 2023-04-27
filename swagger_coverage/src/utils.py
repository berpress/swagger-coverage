import json


def to_dict(data) -> dict:
    """
    Convert nested object to dict
    :return: dict
    """
    return json.loads(json.dumps(data, default=lambda o: o.__dict__))


class obj(object):
    """
    Convert dict to object
    """

    def __init__(self, dict_):
        self.__dict__.update(dict_)


def dict2obj(d):
    return json.loads(json.dumps(d), object_hook=obj)
